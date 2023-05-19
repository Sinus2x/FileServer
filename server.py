import io

import file_service_pb2_grpc
import logging
import grpc
import os

from datetime import datetime
from file_service_pb2 import *
from google.protobuf.timestamp_pb2 import Timestamp

from concurrent import futures
from minio.datatypes import Object
from minio import Minio
from minio.error import S3Error, InvalidResponseError, ServerError


class Servicer(file_service_pb2_grpc.GreeterServicer):
    def __init__(self):
        self.storage = self._get_minio_client()

    @staticmethod
    def _get_minio_client():
        access_key = os.environ.get('MINIO_ACCESS_KEY')
        secret_key = os.environ.get('MINIO_SECRET_KEY')
        return Minio(
            'localhost:9000',
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )

    @staticmethod
    def _to_timestamp(dt: datetime) -> Timestamp:
        timestamp = Timestamp()
        timestamp.FromDatetime(dt)
        return timestamp

    @staticmethod
    def _read_bytes(chunk_data):
        data = io.BytesIO(chunk_data)
        return data, data.getbuffer().nbytes

    @classmethod
    def _meta_from_stat(cls, stat: Object):
        return MetaData(
            bucket=stat.bucket_name,
            filename=stat.object_name,
            hash=stat.etag,
            date=cls._to_timestamp(stat.last_modified)
        )

    def _check_bucket(self, bucket: str) -> None:
        if self.storage.bucket_exists(bucket):
            return
        self.storage.make_bucket(bucket)

    def DownloadFile(
            self,
            request: DownloadRequest,
            context=None
    ) -> DownloadResponse:
        self._check_bucket(request.bucket)
        try:
            data = self.storage.get_object(
                bucket_name=request.bucket,
                object_name=request.filename
            )
            stat = self.storage.stat_object(
                bucket_name=request.bucket,
                object_name=request.filename
            )
            return DownloadResponse(
                chunk_data=data.read(),
                meta=self._meta_from_stat(stat)
            )
        except S3Error as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(e.message)
            return DownloadResponse()
        except InvalidResponseError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return DownloadResponse()
        except ServerError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return DownloadResponse()

    def UploadFile(
            self,
            request: File,
            context=None
    ) -> MetaData:
        self._check_bucket(request.bucket)
        data, length = self._read_bytes(request.chunk_data)
        self.storage.put_object(
            bucket_name=request.bucket,
            object_name=request.filename,
            data=data,
            length=length
        )
        stat = self.storage.stat_object(
            bucket_name=request.bucket,
            object_name=request.filename
        )
        return self._meta_from_stat(stat)

    def RemoveFile(
            self,
            request: MetaData,
            context=None
    ) -> RemoveFileResponse:
        self._check_bucket(request.bucket)
        try:
            self.storage.remove_object(
                bucket_name=request.bucket,
                object_name=request.filename
            )
            return RemoveFileResponse()
        except InvalidResponseError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return RemoveFileResponse()
        except ServerError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return RemoveFileResponse()

    def GetFileList(
            self,
            request: FileListRequest,
            context=None
    ) -> FileListResponse:
        self._check_bucket(request.bucket)
        try:
            response = self.storage.list_objects(request.bucket)
            files = [
                self._meta_from_stat(obj)
                for obj in response
            ]
            return FileListResponse(
                files=files
            )
        except InvalidResponseError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return FileListResponse()
        except ServerError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return FileListResponse()

    def GetFile(
            self,
            request: GetFileRequest,
            context=None
    ) -> MetaData:
        self._check_bucket(request.bucket)
        try:
            stat = self.storage.stat_object(
                bucket_name=request.bucket,
                object_name=request.filename
            )
            return self._meta_from_stat(stat)
        except S3Error as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(e.message)
            return MetaData()
        except InvalidResponseError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return MetaData()
        except ServerError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return MetaData()


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_service_pb2_grpc.add_GreeterServicer_to_server(Servicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()