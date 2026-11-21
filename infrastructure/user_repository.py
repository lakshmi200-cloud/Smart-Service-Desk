
import json
from pathlib import Path


class UserRepository:
    """Stores registered users with salted password hashes."""

    def __init__(self, file_path="data/users.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self._write_users([])

    def _read_users(self):
        try:
            content = self.file_path.read_text(encoding="utf-8").strip()
            users = json.loads(content) if content else []

            # Validate that user data is stored as a list.
            if not isinstance(users, list):
                raise ValueError("User data must contain a list.")

            # Validate that every user record is a dictionary.
            if not all(isinstance(user, dict) for user in users):
                raise ValueError(
                    "Each user record must be a JSON object."
                )

            return users

        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(
                f"Unable to read {self.file_path}: {exc}. "
                "Check the JSON file."
            ) from exc

    def _write_users(self, users):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.write_text(
            json.dumps(users, indent=4),
            encoding="utf-8"
        )

    def find_user(self, username):
        return next(
            (
                user for user in self._read_users()
                if user.get("username", "").lower() == username.lower()
            ),
            None,
        )

    def add_user(self, user_record):
        users = self._read_users()

        if any(
            user.get("username", "").lower()
            == user_record["username"].lower()
            for user in users
        ):
            raise ValueError("That username already exists.")

        users.append(user_record)
        self._write_users(users)
