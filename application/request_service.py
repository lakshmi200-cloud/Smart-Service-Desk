from domain.exceptions import (
    AlreadyResolvedError,
    DuplicateRequestError,
    RequestNotFoundError,
)
from domain.service_request import ServiceRequest


class RequestService:
    """Application use cases. It depends on a repository abstraction."""

    def __init__(self, repository):
        self.repository = repository
        self._requests = {}
        self.load_requests()

    def load_requests(self):
        loaded = self.repository.load_all()
        self._requests = {request.request_id: request for request in loaded}

    def create_request(self, request_id, employee_name, issue, priority):
        request_id = str(request_id).strip()
        if request_id in self._requests:
            raise DuplicateRequestError(
                f"Request ID '{request_id}' already exists. Use a different ID."
            )
        request = ServiceRequest(request_id, employee_name, issue, priority)
        self._requests[request.request_id] = request
        self._save()
        return request

    def view_requests(self):
        return list(self._requests.values())

    def search_request(self, request_id):
        request = self._requests.get(str(request_id).strip())
        if request is None:
            raise RequestNotFoundError(
                f"Request '{str(request_id).strip()}' was not found."
            )
        return request

    def resolve_request(self, request_id):
        request = self.search_request(request_id)
        if not request.resolve():
            raise AlreadyResolvedError(
                f"Request '{request.request_id}' is already RESOLVED."
            )
        self._save()
        return request

    def _save(self):
        self.repository.save_all(self.view_requests())
