
from datetime import datetime
from app.domain.auth.actor_entity import Actor
from app.feature.payment.uow.payment_uow_port import PaymentUoW


class PaymentService():
    async def get_payments(
        limit: int,
        offset: int,
        _from: datetime,
        to: datetime,
        uow: PaymentUoW,
        actor: Actor,
    ) -> 
