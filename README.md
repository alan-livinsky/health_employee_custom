# health_employee_custom

Custom Tryton 6.0 module to extend `company.employee`.

## Features

- Adds a `Cargo` field on employees.
- Adds a model report action called `Descargar lista de empleados`.
- Downloads a CSV with all employee records and their direct data.

## Module structure

Copy the `health_employee_custom` directory into your Tryton modules path.

## Activate or update

1. Add the module path to your `trytond.conf` if needed.
2. Update the database:

   ```bash
   trytond-admin -d <database> -u health_employee_custom
   ```

3. Restart `trytond`.

## Notes

- The CSV is generated from all `company.employee` records.
- It exports direct employee fields and renders relations like company,
  party and supervisor using their display names.
