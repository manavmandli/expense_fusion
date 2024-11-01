import frappe
from frappe import _
from expense_fusion.api.models import IncomeModel


class Income:
    def create_income(self, data: IncomeModel):
        income_doc = frappe.get_doc(
            dict(
                doctype="Income",
                account=data.account,
                space=data.space,
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
        income_doc = frappe.get_doc("Income", data.income_id)
        income_doc.account = data.account
        income_doc.space = data.space
        income_doc.date = data.date
        income_doc.amount = data.amount
        income_doc.write_note = data.write_note
        income_doc.save(ignore_permissions=True)
        frappe.response["message"] = "Transaction updated successfully"
        frappe.response["ID"] = f"{income_doc.name}"

    def delete_income(self, data: IncomeModel):
        if not frappe.db.exists(
            "Income", filter={"owner": frappe.session.user, "name": data.income_id}
        ):
            frappe.response["message"] = "Please Enter valid Transaction id"
            return

        frappe.delete_doc("Income", data.income_id, force=1)
        frappe.response["message"] = "Transaction deleted successfully"
        frappe.response["ID"] = f"{data.income_id}"
