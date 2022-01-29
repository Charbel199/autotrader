from dependency_injector import containers, providers
from app.data_access.repositories.interfaces.abstract_user_repository import AbstractUserRepository
from app.data_access.repositories.user_repository import UserRepository


class Repositories(containers.DeclarativeContainer):
    user_repository = providers.Singleton(AbstractUserRepository.register(UserRepository))
