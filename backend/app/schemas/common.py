from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, PlainSerializer

from app.db.money import format_amount, quantize

# Money in API payloads: Decimal internally, always serialized as a "1234.56" string.
Money = Annotated[
    Decimal,
    BeforeValidator(quantize),
    PlainSerializer(format_amount, return_type=str, when_used="always"),
]


class ErrorOut(BaseModel):
    detail: str
    code: str | None = None
