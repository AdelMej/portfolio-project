from datetime import datetime
from fastapi import APIRouter, Query
from fastapi.params import Depends

from app.domain.auth.actor_entity import Actor
from app.feature.payment.payment_dependencies import get_payment_service
from app.feature.payment.payment_service import PaymentService
from app.feature.payment.uow.payment_uow_port import PaymentUoW
from app.infrastructure.security.provider import get_current_actor

router = APIRouter(
    prefix="/payment",
    tags=["payment"]
)


@router.get(
    path="/",
    status_code=200
)
async def get_own_payment(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    _from: datetime | None = Query(None),
    to: datetime | None = Query(None),
    uow: PaymentUoW,
    actor: Actor = Depends(get_current_actor),
    service: PaymentService = Depends(get_payment_service)
) :
    pass
