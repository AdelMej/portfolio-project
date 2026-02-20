from datetime import datetime
from fastapi import APIRouter, Depends, Query
from app.domain.auth.actor_entity import Actor
from app.feature.admin.credit.admin_credit_dependencies import (
    get_admin_credit_service
)
from app.feature.admin.credit.admin_credit_dto import PaginatedCreditOutputDTO
from app.feature.admin.credit.admin_credit_service import AdminCreditService
from app.feature.admin.credit.uow.admin_credit_uow_port import (
    AdminCreditUoWPort
)
from app.infrastructure.persistence.sqlalchemy.provider import get_credit_uow
from app.infrastructure.security.provider import get_current_actor

router = APIRouter(
    prefix="/admin/credit",
    tags=["admin-credit"]
)


@router.get(
    path="/",
    status_code=200
)
async def get_credit(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    _from: datetime | None = Query(None),
    to: datetime | None = Query(None),
    uow: AdminCreditUoWPort = Depends(get_credit_uow),
    actor: Actor = Depends(get_current_actor),
    service: AdminCreditService = Depends(get_admin_credit_service)
) -> PaginatedCreditOutputDTO:
    items, has_more = await service.get_all_credits(
        limit=limit,
        offset=offset,
        to=to,
        _from=_from,
        uow=uow,
        actor=actor
    )

    return PaginatedCreditOutputDTO(
        items=items,
        limit=limit,
        offset=offset,
        has_more=has_more
    )
