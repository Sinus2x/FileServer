import io

import file_service_pb2_grpc
import file_service_pb2
from concurrent import futures
import logging
import grpc
import os

from dotenv import load_dotenv
from minio import Minio


class Servicer(file_service_pb2_grpc.GreeterServicer):
    def __init__(self):
        self.storage = self._get_minio_client()

    @staticmethod
    def _get_minio_client():
        dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)

        access_key = os.environ.get('MINIO_ACCESS_KEY')
        secret_key = os.environ.get('MINIO_SECRET_KEY')

        return Minio(
            'localhost:9000',
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )

    def DownloadFile(
            self,
            request: file_service_pb2.MetaData,
            context=None
    ) -> file_service_pb2.File:
        data = self.storage.get_object(
            bucket_name=request.bucket,
            object_name=f'{request.filename}.{request.extension}'
        )
        return file_service_pb2.File(
            chunk_data=data.read(),
            # meta=request
        )

    def UploadFile(
            self,
            request: file_service_pb2.File,
            context=None
    ) -> file_service_pb2.MetaData:
        data = io.BytesIO(request.chunk_data)
        result = self.storage.put_object(
            bucket_name=request.meta.bucket,
            object_name=f'{request.meta.filename}.{request.meta.extension}',
            data=data,
            length=data.getbuffer().nbytes
        )
        meta = self.storage.stat_object(
            bucket_name=request.meta.bucket,
            object_name=f'{request.meta.filename}.{request.meta.extension}'
        )
        print(meta.last_modified)

        return file_service_pb2.MetaData(
            bucket=result.bucket_name,
            filename=result.object_name.split('.')[0],
            extension=result.object_name.split('.')[1],
            hash=meta.etag,
            date=meta.last_modified,
        )

    def RemoveFile(
            self,
            request: file_service_pb2.MetaData,
            context=None
    ) -> file_service_pb2.MetaData:
        bucket = request.bucket
        name = request.filename
        ext = request.extension
        self.storage.remove_object(bucket, f'{name}.{ext}')
        return request

    def GetFileList(
            self,
            request: file_service_pb2.FileListRequest,
            context=None
    ) -> file_service_pb2.FileListResponse:
        bucket = request.bucket
        response = self.storage.list_objects(bucket)
        files = [
            file_service_pb2.MetaData(
                bucket=bucket,
                filename=obj.object_name.split('.')[0],
                extension=obj.object_name.split('.')[1],
                hash=obj.etag,
                # date=obj.last_modified
            )
            for obj in response
        ]
        print(files)
        return file_service_pb2.FileListResponse(
            files=files
        )

    @staticmethod
    def _filename(name: str, ext: str):
        return f'{name}.{ext}'

    def GetFile(
            self,
            request: file_service_pb2.FileRequest,
            context
    ) -> file_service_pb2.MetaData:
        name = self._filename(request.filename, request.extension)
        meta = self.storage.stat_object(
            bucket_name=request.bucket,
            object_name=name
        )
        return file_service_pb2.MetaData(
            **request,
            hash=meta.etag,
            date=meta.last_modified
        )


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