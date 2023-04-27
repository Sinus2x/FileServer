from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class File(_message.Message):
    __slots__ = ["chunk_data", "meta"]
    CHUNK_DATA_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    chunk_data: bytes
    meta: MetaData
    def __init__(self, meta: _Optional[_Union[MetaData, _Mapping]] = ..., chunk_data: _Optional[bytes] = ...) -> None: ...

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

class FileRequest(_message.Message):
    __slots__ = ["bucket", "extension", "filename"]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    extension: str
    filename: str
    def __init__(self, bucket: _Optional[str] = ..., filename: _Optional[str] = ..., extension: _Optional[str] = ...) -> None: ...

class MetaData(_message.Message):
    __slots__ = ["bucket", "date", "extension", "filename", "hash"]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    bucket: str
    date: str
    extension: str
    filename: str
    hash: str
    def __init__(self, bucket: _Optional[str] = ..., filename: _Optional[str] = ..., extension: _Optional[str] = ..., hash: _Optional[str] = ..., date: _Optional[str] = ...) -> None: ...
