class ServiceDeskError(Exception):
    """Base exception for expected service-desk errors."""


class DuplicateRequestError(ServiceDeskError):
    pass


class RequestNotFoundError(ServiceDeskError):
    pass


class InvalidPriorityError(ServiceDeskError):
    pass


class AlreadyResolvedError(ServiceDeskError):
    pass


class PersistenceError(ServiceDeskError):
    pass


class AuthenticationError(ServiceDeskError):
    pass
