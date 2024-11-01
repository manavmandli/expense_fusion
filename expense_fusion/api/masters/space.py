import frappe
from frappe import _
from expense_fusion.api.api_utils import remove_default_fields
from expense_fusion.api.models import SpaceModel


class Space:
    def get_space(self):
        spaces = remove_default_fields(
            frappe.get_all(
                "Expense Space", filters={"owner": frappe.session.user}, fields=["*"]
            )
        )
        frappe.response["message"] = "Space list retrieved successfully"
        return spaces

    def create_space(self, data: SpaceModel):
        space_doc = frappe.get_doc(
            dict(
                doctype="Expense Space",
                space_name=data.name,
                owner=frappe.session.user,
            )
        )
        space_doc.insert(ignore_permissions=True)
        frappe.response["message"] = f"{space_doc.name} Space created successfully"

    def update_space(self, data: SpaceModel):
        space_doc = frappe.get_doc("Expense Space", data.name)
        current_user = frappe.session.user
        frappe.set_user("Administrator")
        frappe.rename_doc(
            "Expense Space", data.name, data.new_name, force=True, ignore_if_exists=True
        )
        frappe.set_user(current_user)
        frappe.db.commit()
        frappe.response["message"] = f"{space_doc.name} Space updated successfully"

    def delete_space(self, data: SpaceModel):
        if not frappe.db.exists(
            "Expense Space",
            filter={"owner": frappe.session.user, "space_name": data.name},
        ):
            frappe.response["message"] = "Please Enter valid space name"
            return

        frappe.delete_doc("Expense Space", data.name, force=1)
        frappe.response["message"] = f"{data.name} Space deleted successfully"
