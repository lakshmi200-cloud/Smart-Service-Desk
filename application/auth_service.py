import hashlib
import hmac
import os

from domain.exceptions import AuthenticationError


class AuthService:
    """Registers users and authenticates them using salted password hashes."""

    ITERATIONS = 200_000

    def __init__(self, user_repository):
        self.user_repository = user_repository

    @classmethod
    def _hash_password(cls, password, salt):
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, cls.ITERATIONS
        ).hex()

    def register(self, username, password, confirm_password):
        username = username.strip()
        if not username:
            raise AuthenticationError("Username cannot be empty.")
        if len(username) < 3:
            raise AuthenticationError("Username must contain at least 3 characters.")
        if not password:
            raise AuthenticationError("Password cannot be empty.")
        if len(password) < 8:
            raise AuthenticationError("Password must contain at least 8 characters.")
        if password != confirm_password:
            raise AuthenticationError("Passwords do not match.")
        if self.user_repository.find_user(username) is not None:
            raise AuthenticationError("That username already exists. Please choose another.")

        record = self.create_password_record(username, password)
        self.user_repository.add_user(record)
        return username

    def login(self, username, password):
        user = self.user_repository.find_user(username.strip())
        if user is None:
            raise AuthenticationError("Invalid username or password.")

        calculated_hash = self._hash_password(password, bytes.fromhex(user["salt"]))
        if not hmac.compare_digest(calculated_hash, user["password_hash"]):
            raise AuthenticationError("Invalid username or password.")
        return user["username"]

    @classmethod
    def create_password_record(cls, username, password):
        salt = os.urandom(16)
        return {
            "username": username,
            "salt": salt.hex(),
            "password_hash": cls._hash_password(password, salt),
        }
