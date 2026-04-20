from core.security import verify_password, hash_password, generate_reset_token, get_token_expiry
from datetime import datetime

class AuthService:

    def change_password(self, db, user, current_password, new_password):
        if not verify_password(current_password, user.password):
            raise ValueError("Current password is incorrect")

        user.password = hash_password(new_password)
        db.commit()

    def forgot_password(self, db, email, user_repo):
        user = user_repo.get_by_email(db, email)

        if not user:
            return None

        token = generate_reset_token()
        expiry = get_token_expiry()

        user_repo.save_reset_token(db, user, token, expiry)

        # Return token (for testing only)
        return token

    def reset_password(self, db, token, new_password, user_repo):
        user = user_repo.get_by_token(db, token)

        if not user:
            raise ValueError("Invalid token")

        if user.reset_token_expiry < datetime.utcnow():
            raise ValueError("Token expired")

        user.password = hash_password(new_password)
        user_repo.clear_reset_token(db, user)