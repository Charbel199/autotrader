from dependency_injector import containers, providers
from app.data_access.repositories.interfaces.abstract_user_repository import AbstractUserRepository
from app.data_access.repositories.user_repository import UserRepository
from app.data_access.repositories.interfaces.abstract_bot_repository import AbstractBotRepository
from app.data_access.repositories.bot_repository import BotRepository
from app.data_access.repositories.interfaces.abstract_exchange_repository import AbstractExchangeRepository
from app.data_access.repositories.exchange_repository import ExchangeRepository
from app.data_access.repositories.interfaces.abstract_exchange_instance_repository import AbstractExchangeInstanceRepository
from app.data_access.repositories.exchange_instance_repository import ExchangeInstanceRepository
from app.data_access.repositories.interfaces.abstract_bot_instance_repository import AbstractBotInstanceRepository
from app.data_access.repositories.bot_instance_repository import BotInstanceRepository


class Repositories(containers.DeclarativeContainer):
    user_repository = providers.Singleton(AbstractUserRepository.register(UserRepository))
    bot_repository = providers.Singleton(AbstractBotRepository.register(BotRepository))
    exchange_repository = providers.Singleton(AbstractExchangeRepository.register(ExchangeRepository))
    exchange_instance_repository = providers.Singleton(AbstractExchangeInstanceRepository.register(ExchangeInstanceRepository))
    bot_instance_repository = providers.Singleton(AbstractBotInstanceRepository.register(BotInstanceRepository))
