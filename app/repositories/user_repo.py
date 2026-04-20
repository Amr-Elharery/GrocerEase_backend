from models.user import User

class UserRepository:

    def get_by_email(self, db, email):
        return db.query(User).filter(User.email == email).first()

    def get_by_token(self, db, token):
        return db.query(User).filter(User.reset_token == token).first()

    def update_password(self, db, user, hashed_password):
        user.password = hashed_password
        db.commit()

    def save_reset_token(self, db, user, token, expiry):
        user.reset_token = token
        user.reset_token_expiry = expiry
        db.commit()

    def clear_reset_token(self, db, user):
        user.reset_token = None
        user.reset_token_expiry = None
        db.commit()