from app.domain.session.session_status import SessionStatus


class SessionCreditNeg(Exception):
    def __init__(self, message="Session credit negative"):
        self.message = message
        super().__init__(self.message)
