from datetime import datetime
from fastapi import APIRouter, Query
from fastapi import Depends

from app.domain.auth.actor_entity import Actor
from app.feature.admin.payment.admin_payment_dependencies import (
    get_admin_payment_service
)
from app.feature.admin.payment.admin_payment_dto import (
    PaginatedPaymentOutputDTO
)
from app.feature.admin.payment.admin_payment_service import AdminPaymentService
from app.feature.admin.payment.uow.admin_payment_uow_port import (
    AdminPaymentUoWPort
)
from app.infrastructure.persistence.sqlalchemy.provider import get_payment_uow
from app.infrastructure.security.provider import get_current_actor

router = APIRouter(
    prefix="/admin/payment",
    tags=["admin-payment"]
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
    uow: AdminPaymentUoWPort = Depends(get_payment_uow),
    actor: Actor = Depends(get_current_actor),
    service: AdminPaymentService = Depends(get_admin_payment_service)
) -> PaginatedPaymentOutputDTO:
    items, has_more = await service.get_payments(
        limit=limit,
        offset=offset,
        _from=_from,
        to=to,
        uow=uow,
        actor=actor
    )

    return PaginatedPaymentOutputDTO(
        items=items,
        limit=limit,
        offset=offset,
        has_more=has_more
    )
