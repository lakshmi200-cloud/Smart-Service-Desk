import json
from pathlib import Path

from domain.exceptions import PersistenceError
from domain.service_request import ServiceRequest


class FileRepository:
    """Infrastructure adapter responsible only for JSON persistence."""

    def __init__(self, file_path="data/requests.json"):
        self.file_path = Path(file_path)

    def load_all(self):
        if not self.file_path.exists():
            return []
        try:
            raw = self.file_path.read_text(encoding="utf-8").strip()
            if not raw:
                return []
            records = json.loads(raw)
            if not isinstance(records, list):
                raise PersistenceError("The requests JSON file must contain a list.")

            if not all(isinstance(item, dict) for item in records):
                raise PersistenceError("Each request record must be a JSON Object.")

            return [ServiceRequest.from_dict(item) for item in records]

        
        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError) as exc:
            if isinstance(exc, PersistenceError):
                raise
            raise PersistenceError(
                f"Could not load request data: {exc}. Check data/requests.json."
            ) from exc

    def save_all(self, requests):
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            temporary_path = self.file_path.with_suffix(".tmp")
            payload = [request.to_dict() for request in requests]
            temporary_path.write_text(
                json.dumps(payload, indent=4), encoding="utf-8"
            )
            temporary_path.replace(self.file_path)
        except OSError as exc:
            raise PersistenceError(f"Could not save request data: {exc}") from exc
