from .interfaces.abstract_exchange_instance_service import AbstractExchangeInstanceService
from app.application.models import user_model
from app.application.models import exchange_instance_model
from app.data_access.repositories.interfaces.abstract_exchange_instance_repository import AbstractExchangeInstanceRepository
from typing import List
from app.core.entities.exchange_instance import ExchangeInstance


class ExchangeInstanceService(AbstractExchangeInstanceService):

    def __init__(self, exchange_instance_repository: AbstractExchangeInstanceRepository):
        self.exchange_instance_repository = exchange_instance_repository

    async def get_exchange_instances(self, current_user: user_model.UserToken) -> List[exchange_instance_model.ExchangeInstance]:
        exchange_instances = await self.exchange_instance_repository.get_exchange_instances(current_user.id)
        exchange_instances_to_return = [exchange_instance_model.ExchangeInstance.from_orm(exchange_instance) for exchange_instance in exchange_instances]
        return exchange_instances_to_return

    async def add_exchange_instance(self, current_user: user_model.UserToken,
                                    exchange_instance: exchange_instance_model.ExchangeInstanceCreate) -> exchange_instance_model.ExchangeInstanceCreateResponse:
        exchange_instance_to_add = ExchangeInstance(**dict(exchange_instance))
        exchange_instance_to_add.user_id = current_user.id
        exchange_instance_from_db = await self.exchange_instance_repository.add_exchange_instance(current_user.id, exchange_instance_to_add)
        exchange_instance_added = exchange_instance_model.ExchangeInstanceCreateResponse.from_orm(exchange_instance_from_db)
        return exchange_instance_added

    async def remove_exchange_instance(self, current_user: user_model.UserToken, exchange_instance_id: int) -> exchange_instance_model.ExchangeInstance:
        exchange_instance_from_db = await self.exchange_instance_repository.get_exchange_instance(current_user.id, exchange_instance_id)
        exchange_instance_removed = await self.exchange_instance_repository.add_exchange_instance(current_user.id, exchange_instance_from_db)
        exchange_instance_removed_response = exchange_instance_model.ExchangeInstance.from_orm(exchange_instance_removed)
        return exchange_instance_removed_response

    async def get_exchange_instance(self, current_user: user_model.UserToken, exchange_instance_id: int) -> exchange_instance_model.ExchangeInstance:
        exchange_instance_from_db = await self.exchange_instance_repository.get_exchange_instance(current_user.id, exchange_instance_id)
        exchange_instance = exchange_instance_model.ExchangeInstance.from_orm(exchange_instance_from_db)
        return exchange_instance
