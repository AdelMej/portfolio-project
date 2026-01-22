from app.domain.session.session_exception import (SessionCreditNegativeError)

def ensure_price_is_not_negative(price:int) -> None:
    if price < 0:
        raise SessionCreditNegativeError
