# ==============================================================================
# AUTHOR: Kim Sorng (Group 2, Gen 6)
# MODULE: Authentication & Session Manager
# DESCRIPTION: Manages staff authentication, password verification, active
#              user session, and persistent user credentials.
# ==============================================================================

import json
import os
from typing import Optional, List
from models.user import User

USER_FILE = "data/user_data.json"


def get_default_users() -> List[User]:
    """Generates default staff accounts for initial system deployment."""
    return [
        User(
            user_id=1,
            username="admin",
            password_hash=User.hash_password("admin123"),
            role=User.ROLE_ADMIN,
            full_name="Kim Sorng (Admin)"
        ),
        User(
            user_id=2,
            username="cashier",
            password_hash=User.hash_password("cashier123"),
            role=User.ROLE_CASHIER,
            full_name="Ra Daro (Cashier)"
        ),
        User(
            user_id=3,
            username="waiter",
            password_hash=User.hash_password("waiter123"),
            role=User.ROLE_WAITER,
            full_name="Sokha (Waiter)"
        ),
    ]


def save_users_to_file(user_list: List[User]) -> bool:
    """Saves user list to JSON persistence file."""
    try:
        os.makedirs("data", exist_ok=True)
        data = [u.to_dict() for u in user_list]
        with open(USER_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[Error] Failed to save user data: {e}")
        return False


def load_users_from_file() -> List[User]:
    """Loads users from JSON file, initializing defaults if file is missing."""
    if not os.path.exists(USER_FILE):
        defaults = get_default_users()
        save_users_to_file(defaults)
        return defaults

    try:
        with open(USER_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [User.from_dict(item) for item in data]
    except Exception as e:
        print(f"[Warning] Failed to load users ({e}). Falling back to defaults.")
        return get_default_users()


class AuthManager:
    """Manages staff authentication and current session state."""

    def __init__(self, users_list: Optional[List[User]] = None):
        self.users: List[User] = users_list if users_list is not None else load_users_from_file()
        self.current_user: Optional[User] = None

    def authenticate(self, username: str, plain_password: str) -> Optional[User]:
        """Validates credentials against active staff records."""
        clean_user = username.strip().lower()
        for user in self.users:
            if user.username == clean_user and user.is_active:
                if user.verify_password(plain_password):
                    self.current_user = user
                    return user
        return None

    def logout(self):
        """Clears the active session."""
        self.current_user = None

    def is_authenticated(self) -> bool:
        """Returns True if a staff member is currently logged in."""
        return self.current_user is not None

    def render_login_screen(self, max_attempts: int = 3) -> Optional[User]:
        """Displays the CLI login screen and prompts staff for credentials."""
        print("\n" + "=" * 55)
        print("   🔐 RESTAURANT POS SYSTEM - STAFF LOGIN SCREEN   ")
        print("=" * 55)
        print("  Default test credentials:")
        print("   • Admin:   admin   / admin123")
        print("   • Cashier: cashier / cashier123")
        print("   • Waiter:  waiter  / waiter123")
        print("-" * 55)

        attempts = 0
        while attempts < max_attempts:
            try:
                username = input("Enter Username: ").strip()
                if not username:
                    print("⚠️ Username cannot be blank. Please try again.\n")
                    continue

                password = input("Enter Password: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nLogin cancelled.")
                return None

            user = self.authenticate(username, password)
            if user:
                print("\n✅ Login Successful!")
                print(f"Welcome, {user.full_name} | Role: [{user.role}]")
                print("=" * 55 + "\n")
                return user

            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"❌ Invalid credentials. {remaining} attempt(s) remaining.\n")
            else:
                print("⛔ Maximum login attempts exceeded. Access locked.\n")

        return None

