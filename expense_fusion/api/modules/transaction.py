import frappe
from frappe import _
from datetime import datetime, timedelta
from expense_fusion.api.api_utils import remove_default_fields
from expense_fusion.api.models import TransactionModel


class Transaction:
    def get_transactions(self, data: TransactionModel):
        filters = {}
        filters["owner"] = frappe.session.user
        if data.space_filter:
            filters["space"] = data.space_filter
        if data.duration_filter:
            today = datetime.now()
            if data.duration_filter == "Today":
                start_date = today
                end_date = today
            elif data.duration_filter == "1 Week":
                start_date = today - timedelta(weeks=1)
                end_date = today
            elif data.duration_filter == "1 Month":
                start_date = today - timedelta(days=30)
                end_date = today
            elif data.duration_filter == "6 Months":
                start_date = today - timedelta(days=180)
                end_date = today
            elif data.duration_filter == "1 Year":
                start_date = today - timedelta(days=365)
                end_date = today
            else:
                start_date = end_date = None

            if start_date and end_date:
                filters["date"] = ["between", start_date, end_date]

        expense_records = remove_default_fields(
            frappe.get_all("Expense", filters=filters, fields=["*"])
        )
        income_records = remove_default_fields(
            frappe.get_all("Income", filters=filters, fields=["*"])
        )

        transactions = {
            "expenses_transaction": expense_records,
            "income_transaction": income_records,
        }

        frappe.response["message"] = "Transaction list get successfully"
        return transactions
