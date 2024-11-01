import frappe
from frappe import _
from expense_fusion.api.models import ExpenseModel


class Expense:
    def __init__(self) -> None:
        self.user = frappe.session.user

    def create_expense(self, data: ExpenseModel):
        expense_doc = frappe.get_doc(
            dict(
                doctype="Expense",
                account=data.account,
                date=data.date,
                amount=data.amount,
                write_note=data.write_note,
                owner=self.user,
            )
        )
        expense_doc.insert(ignore_permissions=True)
        frappe.response["message"] = f"{expense_doc.name} Expense created successfully"

    def update_expense(self, data: ExpenseModel):
        expense_doc = frappe.get_doc("Expense", data.expense_id)
        expense_doc.account = data.account
        expense_doc.date = data.date
        expense_doc.amount = data.amount
        expense_doc.write_note = data.write_note
        expense_doc.save(ignore_permissions=True)
        frappe.response["message"] = f"{expense_doc.name} Expense updated successfully"

    def delete_expense(self, data: ExpenseModel):
        if not frappe.db.exists(
            "Expense", filter={"owner": self.user, "name": data.expense_id}
        ):
            frappe.response["message"] = "Please Enter valid expense id"
            return

        frappe.delete_doc("Expense", data.expense_id, force=1)
        frappe.response["message"] = f"{data.expense_id} Expense deleted successfully"
