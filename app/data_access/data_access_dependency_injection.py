from dependency_injector import containers, providers


class Repositories(containers.DeclarativeContainer):
    data_loader_repository = providers.Singleton(AbstractUserRepository.register(UserRepository))

