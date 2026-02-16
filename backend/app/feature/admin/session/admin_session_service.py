    async def admin_list_sessions_by_coach(
            self,
            uow: SessionUoWPort,
            actor: Actor,
            coach_id: UUID
    ):
        ensure_has_permission(actor, Permission.READ_USERS)

        sessions = await uow.session_repo.list_sessions(coach_id=coach_id)

        return [
            GetOutputDto(
                id=s.id,
                coach_id=s.coach_id,
                title=s.title,
                starts_at=s.starts_at,
                ends_at=s.ends_at,
                status=s.status
            )
            for s in sessions
        ]

    async def admin_cancel_session(
            self,
            uow: SessionUoWPort,
            actor: Actor,
            session_id: UUID
    ):
        # Ensure admin permission
        ensure_has_permission(actor, Permission.READ_USERS)

        session = await uow.session_repo.get_session_by_id(session_id)
        if not session:
            raise NotFoundError()

        await uow.session_repo.cancel_session(session_id)
