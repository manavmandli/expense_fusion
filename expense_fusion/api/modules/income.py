import frappe
from frappe import _
from expense_fusion.api.models import IncomeModel


class Income:
    def __init__(self) -> None:
        self.user = frappe.session.user

    def create_income(self, data: IncomeModel):
        income_doc = frappe.get_doc(
            dict(
                doctype="Income",
                account=data.account,
                date=data.date,
                amount=data.amount,
                write_note=data.write_note,
                owner=self.user,
            )
        )
        income_doc.insert(ignore_permissions=True)
        frappe.response["message"] = f"{income_doc.name} Income created successfully"

    def update_income(self, data: IncomeModel):
        income_doc = frappe.get_doc("Income", data.income_id)
        income_doc.account = data.account
        income_doc.date = data.date
        income_doc.amount = data.amount
        income_doc.write_note = data.write_note
        income_doc.save(ignore_permissions=True)
        frappe.response["message"] = f"{income_doc.name} Income updated successfully"

    def delete_income(self, data: IncomeModel):
        if not frappe.db.exists(
            "Income", filter={"owner": self.user, "name": data.income_id}
        ):
            frappe.response["message"] = "Please Enter valid income id"
            return

        frappe.delete_doc("Income", data.income_id, force=1)
        frappe.response["message"] = f"{data.income_id} Income deleted successfully"
