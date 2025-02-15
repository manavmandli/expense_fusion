from pydantic import BaseModel
from typing import List, Optional


class UserModel(BaseModel):
    name: str
    email: str
    mobile_no: str
    password: str


class SpaceModel(BaseModel):
    name: str
    new_name: Optional[str] = None


class AccountModel(BaseModel):
    name: Optional[str] = None
    new_name: Optional[str] = None
    space: Optional[str] = None
    amount: Optional[int] = None


class IncomeModel(BaseModel):
    income_id: Optional[str] = None
    account: Optional[str] = None
    date: Optional[str] = None
    amount: Optional[int] = None
    write_note: Optional[str] = None


class ExpenseModel(BaseModel):
    expense_id: Optional[str] = None
    account: Optional[str] = None
    date: Optional[str] = None
    amount: Optional[int] = None
    write_note: Optional[str] = None


class TransactionModel(BaseModel):
    space_filter: Optional[str] = None
    duration_filter: Optional[str] = None
