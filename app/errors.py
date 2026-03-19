#app/errors.py


class SermonError(Exception):
    """Basfel för applikationen."""
    pass


class NotFoundError(SermonError):
    pass


class ValidationError(SermonError):
    pass


class ConflictError(SermonError):
    pass


class DatabaseError(SermonError):
    pass


class FileError(SermonError):
    pass


