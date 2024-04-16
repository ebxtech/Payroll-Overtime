# Copyright (c) 2024, EBX Technolgies and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import time_diff_in_seconds, flt
from frappe.model.document import Document
from erpnext.setup.doctype.employee.employee import is_holiday


class OvertimeRequest(Document):
	def validate(self):
		self.set_holiday()
		self.validate_existance()
	
	def on_submit(self):
		if self.overtime_status == "Draft":
			frappe.throw(_("Overtime Status Can Not Be Draft"))

	@frappe.whitelist()
	def get_difference(self):
		precession = self.precision("overtime_hours")
		if self.till_time and self.from_time:
			return flt(time_diff_in_seconds(self.till_time, self.from_time )/3600, precession)
		return 0
	
	def set_holiday(self):
		self.is_holiday = is_holiday(self.employee, self.date)

	def validate_existance(self):
		if frappe.db.exists({
			"doctype": self.doctype,
			"employee": self.employee,
			"date": self.date,
			"name": ["!=", self.name]
		}):
			frappe.throw(_("Cannot Create More Than One Overtime Request For Same Employee and Same Date"))

