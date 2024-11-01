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
        current_user = frappe.session.user
        frappe.set_user("Administrator")
        account_doc = frappe.get_doc("Expense Account", data.name)
        if data.amount is not None:
            account_doc.amount = data.amount

        if data.new_name:
            frappe.rename_doc(
                "Expense Account",
                data.name,
                data.new_name,
                force=True,
                ignore_if_exists=True,
            )
            frappe.set_user(current_user)
        account_doc.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.response["message"] = f"{account_doc.name} Account updated successfully"

    def delete_account(self, data: AccountModel):
        if not frappe.db.exists(
            "Expense Account",
            filter={"owner": frappe.session.user, "account_name": data.name},
        ):
            frappe.response["message"] = "Please Enter valid account name"
            return

        frappe.delete_doc("Expense Account", data.name, force=1)
        frappe.response["message"] = f"{data.name} Account deleted successfully"
