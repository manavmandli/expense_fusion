import frappe
from frappe import _
from expense_fusion.api.api_utils import remove_default_fields
from expense_fusion.api.models import AccountModel


class Account:
    def get_account(self):
        accounts = remove_default_fields(
            frappe.get_all(
                "Expense Account", filters={"owner": frappe.session.user}, fields=["*"]
            )
        )
        frappe.response["message"] = "Account list retrieved successfully"
        return accounts

    def create_account(self, data: AccountModel):
        if not data.name:
            frappe.response["message"] = "The 'account name' field is required."
            return
        if not data.space:
            frappe.response["message"] = "The 'space' field is required."
            return
        if data.amount is None:
            frappe.response["message"] = "The 'amount' field is required."
            return

        if frappe.db.exists(
            "Expense Account",
            {
                "owner": frappe.session.user,
                "account_name": data.name,
                "space": data.space,
            },
        ):
            frappe.response["message"] = (
                f"{data.name} Already exists please enter unique name or add in another space"
            )
            return
        account_doc = frappe.get_doc(
            dict(
                doctype="Expense Account",
                account_name=data.name,
                space=data.space,
                amount=data.amount,
                owner=frappe.session.user,
            )
        )
        account_doc.insert(ignore_permissions=True)
        frappe.response["message"] = f"{account_doc.name} Account created successfully"

    def update_account(self, data: AccountModel):
        if frappe.db.exists(
            "Expense Account",
            {
                "owner": frappe.session.user,
                "account_name": data.new_name,
                "space": data.space,
            },
        ):
            frappe.response["message"] = (
                f"{data.new_name} Already exists please enter unique name or add in another space"
            )
            return
        account_doc = frappe.get_doc(
            "Expense Account", {"account_name": data.name, "space": data.space}
        )
        account_doc.account_name = data.new_name
        account_doc.space = data.space
        account_doc.amount = data.amount
        account_doc.save(ignore_permissions=True)
        frappe.response["message"] = f"{account_doc.name} Account updated successfully"

    def delete_account(self, data: AccountModel):
        if not data.name:
            frappe.response["message"] = "The 'account name' field is required."
            return
        if not data.space:
            frappe.response["message"] = "The 'space' field is required."
            return
        account_name = frappe.db.get_value(
            "Expense Account",
            {
                "owner": frappe.session.user,
                "account_name": data.name,
                "space": data.space,
            },
            "name",
        )

        if not account_name:
            frappe.response["message"] = (
                f"Account does not exist in the space '{data.space}'."
            )
            return

        account_doc = frappe.get_doc("Expense Account", account_name)
        frappe.delete_doc("Expense Account", account_doc.name, force=1)
        frappe.response["message"] = f"'{data.name}' account deleted successfully."
