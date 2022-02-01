from dependency_injector import containers, providers
from app.application.services.interfaces.abstract_user_service import AbstractUserService
from app.application.services.interfaces.abstract_token_service import AbstractTokenService
from app.application.services.interfaces.abstract_bot_service import AbstractBotService
from app.application.services.interfaces.abstract_exchange_service import AbstractExchangeService
from app.application.services.interfaces.abstract_bot_instance_service import AbstractBotInstanceService
from app.application.services.interfaces.abstract_exchange_instance_service import AbstractExchangeInstanceService
from app.application.services.user_service import UserService
from app.application.services.token_service import TokenService
from app.application.services.bot_service import BotService
from app.application.services.exchange_service import ExchangeService
from app.application.services.exchange_instance_service import ExchangeInstanceService
from app.application.services.bot_instance_service import BotInstanceService
from app.data_access.data_access_dependency_injection import Repositories


class Services(containers.DeclarativeContainer):
    token_service = providers.Singleton(AbstractTokenService.register(TokenService))
    user_service = providers.Factory(AbstractUserService.register(UserService), user_repository=Repositories.user_repository, token_service=token_service)
    bot_service = providers.Factory(AbstractBotService.register(BotService),
                                    bot_repository=Repositories.bot_repository)
    exchange_service = providers.Factory(AbstractExchangeService.register(ExchangeService),
                                         exchange_repository=Repositories.exchange_repository)
    bot_instance_service = providers.Factory(AbstractBotInstanceService.register(BotInstanceService),
                                             bot_instance_repository=Repositories.bot_instance_repository)
    exchange_instance_service = providers.Factory(AbstractExchangeInstanceService.register(ExchangeInstanceService),
                                                  exchange_instance_repository=Repositories.exchange_instance_repository)
