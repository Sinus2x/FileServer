from __future__ import print_function

import logging

import grpc
import file_service_pb2
import file_service_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = file_service_pb2_grpc.GreeterStub(channel)
        download = stub.DownloadFile(file_service_pb2.MetaData(
            bucket='test',
            filename='code.txt'
        )
        )
        print(download.meta.date.ToDatetime())
        # print("Greeter client received: " + response.message)
        with open('download_response1.txt', 'wb') as f:
            f.write(download.chunk_data)


        with open('test.txt', 'rb') as f:
            upload = stub.UploadFile(
                file_service_pb2.File(
                    chunk_data=f.read(),
                    filename='test.txt',
                    bucket='test',
                )
            )
        print(upload)

        rm = stub.RemoveFile(
            file_service_pb2.RemoveFileRequest(
                bucket='test',
                filename='testtxt'
            )
        )
        print(rm)

        files = stub.GetFileList(
            file_service_pb2.FileListRequest(
                bucket='test'
            )
        )
        print(files.files)

        file = stub.GetFile(
            file_service_pb2.GetFileRequest(
                bucket='test',
                filename='code.txt'
            )
        )
        print(file)

if __name__ == '__main__':
    logging.basicConfig()
    run()