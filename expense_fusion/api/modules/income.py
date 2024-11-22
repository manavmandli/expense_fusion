import frappe
from frappe import _
from expense_fusion.api.models import IncomeModel


class Income:
    def create_income(self, data: IncomeModel):
        if not data.account:
            frappe.response["message"] = "The 'account name' field is required."
            return
        if not data.amount:
            frappe.response["message"] = "The 'amount' field is required."
            return

        income_doc = frappe.get_doc(
            dict(
                doctype="Income",
                account=data.account,
                date=data.date,
                amount=data.amount,
                write_note=data.write_note,
                owner=frappe.session.user,
            )
        )
        income_doc.insert(ignore_permissions=True)
        frappe.response["message"] = "Transaction created successfully"
        frappe.response["ID"] = f"{income_doc.name}"

    def update_income(self, data: IncomeModel):
        if not data.income_id:
            frappe.response["message"] = "The 'income_id' field is required."
            return
        income_doc = frappe.get_doc("Income", data.income_id)
        income_doc.account = data.account
        income_doc.date = data.date
        income_doc.amount = data.amount
        income_doc.write_note = data.write_note
        income_doc.save(ignore_permissions=True)
        frappe.response["message"] = "Transaction updated successfully"
        frappe.response["ID"] = f"{income_doc.name}"

    def delete_income(self, data: IncomeModel):
        if not data.income_id:
            frappe.response["message"] = "The 'income_id' field is required."
            return
        if not frappe.db.exists(
            "Income", {"owner": frappe.session.user, "name": data.income_id}
        ):
            frappe.response["message"] = "Please Enter valid Transaction id"
            return

        frappe.delete_doc("Income", data.income_id, force=1)
        frappe.response["message"] = "Transaction deleted successfully"
        frappe.response["ID"] = f"{data.income_id}"
