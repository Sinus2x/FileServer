from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DownloadRequest(_message.Message):
    __slots__ = ["bucket", "filename"]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    filename: str
    def __init__(self, bucket: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class DownloadResponse(_message.Message):
    __slots__ = ["chunk_data", "meta"]
    CHUNK_DATA_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    chunk_data: bytes
    meta: MetaData
    def __init__(self, chunk_data: _Optional[bytes] = ..., meta: _Optional[_Union[MetaData, _Mapping]] = ...) -> None: ...

class File(_message.Message):
    __slots__ = ["bucket", "chunk_data", "filename", "last_modified"]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    CHUNK_DATA_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    LAST_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    chunk_data: bytes
    filename: str
    last_modified: str
    def __init__(self, chunk_data: _Optional[bytes] = ..., bucket: _Optional[str] = ..., filename: _Optional[str] = ..., last_modified: _Optional[str] = ...) -> None: ...

class FileListRequest(_message.Message):
    __slots__ = ["bucket"]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    def __init__(self, bucket: _Optional[str] = ...) -> None: ...

class FileListResponse(_message.Message):
    __slots__ = ["files"]
    FILES_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[MetaData]
    def __init__(self, files: _Optional[_Iterable[_Union[MetaData, _Mapping]]] = ...) -> None: ...

class GetFileRequest(_message.Message):
    __slots__ = ["bucket", "filename"]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    filename: str
    def __init__(self, bucket: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class MetaData(_message.Message):
    __slots__ = ["bucket", "filename", "hash", "last_modified", "size"]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    LAST_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    filename: str
    hash: str
    last_modified: str
    size: float
    def __init__(self, bucket: _Optional[str] = ..., filename: _Optional[str] = ..., hash: _Optional[str] = ..., last_modified: _Optional[str] = ..., size: _Optional[float] = ...) -> None: ...

class RemoveFileRequest(_message.Message):
    __slots__ = ["bucket", "filename"]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    filename: str
    def __init__(self, bucket: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class RemoveFileResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
