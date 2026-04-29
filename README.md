# z_health_employee

Módulo personalizado de Tryton 6.0 para extender `company.employee`.

## Funcionalidades

- Agrega un campo `Cargo` en los empleados.
- Agrega una acción de reporte llamada `Descargar lista de empleados`.
- Descarga un CSV con todos los registros de empleados y sus datos directos.

## Instalación local con pip

Desde un entorno de Python 3.10, instalar el módulo desde este directorio:

```bash
python -m pip install .
```

Para desarrollo local en modo editable:

```bash
python -m pip install -e .
```

## Activar o actualizar

1. Actualizar la base de datos:

   ```bash
   trytond-admin -d <database> -u z_health_employee
   ```

2. Reiniciar `trytond`.

## Notas

- El CSV se genera a partir de todos los registros de `company.employee`.
- Exporta los campos directos del empleado y renderiza relaciones como empresa,
  tercero y supervisor usando sus nombres de visualización.
- La instalación expone el módulo a través del entry point `trytond.modules`,
  por lo que no es necesario copiarlo manualmente a la carpeta de módulos.
