from fastapi import FastAPI
from .auth_exception_handler import register_exception_handler as auth_handler
from .common_exception_handler import (
    register_exception_handler as common_handler
)
from .credit_exception_handler import (
    register_exception_handler as credit_handler
)
from .currency_exception_handler import (
    register_exception_handler as currency_exception_handler
)
from .payment_exception_handler import (
    register_exception_handler as payment_exception_handler
)
from .payment_intent_exception_handler import (
    register_exception_handler as payment_intent_exception_handler
)
from .session_exception_handler import (
    register_exception_handler as session_exception_handler
)
from .stripe_exception_handler import (
    register_exception_handler as stripe_exception_handler
)


def register_exception_handlers(app: FastAPI):
    auth_handler(app)
    common_handler(app)
    credit_handler(app)
    currency_exception_handler(app)
    payment_exception_handler(app)
    payment_intent_exception_handler(app)
    session_exception_handler(app)
    stripe_exception_handler(app)
