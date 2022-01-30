from .interfaces.abstract_user_repository import AbstractUserRepository
from app.core.entities import user
from app.data_access.persistence.database import Session
from app.application.models import user_model


class UserRepository(AbstractUserRepository):
    async def add_user(self, user_data: user_model.UserCreate) -> user.User:
        session = Session()
        new_user = user.User(
            email=user_data.email,
            hashed_password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        session.close()
        return new_user

    async def get_user_from_email(self, email: str) -> user.User:
        session = Session()
        user_from_db = session.query(user.User).filter(user.User.email == email).first()
        session.close()
        return user_from_db
