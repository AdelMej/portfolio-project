from uuid import UUID
from datetime import datetime, timedelta
import stripe
from app.domain.credit.credit_cause import CreditCause
from app.domain.credit.credit_entity import NewCreditEntity
from app.domain.credit.credit_exception import CreditNegativeError
from app.domain.payment.payment_exception import PaymentProviderError
from app.domain.payment_intent.payment_intent_entity import (
    NewPaymentIntentEntity
)
from app.domain.payment_intent.payment_intent_providers import PaymentProvier
from app.domain.session.session_creation_rules import (
    ensure_price_is_not_negative,
    ensure_times_valid,
    ensure_title_is_valid
)
from app.domain.session.session_exception import (
    AlreadyActiveParticipationError,
    InvalidAttendanceInputError,
    InvalidCoachAccountError,
    NoActiveParticipationFoundError,
    NotOwnerOfSessionError,
    OwnerCantRegisterToOwnSessionError,
    SessionAlreadyAttendedError,
    SessionAttendanceNotOpenError,
    SessionCancelledError,
    SessionClosedForRegistration,
    SessionIsFullError,
    SessionNotFoundError,
    SessionOverlappingError,
    SessionStartedError
)
from app.feature.session.session_dto import (
    AttendanceInputDTO,
    CoachPublicDto,
    GetOutputDto,
    SessionUpdateInputDTO,
    AttendanceOutputDto,
    SessionCreationInputDTO
)
from app.domain.auth.actor_entity import Actor
from app.domain.auth.permission_rules import ensure_has_permission
from app.domain.auth.permission import Permission
from app.feature.session.uow.session_public_uow_port import (
    SessionPulbicUoWPort
)
from app.feature.session.uow.session_uow_port import SessionUoWPort
from app.domain.session.session_entity import (
    NewSessionEntity,
    NewSessionParticipationEntity
)
from app.domain.currency.currency_rules import (
    ensure_currency_is_valid
)
from app.domain.auth.auth_exceptions import (
    AuthUserIsDisabledError
)
from app.shared.utils.time import utcnow


