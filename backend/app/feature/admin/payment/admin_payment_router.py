from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Query
from fastapi import Depends

from app.domain.auth.actor_entity import Actor
from app.feature.admin.payment.admin_payment_dependencies import (
    get_admin_payment_service
)
from app.feature.admin.payment.admin_payment_dto import (
    PaginatedCoachPaymentOutputDTO,
    PaginatedPaymentOutputDTO
)
from app.feature.admin.payment.admin_payment_service import AdminPaymentService
from app.feature.admin.payment.uow.admin_payment_uow_port import (
    AdminPaymentUoWPort
)
from app.infrastructure.persistence.sqlalchemy.provider import (
    get_admin_payment_uow
)
from app.infrastructure.security.provider import get_current_actor

router = APIRouter(
    prefix="/admin/payment",
    tags=["admin-payment"]
)


@router.get(
    path="/",
    status_code=200
)
async def get_all_payments(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    _from: datetime | None = Query(None),
    to: datetime | None = Query(None),
    uow: AdminPaymentUoWPort = Depends(get_admin_payment_uow),
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


@router.get(
    path="/users/{user_id}",
    status_code=200
)
async def get_user_payment(
    user_id: UUID,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    _from: datetime | None = Query(None),
    to: datetime | None = Query(None),
    uow: AdminPaymentUoWPort = Depends(get_admin_payment_uow),
    actor: Actor = Depends(get_current_actor),
    service: AdminPaymentService = Depends(get_admin_payment_service)
) -> PaginatedPaymentOutputDTO:
    items, has_more = await service.get_user_payments(
        limit=limit,
        offset=offset,
        _from=_from,
        to=to,
        uow=uow,
        actor=actor,
        user_id=user_id
    )

    return PaginatedPaymentOutputDTO(
        items=items,
        limit=limit,
        offset=offset,
        has_more=has_more
    )


@router.get(
    path="/coach/{coach_id}",
    status_code=200
)
async def get_coach_payment(
    coach_id: UUID,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    _from: datetime | None = Query(None),
    to: datetime | None = Query(None),
    uow: AdminPaymentUoWPort = Depends(get_admin_payment_uow),
    actor: Actor = Depends(get_current_actor),
    service: AdminPaymentService = Depends(get_admin_payment_service)
) -> PaginatedCoachPaymentOutputDTO:
    items, has_more = await service.get_coach_payments(
        limit=limit,
        offset=offset,
        _from=_from,
        to=to,
        uow=uow,
        actor=actor,
        coach_id=coach_id
    )

    return PaginatedCoachPaymentOutputDTO(
        items=items,
        limit=limit,
        offset=offset,
        has_more=has_more
    )
