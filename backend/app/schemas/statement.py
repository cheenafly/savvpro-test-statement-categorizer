import datetime as dt
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.brain.models import AccountType, TxnStatus
from app.schemas.common import Money


class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    statement_id: int
    row_index: int
    date: dt.date
    description_raw: str
    merchant_key: str
    amount: Money
    category_id: str
    suggested_category_id: str | None
    confidence: float
    status: TxnStatus
    reasons: list[str]
    rule_id: str | None
    flags: list[str]
    is_pending: bool
    linked_transaction_id: int | None
    updated_at: dt.datetime


class StatementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    account_type: AccountType
    uploaded_at: dt.datetime
    row_count: int
    parse_errors: list[dict[str, Any]]
