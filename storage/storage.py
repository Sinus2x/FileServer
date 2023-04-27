import datetime
import hashlib
import os

from dotenv import load_dotenv
from minio import Minio
from minio.error import InvalidResponseError, S3Error
from minio.tagging import Tags
from minio.versioningconfig import VersioningConfig


class MinioServer:

    def __init__(self):
        self._minio_client = self._get_minio_client()
        # self._bucket_name = 'test'
        # self._check_bucket()

    @staticmethod
    def _get_minio_client():
        dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)

        access_key = os.environ.get('MINIO_ACCESS_KEY')
        secret_key = os.environ.get('MINIO_SECRET_KEY')

        return Minio(
            'localhost:9001',
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )

    def _check_bucket(self, bucket_name: str):
        if not self._minio_client.bucket_exists(bucket_name):
            try:
                self._minio_client.make_bucket(bucket_name)
                self._minio_client.set_bucket_versioning(bucket_name)
            except InvalidResponseError:
                raise Exception

    def _check_file(self, file_name: str):
        if not os.path.exists(file_name):
            print(f"file {file_name} doesnt exist on client")
            try:
                self.download_file(file_name=file_name)
            except S3Error:
                raise
            return

        print(f"file {file_name} exists on client")
        try:
            response = self._minio_client.get_object(self._bucket_name, file_name)
            response.close()
            response.release_conn()
        except S3Error:
            print("no such file on server, uploading new one")
            self._upload_file(file_name=file_name)
        print(f"file {file_name} exists on server")

    def download_file(self, file_name: str):
        # file_path = file_name
        # if from_server:
        #     file_path = self._make_file_from_server(file_name)

        try:
            self._minio_client.fget_object(bucket_name=self._bucket_name, object_name=file_name, file_path=file_name)
            print(f"file {file_name} successfully downloaded from server")
        except InvalidResponseError as error:
            print(error)
        except S3Error:
            print(f"file {file_name} doesnt exist on server")

    # def _make_file_from_server(self, file_name: str):
    #     first, second = file_name.split('.', maxsplit=1)
    #     return first + "_from_server" + '.' + second

    def _upload_file(self, file_name: str):
        try:
            with open(file_name, 'rb') as textfile:
                statdata = os.stat(file_name)
                tags = Tags(for_object=True)
                tags['hash'] = self._md5(file_name)
                tags['date'] = str(self._last_modified_date(file_name))
                result = self._minio_client.put_object(bucket_name=self._bucket_name,
                                                       object_name=file_name,
                                                       data=textfile,
                                                       length=statdata.st_size,
                                                       content_type='text/plain',
                                                       tags=tags
                                                       )
                print(f'file {result.object_name} successfully uploaded to server')
        except InvalidResponseError as error:
            print(error)
        return result

    def _files_equal(self, file_name: str) -> bool:
        local_hash = self._md5(file_name)
        tags = self._minio_client.get_object_tags(bucket_name=self._bucket_name, object_name=file_name)
        remote_hash = tags['hash']
        return remote_hash == local_hash

    def upload_file(self, file_name: str):
        try:
            self._check_file(file_name)
        except FileExistsError:
            print(f"file {file_name} doesnt exist anywhere")
            return
        if self._files_equal(file_name):
            self._upload_file(file_name=file_name)
        else:
            local_date = self._last_modified_date(file_name)
            remote_date_str = self._minio_client.get_object_tags(self._bucket_name, file_name)['date']
            remote_date = datetime.datetime.fromisoformat(remote_date_str)

            # self._download_file(file_name=file_name, from_server=True)

            if remote_date > local_date:
                self.download_file(file_name=file_name)
            else:
                self._upload_file(file_name)

    def _md5(self, file_name):
        hash_md5 = hashlib.md5()
        with open(file_name, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def _last_modified_date(self, file_name: str) -> datetime.datetime:
        try:
            return datetime.datetime.fromtimestamp(os.path.getmtime(file_name))
        except OSError:
            print('no such file')
        return datetime.datetime.now()

    def get_file_info(self, file_name: str):
        # try:
        #     print(f"file {file_name} successfully downloaded from server")

