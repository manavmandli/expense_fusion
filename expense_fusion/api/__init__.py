import frappe
from expense_fusion.api.auth import Auth
from expense_fusion.api.masters import Space, Account
from expense_fusion.api.modules import log, Income, Expense, Transaction
from expense_fusion.api.models import (
    UserModel,
    SpaceModel,
    AccountModel,
    IncomeModel,
    ExpenseModel,
    TransactionModel,
)
from bs4 import BeautifulSoup


endpoints = {
    # Auth End Points
    "login": {"methods": {"POST"}, "function": Auth().login, "allow_guest": True},
    "signup": {
        "methods": {"POST"},
        "function": Auth().create_account,
        "model": UserModel,
        "allow_guest": True,
    },
    "logout": {"methods": {"POST"}, "function": Auth().logout, "allow_guest": False},
    # space End Points
    "get_space": {
        "methods": {"GET"},
        "function": Space().get_space,
        "allow_guest": False,
    },
    "create_space": {
        "methods": {"POST"},
        "function": Space().create_space,
        "model": SpaceModel,
        "allow_guest": False,
    },
    "update_space": {
        "methods": {"PUT"},
        "function": Space().update_space,
        "model": SpaceModel,
        "allow_guest": False,
    },
    "delete_space": {
        "methods": {"DELETE"},
        "function": Space().delete_space,
        "model": SpaceModel,
        "allow_guest": False,
    },
    # account End Points
    "get_account": {
        "methods": {"GET"},
        "function": Account().get_account,
        "allow_guest": False,
    },
    "create_account": {
        "methods": {"POST"},
        "function": Account().create_account,
        "model": AccountModel,
        "allow_guest": False,
    },
    "update_account": {
        "methods": {"PUT"},
        "function": Account().update_account,
        "model": AccountModel,
        "allow_guest": False,
    },
    "delete_account": {
        "methods": {"DELETE"},
        "function": Account().delete_account,
        "model": AccountModel,
        "allow_guest": False,
    },
    # Income End Points
    "create_income": {
        "methods": {"POST"},
        "function": Income().create_income,
        "model": IncomeModel,
        "allow_guest": False,
    },
    "update_income": {
        "methods": {"PUT"},
        "function": Income().update_income,
        "model": IncomeModel,
        "allow_guest": False,
    },
    "delete_income": {
        "methods": {"DELETE"},
        "function": Income().delete_income,
        "model": IncomeModel,
        "allow_guest": False,
    },
    # Expense End Points
    "create_expense": {
        "methods": {"POST"},
        "function": Expense().create_expense,
        "model": ExpenseModel,
        "allow_guest": False,
    },
    "update_expense": {
        "methods": {"PUT"},
        "function": Expense().update_expense,
        "model": ExpenseModel,
        "allow_guest": False,
    },
    "delete_expense": {
        "methods": {"DELETE"},
        "function": Expense().delete_expense,
        "model": ExpenseModel,
        "allow_guest": False,
    },
    # Transaction End Points
    "get_transactions": {
        "methods": {"GET"},
        "function": Transaction().get_transactions,
        "model": TransactionModel,
        "allow_guest": False,
    },
}


def get_allow_guest(type: str):
    endpoint = endpoints.get(type)
    return endpoint.get("allow_guest", False) if endpoint else False


@frappe.whitelist(methods=["POST", "GET", "PUT", "DELETE"], allow_guest=True)
@log()
def v1(type: str, data: dict | None = None, **kwargs):
    """
    data param is for POST and should be converted to Pydantic Model
    """
    endpoint = endpoints.get(type)

    if not endpoint:
        gen_response(404, "Endpoint not found.")
        return

    if frappe.request.method not in endpoint["methods"]:
        gen_response(405, "Method not allowed.")
        return

    allow_guest = get_allow_guest(type)
    if not allow_guest and frappe.session.user == "Guest":
        gen_response(403, "Guest access not allowed for this endpoint.")
        return

    if not data:
        data = dict()

    model = endpoint.get("model")
    if model:
        data = model(**data)

    try:
        if frappe.request.method == "POST":
            frappe.db.begin()

        if not model:
            result = endpoint["function"](**data)
        else:
            result = endpoint["function"](data)

        if frappe.request.method == "POST":
            frappe.db.commit()
    except frappe.AuthenticationError:
        return gen_response(500, frappe.response["message"])
    except Exception as e:
        frappe.log_error(title="Expense Tracker Error", message=frappe.get_traceback())
        result = str(e)
        return gen_response(500, result)
    finally:
        if frappe.request.method == "POST":
            frappe.db.close()

    gen_response(
        200,
        frappe.response["message"],
        result,
    )
    return


def gen_response(status, message, data=None):
    frappe.response["http_status_code"] = status
    if status == 500:
        frappe.response["message"] = BeautifulSoup(str(message),features="lxml").get_text()
    else:
        frappe.response["message"] = message
    if data is not None:
        frappe.response["data"] = data
