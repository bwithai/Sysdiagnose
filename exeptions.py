from fastapi import HTTPException, status


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str, headers: dict = None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


# General file upload exceptions
file_size_limit_exception = CustomHTTPException(
    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    detail="File size exceeds the limit"
)

file_extension_exception = CustomHTTPException(
    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    detail="Invalid file extension"
)

# Custom business logic exceptions for file uploads
invalid_file_format_exception = CustomHTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid file format"
)

file_not_uploaded_exception = CustomHTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="File not uploaded"
)

# Add these to your existing exceptions
duplicate_record_exception = CustomHTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Record already exists.",
    headers={"WWW-Authenticate": "Bearer"},
)

expired_token_exception = CustomHTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Token expired'
)

invalid_token_exception = CustomHTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid token'
)

not_found_exception = CustomHTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Record not found"
)
