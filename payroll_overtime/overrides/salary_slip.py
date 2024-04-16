import frappe
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip

class POSalarySlip(SalarySlip):
    @frappe.whitelist()
    def get_emp_and_working_day_details(self):
        super(POSalarySlip, self).get_emp_and_working_day_details()
        ovrs = frappe.get_list("Overtime Request", filters={
            "employee": self.employee,
            "date": ["between", [self.start_date, self.end_date]],
            "docstatus": 1,
            "is_earned": 0,
            "overtime_status": "Approved"
        }, fields=["name", "overtime_hours", "is_holiday"])
        total_holiday_hours = total_workday_hours = 0
        for ovr in ovrs:
            if ovr.is_holiday:
                total_holiday_hours += ovr.overtime_hours
            else:
                total_workday_hours += ovr.overtime_hours
            self.append("custom_salary_slip_overtime", {
                "overtime_request": ovr.name,
                "overtime_hours": ovr.overtime_hours,
                "is_holiday": ovr.is_holiday
            })
        self.total_overtime_hours_in_holidays = total_holiday_hours
        self.total_overtime_hours_in_workday = total_workday_hours

    def on_submit(self):
        super(POSalarySlip, self).on_submit()
        for sso in self.custom_salary_slip_overtime:
            frappe.db.set_value("Overtime Request", sso.overtime_request, "is_earned", 1)
    
    def on_cancel(self):
        super(POSalarySlip, self).on_cancel()
        for sso in self.custom_salary_slip_overtime:
            frappe.db.set_value("Overtime Request", sso.overtime_request, "is_earned", 0)
        