from datetime import datetime
from app.domain.auth.actor_entity import Actor
from app.domain.auth.auth_exceptions import (
    AdminCantSelfDeleteError,
    AuthUserIsDisabledError,
    EmailAlreadyExistError,
    PasswordMissmatchError,
    PasswordReuseError
)
from app.domain.auth.auth_password_rules import ensure_password_is_strong
from app.domain.auth.permission import Permission
from app.domain.auth.permission_rules import ensure_has_permission
from app.domain.user.user_profile_rules import (
    ensure_first_name_is_valid,
    ensure_last_name_is_valid
)
from app.feature.auth.auth_dto import GetMeOutputDTO
from app.feature.me.me_dto import (
    CoachDto,
    GetMeProfileOutputDTO,
    GetSessionOutputDto,
    MeEmailChangeInputDTO,
    MePasswordChangeInputDTO,
    ParticipationOutputDTO,
    UpdateMeProfileInputDTO
)
from app.feature.me.uow.me_system_uow_port import MeSystemUoWPort
from app.feature.me.uow.me_uow_port import MeUoWPort
from app.shared.security.password_hasher_port import PasswordHasherPort


class MeService:
    async def get_me(
        self,
        actor: Actor,
        uow: MeUoWPort,
    ) -> GetMeOutputDTO:

        ensure_has_permission(actor, Permission.READ_SELF)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        user = await uow.me_read_repo.get(actor.id)

        return GetMeOutputDTO(
            email=user.email,
            roles=user.roles
        )

    async def email_change_me(
        self,
        actor: Actor,
        uow: MeSystemUoWPort,
        input: MeEmailChangeInputDTO,
    ) -> None:
        ensure_has_permission(actor, Permission.UPDATE_SELF)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        # normalization
        email = input.email.strip().lower()

        if await uow.auth_read_repo.exist_email(email):
            raise EmailAlreadyExistError()

        await uow.me_update_repo.update_email_by_user_id(
            email,
            actor.id
        )

    async def password_change_me(
        self,
        input: MePasswordChangeInputDTO,
        password_hasher: PasswordHasherPort,
        actor: Actor,
        uow: MeSystemUoWPort
    ) -> None:
        ensure_has_permission(actor, Permission.UPDATE_SELF)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        # normalization
        old_password = input.old_password.strip()
        new_password = input.new_password.strip()

        ensure_password_is_strong(new_password)

        user = await uow.auth_read_repo.get_user_by_id(actor.id)

        if not password_hasher.verify(old_password, user.password_hash):
            raise PasswordMissmatchError()

        if password_hasher.verify(new_password, user.password_hash):
            raise PasswordReuseError()

        new_password_hash = password_hasher.hash(new_password)

        await uow.me_update_repo.update_password_by_id(
            user_id=actor.id,
            password_hash=new_password_hash
        )

    async def get_me_profile(
        self,
        actor: Actor,
        uow: MeUoWPort
    ) -> GetMeProfileOutputDTO:
        ensure_has_permission(actor, Permission.READ_SELF)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        profile = await uow.me_read_repo.get_profile_by_id(actor.id)

        return GetMeProfileOutputDTO(
            first_name=profile.first_name,
            last_name=profile.last_name
        )

    async def update_me_profile(
        self,
        input: UpdateMeProfileInputDTO,
        actor: Actor,
        uow: MeUoWPort
    ) -> None:
        ensure_has_permission(actor, Permission.UPDATE_SELF)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        # normalization
        first_name = input.first_name.strip()
        last_name = input.last_name.strip()

        ensure_first_name_is_valid(first_name)
        ensure_last_name_is_valid(last_name)

        await uow.me_update_repo.update_profile_by_id(
            user_id=actor.id,
            first_name=first_name,
            last_name=last_name
        )

    async def delete_me(
        self,
        actor: Actor,
        uow: MeSystemUoWPort,
    ) -> None:
        if Permission.NO_SELF_DELETE in actor.permissions:
            raise AdminCantSelfDeleteError()

        ensure_has_permission(actor, Permission.DELETE_SELF)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        await uow.me_delete_repo.soft_delete_user(
            user_id=actor.id,
        )

        await uow.auth_update_repo.revoke_all_refresh_token(
            user_id=actor.id
        )

    async def get_own_sessions(
        self,
        actor: Actor,
        uow: MeUoWPort,
        limit: int,
        offset: int,
        _from: datetime | None,
        to: datetime | None,
    ) -> tuple[list[GetSessionOutputDto], bool]:
        ensure_has_permission(actor, Permission.READ_SESSION)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        sessions, has_more = await (
            uow.session_read_repo.get_own_sessions(
                user_id=actor.id,
                limit=limit,
                offset=offset,
                _from=_from,
                to=to
            )
        )

        return [
            GetSessionOutputDto(
                id=session.id,
                coach=CoachDto(
                    first_name=session.coach.first_name,
                    last_name=session.coach.last_name
                ),
                title=session.title,
                starts_at=session.starts_at,
                ends_at=session.ends_at,
                price_cents=session.price_cents,
                currency=session.currency,
                status=session.status,
                participants=[
                   ParticipationOutputDTO(
                        first_name=participant.first_name,
                        last_name=participant.last_name
                    )for participant in session.participants
                ]
            ) for session in sessions
        ], has_more
