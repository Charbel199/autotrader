from dependency_injector import containers, providers
from app.data_access.repositories.interfaces.abstract_user_repository import AbstractUserRepository
from app.data_access.repositories.user_repository import UserRepository
from app.data_access.repositories.interfaces.abstract_bot_repository import AbstractBotRepository
from app.data_access.repositories.bot_repository import BotRepository


class Repositories(containers.DeclarativeContainer):
    user_repository = providers.Singleton(AbstractUserRepository.register(UserRepository))
    bot_repository = providers.Singleton(AbstractBotRepository.register(BotRepository))
