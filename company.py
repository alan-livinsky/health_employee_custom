import csv
import io

from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.report import Report


class Employee(metaclass=PoolMeta):
    __name__ = 'company.employee'

    cargo = fields.Char(
        'Cargo',
        help='Labor or job title for the employee.')


class EmployeeOrganigramaReport(Report):
    __name__ = 'z_health_employee.employee_list'
    EXPORT_FIELDS = [
        'party',
        'cargo',
        'company',
        'supervisor',
        'start_date',
        'end_date',
    ]

    @classmethod
    def execute(cls, ids, data):
        pool = Pool()
        Employee = pool.get('company.employee')

        employees = Employee.search([], order=[('id', 'ASC')])
        output = io.StringIO()
        writer = csv.writer(output)
        field_names = cls._exportable_field_names(Employee)
        writer.writerow([cls._field_label(Employee, name) for name in field_names])

        for employee in employees:
            writer.writerow([
                    cls._field_value(employee, name) for name in field_names
                    ])

        content = output.getvalue().encode('utf-8-sig')
        return 'csv', content, False, 'lista_empleados'

    @classmethod
    def _exportable_field_names(cls, Employee):
        return [name for name in cls.EXPORT_FIELDS if name in Employee._fields]

    @staticmethod
    def _field_label(Employee, name):
        field = Employee._fields[name]
        return field.string or name

    @staticmethod
    def _field_value(employee, name):
        value = getattr(employee, name, None)
        if value is None:
            return ''
        if hasattr(value, 'rec_name'):
            return value.rec_name or ''
        if isinstance(value, bool):
            return 'Si' if value else 'No'
        return value
