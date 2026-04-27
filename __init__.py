from trytond.pool import Pool

from . import company


def register():
    Pool.register(
        company.Employee,
        module='z _health_employee_custom', type_='model')
    Pool.register(
        company.EmployeeOrganigramaReport,
        module='z _health_employee_custom', type_='report')
