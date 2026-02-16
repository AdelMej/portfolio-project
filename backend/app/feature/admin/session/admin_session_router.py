@router.get(
    "/admin/sessions/{coach_id}",
    response_model=list[GetOutputDto]
)
async def admin_get_sessions_by_coach(
    coach_id: UUID,
    actor: Actor = Depends(get_current_actor),
    UoW: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service),
):
    return await service.admin_list_sessions_by_coach(UoW, actor, coach_id)


@router.put(
    "/admin/sessions/{session_id}/cancel",
    status_code=status.HTTP_204_NO_CONTENT
)
async def admin_cancel_session(
    session_id: UUID,
    actor: Actor = Depends(get_current_actor),
    UoW: SessionUoWPort = Depends(get_session_uow),
    service: SessionService = Depends(get_session_service),
):
    await service.admin_cancel_session(UoW, actor, session_id)
