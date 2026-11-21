from datetime import datetime, timezone

from domain.exceptions import InvalidPriorityError


class ServiceRequest:
    """Domain entity representing one employee IT support request."""

    ALLOWED_PRIORITIES = {"LOW", "MEDIUM", "HIGH"}
    ALLOWED_STATUSES = {"OPEN", "RESOLVED"}

    def __init__(
        self,
        request_id,
        employee_name,
        issue,
        priority,
        status="OPEN",
        created_at=None,
        resolved_at=None,
    ):
        self.request_id = self._required_text(request_id, "Request ID")
        self.employee_name = self._required_text(employee_name, "Employee name")
        self.issue = self._required_text(issue, "Issue description")
        self._priority = self._validate_priority(priority)

        normalized_status = str(status).strip().upper()
        if normalized_status not in self.ALLOWED_STATUSES:
            raise ValueError("Status must be OPEN or RESOLVED.")
        self._status = normalized_status
        self.created_at = created_at or datetime.now(timezone.utc).isoformat()
        self.resolved_at = resolved_at

    @staticmethod
    def _required_text(value, field_name):
        value = str(value).strip()
        if not value:
            raise ValueError(f"{field_name} cannot be empty.")
        return value

    @classmethod
    def _validate_priority(cls, priority):
        normalized = str(priority).strip().upper()
        if normalized not in cls.ALLOWED_PRIORITIES:
            raise InvalidPriorityError("Priority must be LOW, MEDIUM or HIGH.")
        return normalized

    @property
    def priority(self):
        return self._priority

    @property
    def status(self):
        return self._status

    def resolve(self):
        """Apply the business rule for resolving an open request."""
        if self._status == "OPEN":
            self._status = "RESOLVED"
            self.resolved_at = datetime.now(timezone.utc).isoformat()
            return True
        return False

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "employee_name": self.employee_name,
            "issue": self.issue,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
            "resolved_at": self.resolved_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            request_id=data["request_id"],
            employee_name=data["employee_name"],
            issue=data["issue"],
            priority=data["priority"],
            status=data.get("status", "OPEN"),
            created_at=data.get("created_at"),
            resolved_at=data.get("resolved_at"),
        )
