# z_health_employee_custom

Custom Tryton 6.0 module to extend `company.employee`.

## Features

- Adds a `Cargo` field on employees.
- Adds a model report action called `Descargar lista de empleados`.
- Downloads a CSV with all employee records and their direct data.

## Local pip install

From a Python 3.10 environment, install the module from this directory:

```bash
python -m pip install .
```

For editable local development:

```bash
python -m pip install -e .
```

## Activate or update

1. Update the database:

   ```bash
   trytond-admin -d <database> -u z_health_employee_custom
   ```

2. Restart `trytond`.

## Notes

- The CSV is generated from all `company.employee` records.
- It exports direct employee fields and renders relations like company,
  party and supervisor using their display names.
- The install exposes the module through the `trytond.modules` entry point,
  so you do not need to copy it manually into a modules path.
