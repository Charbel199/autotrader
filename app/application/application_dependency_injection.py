from dependency_injector import containers, providers
from app.application.services.interfaces.abstract_user_service import AbstractUserService
from app.application.services.interfaces.abstract_authentication_service import AbstractAuthenticationService
from app.application.services.interfaces.abstract_token_service import AbstractTokenService
from app.application.services.user_service import UserService
from app.application.services.authentication_service import AuthenticationService
from app.application.services.token_service import TokenService
from app.data_access.data_access_dependency_injection import Repositories


class Services(containers.DeclarativeContainer):
    user_service = providers.Factory(AbstractUserService.register(UserService), user_repository=Repositories.user_repository)
    token_service = providers.Singleton(AbstractTokenService.register(TokenService))


class Managers(containers.DeclarativeContainer):
    authentication_manager = providers.Factory(AbstractAuthenticationService.register(AuthenticationService),
                                               user_service=Services.user_service,
                                               token_service=Services.token_service)
