import csv
import io

from trytond.model import ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.report import Report


class Employee(metaclass=PoolMeta):
    __name__ = 'company.employee'

    cargo = fields.Char(
        'Cargo',
        help='Labor or job title for the employee.')

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls._buttons.update({
                'download_organigrama': {},
                })

    @classmethod
    @ModelView.button_action(
        'health_employee_custom.report_employee_organigrama')
    def download_organigrama(cls, employees):
        pass


class EmployeeOrganigramaReport(Report):
    __name__ = 'health_employee_custom.employee_organigrama'

    @classmethod
    def execute(cls, ids, data):
        pool = Pool()
        Employee = pool.get('company.employee')

        employees = Employee.browse(ids)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
                'Nivel',
                'Empleado',
                'Cargo',
                'Empresa',
                'Supervisor',
                ])

        seen = set()
        for employee in employees:
            cls._append_employee_rows(writer, employee, 0, seen)

        content = output.getvalue().encode('utf-8-sig')
        report_name = cls._report_name(employees)
        return 'csv', content, False, report_name

    @classmethod
    def _append_employee_rows(cls, writer, employee, level, seen):
        if employee.id in seen:
            return
        seen.add(employee.id)
        writer.writerow([
                level,
                employee.rec_name or '',
                employee.cargo or '',
                employee.company.rec_name if employee.company else '',
                employee.supervisor.rec_name if employee.supervisor else '',
                ])

        subordinates = sorted(
            employee.subordinates or [],
            key=lambda subordinate: subordinate.rec_name or '')
        for subordinate in subordinates:
            cls._append_employee_rows(writer, subordinate, level + 1, seen)

    @staticmethod
    def _report_name(employees):
        if not employees:
            return 'organigrama_empleados'
        if len(employees) == 1:
            base_name = employees[0].rec_name or 'empleado'
            return 'organigrama_%s' % base_name.replace(' ', '_')
        return 'organigrama_empleados'
