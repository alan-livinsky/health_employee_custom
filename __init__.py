from trytond.pool import Pool

from . import company


def register():
    Pool.register(
        company.Employee,
        module='health_employee_custom', type_='model')
    Pool.register(
        company.EmployeeOrganigramaReport,
        module='health_employee_custom', type_='report')
