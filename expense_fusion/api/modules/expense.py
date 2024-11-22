import frappe
from frappe import _
from expense_fusion.api.models import ExpenseModel


class Expense:
    def create_expense(self, data: ExpenseModel):
        if not data.account:
            frappe.response["message"] = "The 'account name' field is required."
            return
        if not data.amount:
            frappe.response["message"] = "The 'amount' field is required."
            return
        expense_doc = frappe.get_doc(
            dict(
                doctype="Expense",
                account=data.account,
                date=data.date,
                amount=data.amount,
                write_note=data.write_note,
                owner=frappe.session.user,
            )
        )
        expense_doc.insert(ignore_permissions=True)
        frappe.response["message"] = "Transaction created successfully"
        frappe.response["ID"] = f"{expense_doc.name}"

    def update_expense(self, data: ExpenseModel):
        if not data.expense_id:
            frappe.response["message"] = "The 'expense_id' field is required."
            return
        expense_doc = frappe.get_doc("Expense", data.expense_id)
        expense_doc.account = data.account
        expense_doc.date = data.date
        expense_doc.amount = data.amount
        expense_doc.write_note = data.write_note
        expense_doc.save(ignore_permissions=True)
        frappe.response["message"] = "Transaction updated successfully"
        frappe.response["ID"] = f"{expense_doc.name}"

    def delete_expense(self, data: ExpenseModel):
        if not data.expense_id:
            frappe.response["message"] = "The 'expense_id' field is required."
            return
        if not frappe.db.exists(
            "Expense", {"owner": frappe.session.user, "name": data.expense_id}
        ):
            frappe.response["message"] = "Please Enter valid Transaction id"
            return

        frappe.delete_doc("Expense", data.expense_id, force=1)
        frappe.response["message"] = "Transaction deleted successfully"
        frappe.response["ID"] = f"{data.expense_id}"
