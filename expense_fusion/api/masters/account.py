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
        if frappe.db.exists(
            "Expense Account",
            {"owner": frappe.session.user, "account_name": data.name},
        ):
            frappe.response["message"] = (
                f"{data.name} Already exists please enter unique name"
            )
            return
        account_doc = frappe.get_doc(
            dict(
                doctype="Expense Account",
                account_name=data.name,
                amount=data.amount,
                owner=frappe.session.user,
            )
        )
        account_doc.insert(ignore_permissions=True)
        frappe.response["message"] = f"{account_doc.name} Account created successfully"

    def update_account(self, data: AccountModel):
        if frappe.db.exists(
            "Expense Account",
            {"owner": frappe.session.user, "account_name": data.new_name},
        ):
            frappe.response["message"] = (
                f"{data.new_name} Already exists please enter unique name"
            )
            return
        account_doc = frappe.get_doc("Expense Account", {"account_name": data.name})
        account_doc.account_name = data.new_name
        account_doc.amount = data.amount
        account_doc.save(ignore_permissions=True)
        frappe.response["message"] = f"{account_doc.name} Account updated successfully"

    def delete_account(self, data: AccountModel):
        account_exists = frappe.db.exists(
            "Expense Account",
            {"owner": frappe.session.user, "account_name": data.name},
        )

        if not account_exists:
            frappe.response["message"] = "Please enter a valid account name."
            return

        frappe.delete_doc("Expense Account", account_exists, force=1)
        frappe.response["message"] = f"{data.name} account deleted successfully."
