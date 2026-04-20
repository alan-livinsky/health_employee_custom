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
    __name__ = 'health_employee_custom.employee_list'

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
        excluded_types = (
            fields.Binary,
            fields.Function,
            fields.One2Many,
            fields.Many2Many,
        )
        preferred = [
            'id',
            'rec_name',
            'party',
            'company',
            'supervisor',
            'cargo',
            'active',
        ]
        available = []
        for name, field in Employee._fields.items():
            if isinstance(field, excluded_types):
                continue
            available.append(name)

        ordered = [name for name in preferred if name in available]
        ordered.extend(sorted(name for name in available if name not in ordered))
        return ordered

    @staticmethod
    def _field_label(Employee, name):
        if name == 'id':
            return 'ID'
        if name == 'rec_name':
            return 'Nombre'
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
