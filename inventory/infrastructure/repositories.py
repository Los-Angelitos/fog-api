from inventory.infrastructure.models import Supply as SupplyModel, SupplyRequest as SupplyRequestModel
from inventory.domain.entities import Supply, SupplyRequest


class SupplyRepository:
    def save(self, supply):
        record = SupplyModel.create(
            provider_id=supply.provider_id,
            name=supply.name,
            price=supply.price,
            stock=supply.stock,
            state=supply.state
        )
        return Supply(
            supply.provider_id,
            supply.name,
            supply.price,
            supply.stock,
            supply.state,
            record.id
        )

    def find_by_id(self, supply_id):
        try:
            record = SupplyModel.get(SupplyModel.id == supply_id)
            return Supply(
                record.provider_id,
                record.name,
                float(record.price),
                record.stock,
                record.state,
                record.id
            )
        except SupplyModel.DoesNotExist:
            return None


class SupplyRequestRepository:
    def save(self, supply_request):
        record = SupplyRequestModel.create(
            payment_owner_id=supply_request.payment_owner_id,
            supply_id=supply_request.supply_id,
            count=supply_request.count,
            amount=supply_request.amount
        )
        return SupplyRequest(
            supply_request.payment_owner_id,
            supply_request.supply_id,
            supply_request.count,
            supply_request.amount,
            record.id
        )