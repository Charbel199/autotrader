from .interfaces.abstract_user_repository import AbstractUserRepository
from app.data_access.persistence.models import user
from app.data_access.persistence.database import Session


class UserRepository(AbstractUserRepository):
    async def get_user_from_email(self, email: str) -> user.User:
        session = Session()
        user_from_db = session.query(user.User).filter(user.User.email == email).first()
        session.close()
        return user_from_db
