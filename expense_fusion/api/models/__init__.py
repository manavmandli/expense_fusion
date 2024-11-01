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
    name: str
    new_name: str
    amount: Optional[str] = None


class IncomeModel(BaseModel):
    income_id: Optional[str] = None
    account = str
    date: Optional[str] = None
    amount = str
    write_note: Optional[str] = None


class ExpenseModel(BaseModel):
    expense_id: Optional[str] = None
    account = str
    date: Optional[str] = None
    amount = str
    write_note: Optional[str] = None