class SessionService:
    async def get_session(
            self,
            uow: SessionPulbicUoWPort,
            session_id: UUID
    ) -> GetOutputDto:
        if not await uow.session_read_repo.public_exists_session(session_id):
            raise SessionNotFoundError()

        session = await uow.session_read_repo.get_session_by_id(session_id)

        return GetOutputDto(
            id=session.id,
            coach=CoachPublicDto(
                id=session.coach.user_id,
                first_name=session.coach.first_name,
                last_name=session.coach.last_name
            ),
            title=session.title,
            starts_at=session.starts_at,
            ends_at=session.ends_at,
            price_cents=session.price_cents,
            currency=session.currency,
            status=session.status
        )

    async def create_session(
            self,
            uow: SessionUoWPort,
            actor: Actor,
            input: SessionCreationInputDTO
    ) -> None:
        ensure_has_permission(actor, Permission.CREATE_SESSION)

        # normalization
        title = input.title.strip()
        currency = input.currency.strip().upper()

        ensure_times_valid(input.starts_at, input.ends_at)
        ensure_price_is_not_negative(input.price_cents)
        ensure_title_is_valid(title)
        ensure_currency_is_valid(currency)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        if not await uow.coach_stripe_account_read_repo.is_coach_account_valid(
            actor.id
        ):
            raise InvalidCoachAccountError()

        if await uow.session_read_repo.is_session_overlapping(
            starts_at=input.starts_at,
            ends_at=input.ends_at
        ):
            raise SessionOverlappingError()

        new_session = NewSessionEntity(
            coach_id=actor.id,
            title=title,
            starts_at=input.starts_at,
            ends_at=input.ends_at,
            price_cents=input.price_cents,
            currency=currency
        )

        await uow.session_creation_repo.create_session(new_session)

    async def get_all_sessions(
        self,
        offset: int,
        limit: int,
        _from: datetime | None,
        to: datetime | None,
        uow: SessionPulbicUoWPort
    ) -> tuple[list[GetOutputDto], bool]:
        sessions, has_more = (
            await uow.session_read_repo.get_all_sessions(
                offset=offset,
                limit=limit,
                _from=_from,
                to=to,
            )
        )

        return [
            GetOutputDto(
                id=session.id,
                coach=CoachPublicDto(
                    id=session.coach.user_id,
                    first_name=session.coach.first_name,
                    last_name=session.coach.last_name
                ),
                title=session.title,
                starts_at=session.starts_at,
                ends_at=session.ends_at,
                price_cents=session.price_cents,
                currency=session.currency,
                status=session.status
            ) for session in sessions
        ], has_more

    async def cancel_session(
        self,
        uow: SessionUoWPort,
        actor: Actor,
        session_id: UUID
    ):
        ensure_has_permission(actor, Permission.CANCEL_SESSION)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        if not await uow.session_read_repo.exist_session(session_id):
            raise SessionNotFoundError()

        if await uow.session_read_repo.is_session_cancelled(session_id):
            raise SessionCancelledError()

        if not await uow.session_read_repo.is_session_owner(
            session_id,
            actor.id
        ):
            raise NotOwnerOfSessionError()

        if await uow.session_read_repo.is_session_started(
            session_id=session_id
        ):
            raise SessionStartedError()

        await uow.session_update_repo.cancel_session(session_id)

    async def get_attendance(
            self,
            uow: SessionUoWPort,
            actor: Actor,
            session_id: UUID
    ) -> list[AttendanceOutputDto]:
        ensure_has_permission(actor, Permission.READ_ATTENDANCE)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        if not await uow.session_read_repo.exist_session(session_id):
            raise SessionNotFoundError()

        if await uow.session_read_repo.is_session_cancelled(session_id):
            raise SessionCancelledError()

        if not await uow.session_read_repo.is_session_owner(
            session_id, actor.id
        ):
            raise NotOwnerOfSessionError()

        if not (
            await uow.session_attendance_read_repo.is_session_attendance_open(
                session_id
            )
        ):
            raise SessionAttendanceNotOpenError()

        if await uow.session_attendance_read_repo.is_session_attended(
            session_id
        ):
            raise SessionAlreadyAttendedError()

        profiles = await uow.session_attendance_read_repo.get_attendance(
            session_id
        )

        return [
            AttendanceOutputDto(
                user_id=profile.user_id,
                first_name=profile.first_name,
                last_name=profile.last_name
            ) for profile in profiles
        ]

    async def put_attendance(
        self,
        input: AttendanceInputDTO,
        uow: SessionUoWPort,
        actor: Actor,
        session_id: UUID
    ) -> None:
        ensure_has_permission(actor, Permission.CREATE_ATTENDANCE)
        attendance_map: dict[UUID, bool] = {
            dto.user_id: dto.attended
            for dto in input.attendance
        }

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        if not await uow.session_read_repo.exist_session(session_id):
            raise SessionNotFoundError()

        if await uow.session_read_repo.is_session_cancelled(session_id):
            raise SessionCancelledError()

        if not await uow.session_read_repo.is_session_owner(
            session_id, actor.id
        ):
            raise NotOwnerOfSessionError()

        if not await (
            uow.session_attendance_read_repo.is_session_attendance_open(
                session_id
            )
        ):
            raise SessionAttendanceNotOpenError()

        if await uow.session_attendance_read_repo.is_session_attended(
            session_id
        ):
            raise SessionAlreadyAttendedError()

        if not await (
            uow.session_attendance_read_repo.is_attendance_payload_valid(
                session_id=session_id,
                attendance_list=attendance_map
            )
        ):
            raise InvalidAttendanceInputError()

        await uow.session_attendance_creation_repo.create_attendance(
            session_id=session_id,
            attendance_list=attendance_map
        )

    async def update_session(
            self,
            uow: SessionUoWPort,
            actor: Actor,
            session_id: UUID,
            input: SessionUpdateInputDTO
    ):
        ensure_has_permission(actor, Permission.UPDATE_SESSION)

        # normalization
        title = input.title.strip()

        ensure_title_is_valid(title)
        ensure_times_valid(input.starts_at, input.ends_at)

        if not await uow.session_read_repo.exist_session(session_id):
            raise SessionNotFoundError()

        if not await uow.session_read_repo.is_session_owner(
            session_id=session_id,
            user_id=actor.id
        ):
            raise NotOwnerOfSessionError()

        if await uow.session_read_repo.is_session_overlapping_except(
            starts_at=input.starts_at,
            ends_at=input.ends_at,
            except_session_id=session_id
        ):
            raise SessionOverlappingError()

        await uow.session_update_repo.update_session(
            session_id=session_id,
            title=title,
            starts_at=input.starts_at,
            ends_at=input.ends_at
        )

    async def cancel_registration(
        self,
        uow: SessionUoWPort,
        actor: Actor,
        session_id: UUID
    ):
        ensure_has_permission(actor, Permission.CANCEL_REGISTRATION)

        if not await uow.session_read_repo.exist_session(session_id):
            raise SessionNotFoundError()

        if await uow.session_read_repo.is_session_cancelled(session_id):
            raise SessionCancelledError()

        if await uow.auth_read_repo.is_user_disabled(
            user_id=actor.id
        ):
            raise AuthUserIsDisabledError()

        if not (
            await uow.session_participation_read_repo.has_active_participation(
                session_id=session_id,
                user_id=actor.id
            )
        ):
            raise NoActiveParticipationFoundError()

        await uow.session_participation_update_repo.cancel_registration(
            session_id=session_id,
            user_id=actor.id
        )

    async def register_user(
        self,
        session_id: UUID,
        actor: Actor,
        uow: SessionUoWPort,
        session_ttl: int
    ) -> tuple[bool, str | None]:
        ensure_has_permission(actor, Permission.SESSION_REGISTRATION)

        if await uow.auth_read_repo.is_user_disabled(actor.id):
            raise AuthUserIsDisabledError()

        if await uow.session_read_repo.is_session_owner(
            session_id,
            actor.id
        ):
            raise OwnerCantRegisterToOwnSessionError()

        if not await uow.session_read_repo.exist_session(session_id):
            raise SessionNotFoundError()

        if await uow.session_read_repo.is_session_cancelled(session_id):
            raise SessionCancelledError()

        if await uow.session_participation_read_repo.has_active_participation(
            session_id,
            actor.id
        ):
            raise AlreadyActiveParticipationError()

        if await uow.session_participation_read_repo.is_session_full(
            session_id
        ):
            raise SessionIsFullError()

        if not await uow.session_participation_read_repo.is_registration_open(
            session_id
        ):
            raise SessionClosedForRegistration()

        session = await uow.session_read_repo.system_get_session_by_id(
            session_id
        )

        credit = (
            await uow.credit_ledger_read_repo.fetch_credit_by_user_id(
                user_id=actor.id,
                currency=session.currency
            )
        )

        credit_applied = min(credit, session.price_cents)

        final_amount = session.price_cents - credit_applied

        if final_amount < 0:
            raise CreditNegativeError()

        required_payment = final_amount > 0

        if final_amount == 0 and credit_applied == 0:
            client_secret = None

        elif final_amount == 0 and credit_applied > 0:
            await uow.credit_ledger_creation_repo.create_credit_entry(
                NewCreditEntity(
                    user_id=actor.id,
                    amount_cents=-credit_applied,
                    currency=session.currency,
                    cause=CreditCause.SESSION_USAGE,
                )
            )

            client_secret = None

        else:
            try:
                intent = await stripe.PaymentIntent.create_async(
                    amount=final_amount,
                    currency=session.currency,
                    automatic_payment_methods={"enabled": True},
                    metadata={
                        "resource": "session_registration",
                        "flow_version": "v1",

                        "session_id": str(session_id),
                        "user_id": str(actor.id),
                    },
                )
            except stripe.StripeError as exc:
                raise PaymentProviderError() from exc

            await uow.payment_intent_creation_repo.create_payment_intent(
                NewPaymentIntentEntity(
                    user_id=actor.id,
                    session_id=session.id,
                    provider=PaymentProvier.STRIPE,
                    provider_intent_id=intent.id,
                    status=intent.status,
                    credit_applied_cents=credit_applied,
                    amount_cents=final_amount,
                    currency=session.currency
                )
            )

            if intent.client_secret is None:
                raise PaymentProviderError()

            client_secret = intent.client_secret

        await uow.session_participation_creation_repo.create_participation(
            participation=NewSessionParticipationEntity(
                session_id=session_id,
                user_id=actor.id,
            ),
            expires_at=utcnow() + timedelta(seconds=session_ttl)
        )

        return required_payment, client_secret
