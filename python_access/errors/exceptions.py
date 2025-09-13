class NotFoundError(Exception):
    """Raised when a requested resource is not found."""

    def __init__(self, message="Resource not found"):
        self.message = message
        super().__init__(self.message)

class DeleteError(Exception):
    """Raised when a delete operation fails."""

    def __init__(self, message="Delete operation failed"):
        self.message = message
        super().__init__(self.message)

class CreateError(Exception):
    """Raised when a create operation fails."""

    def __init__(self, message="Create operation failed"):
        self.message = message
        super().__init__(self.message)