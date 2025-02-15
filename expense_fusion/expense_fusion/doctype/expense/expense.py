# Copyright (c) 2024, Manav and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from frappe.model.document import Document


class Expense(Document):
    def after_insert(self):
        self.update_account(update=True)

    def on_trash(self):
        self.update_account(update=False)

    def update_account(self, update):
        if update:
            account_doc = frappe.get_doc("Expense Account", self.account)
            account_doc.amount = flt(account_doc.amount) - flt(self.amount)
            account_doc.save()
        else:
            account_doc = frappe.get_doc("Expense Account", self.account)
            account_doc.amount = flt(account_doc.amount) + flt(self.amount)
            account_doc.save()
