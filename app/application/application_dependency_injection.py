from dependency_injector import containers, providers
from app.application.services.interfaces.abstract_user_service import AbstractUserService
from app.application.services.interfaces.abstract_token_service import AbstractTokenService
from app.application.services.interfaces.abstract_bot_service import AbstractBotService
from app.application.services.user_service import UserService
from app.application.services.token_service import TokenService
from app.application.services.bot_service import BotService
from app.data_access.data_access_dependency_injection import Repositories


class Services(containers.DeclarativeContainer):
    token_service = providers.Singleton(AbstractTokenService.register(TokenService))
    user_service = providers.Factory(AbstractUserService.register(UserService), user_repository=Repositories.user_repository, token_service=token_service)
    bot_service = providers.Factory(AbstractBotService.register(BotService),
                                    bot_repository=Repositories.bot_repository)
