import functools
import frappe
from frappe.exceptions import AuthenticationError, ValidationError


class log(object):
    def __init__(self) -> None:
        pass

    def __call__(self, fn):

        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            try:
                user = frappe.session.user
                ip = frappe.local.request_ip
                function_name = fn.__name__
                module = fn.__module__

                # Execute the function
                result = fn(*args, **kwargs)

                # Save log to Doctype
                frappe.get_doc(
                    {
                        "doctype": "API Log",
                        "timestamp": frappe.utils.now(),
                        "user": user,
                        "ip": ip,
                        "function_name": function_name,
                        "module": module,
                        "arguments": str(args),
                        "kwarguments": str(kwargs),
                        "result": str(result),
                        "exception": "",
                        "http_status_code": 200,
                    }
                ).insert(ignore_permissions=True)

                return result
            except AuthenticationError as e:
                frappe.response["http_status_code"] = e.http_status_code
                frappe.response["message"] = "Unauthorize"

                # Save error log to Doctype
                frappe.get_doc(
                    {
                        "doctype": "API Log",
                        "timestamp": frappe.utils.now(),
                        "user": user,
                        "ip": ip,
                        "function_name": function_name,
                        "module": module,
                        "arguments": str(args),
                        "kwarguments": str(kwargs),
                        "result": "",
                        "exception": str(e),
                        "http_status_code": e.http_status_code,
                    }
                ).insert(ignore_permissions=True)

                return str(e)
            except ValidationError as e:
                frappe.response["http_status_code"] = e.http_status_code

                # Save error log to Doctype
                frappe.get_doc(
                    {
                        "doctype": "POS API Log",
                        "timestamp": frappe.utils.now(),
                        "user": user,
                        "ip": ip,
                        "function_name": function_name,
                        "module": module,
                        "arguments": str(args),
                        "kwarguments": str(kwargs),
                        "result": "",
                        "exception": str(e),
                        "http_status_code": e.http_status_code,
                    }
                ).insert(ignore_permissions=True)

                return str(e)
            except Exception as e:
                frappe.log_error(
                    title="Expense Tracker Error", message=frappe.get_traceback()
                )
                frappe.response["http_status_code"] = 500

                # Save error log to Doctype
                frappe.get_doc(
                    {
                        "doctype": "API Log",
                        "timestamp": frappe.utils.now(),
                        "user": user,
                        "ip": ip,
                        "function_name": function_name,
                        "module": module,
                        "arguments": str(args),
                        "kwarguments": str(kwargs),
                        "result": "",
                        "exception": str(e),
                        "http_status_code": 500,
                    }
                ).insert(ignore_permissions=True)

                return str(e)

        return decorated
