from .interfaces.abstract_user_repository import AbstractUserRepository
from app.core.entities import user
from app.data_access.persistence.database import Session
from app.application.models import user_model


class UserRepository(AbstractUserRepository):
    async def add_user(self, user_to_add: user.User) -> user.User:
        session = Session()
        session.add(user_to_add)
        session.commit()
        session.refresh(user_to_add)
        session.close()
        return user_to_add

    async def get_user_from_email(self, email: str) -> user.User:
        session = Session()
        user_from_db = session.query(user.User).filter(user.User.email == email).first()
        session.close()
        return user_from_db
