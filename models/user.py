# ==============================================================================
# AUTHOR: Kim Sorng (Group 2, Gen 6)
# MODULE: User & Authentication Models
# DESCRIPTION: Contains User class representing staff members with role-based
#              access control (Admin/Manager, Cashier, Waiter).
# ==============================================================================

import hashlib


class User:
    """Class representing a restaurant staff member."""

    ROLE_ADMIN = "Admin"
    ROLE_CASHIER = "Cashier"
    ROLE_WAITER = "Waiter"
    VALID_ROLES = [ROLE_ADMIN, ROLE_CASHIER, ROLE_WAITER]

    def __init__(
        self,
        user_id: int,
        username: str,
        password_hash: str,
        role: str = ROLE_CASHIER,
        full_name: str = "",
        is_active: bool = True
    ):
        if user_id <= 0:
            raise ValueError("User ID must be a positive integer.")
        if not username.strip():
            raise ValueError("Username cannot be empty.")
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role '{role}'. Must be one of: {', '.join(self.VALID_ROLES)}")

        self.user_id = user_id
        self.username = username.strip().lower()
        self.password_hash = password_hash
        self.role = role
        self.full_name = full_name.strip() or username.capitalize()
        self.is_active = is_active

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """Hashes a plain password using SHA-256."""
        return hashlib.sha256(plain_password.encode("utf-8")).hexdigest()

    def verify_password(self, plain_password: str) -> bool:
        """Verifies if the provided plain password matches the stored hash."""
        return self.password_hash == self.hash_password(plain_password)

    def get_details(self) -> str:
        """Returns formatted string details of the staff member."""
        status = "Active" if self.is_active else "Inactive"
        return f"[{self.user_id:03d}] {self.full_name} (@{self.username}) | Role: {self.role} | Status: {status}"

    def to_dict(self) -> dict:
        """Converts User object to dictionary for JSON persistence."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role,
            "full_name": self.full_name,
            "is_active": self.is_active
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Instantiates a User object from serialized dictionary data."""
        return cls(
            user_id=data["user_id"],
            username=data["username"],
            password_hash=data["password_hash"],
            role=data.get("role", cls.ROLE_CASHIER),
            full_name=data.get("full_name", ""),
            is_active=data.get("is_active", True)
        )

