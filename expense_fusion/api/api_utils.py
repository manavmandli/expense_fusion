import frappe
from frappe import _


def remove_default_fields(data):
    default_fields = {
        "user",
        "owner",
        "creation",
        "modified",
        "modified_by",
        "docstatus",
        "idx",
        "doctype",
        "links",
        "_user_tags",
        "_comments",
        "_assign",
        "_liked_by",
    }
    # Remove default fields
    if isinstance(data, list):
        for doc in data:
            for field in default_fields:
                doc.pop(field, None)
    elif isinstance(data, dict):
        for field in default_fields:
            data.pop(field, None)
    return data
