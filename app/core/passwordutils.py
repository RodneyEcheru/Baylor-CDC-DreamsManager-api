from argon2 import PasswordHasher


class PasswordUtils:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash the provided password using argon2"""
        hashed_password = PasswordHasher().hash(password)
        return hashed_password

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify the provided password against the hashed password"""
        try:
            valid_password = PasswordHasher().verify(hashed_password, password)
            return valid_password
        except Exception as e:
            return False
