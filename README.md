# z_health_employee_custom

Módulo personalizado para **Tryton 6.0** que extiende el modelo `company.employee` con un campo de cargo y una acción de exportación CSV.

---

## Descripción general

Este módulo amplía el modelo estándar de empleados de Tryton agregando:

- Un campo **Cargo** visible en la vista formulario (antes del supervisor) y en la vista lista (después del nombre del tercero).
- Un acceso de reporte **"Descargar lista de empleados"** disponible en el menú lateral de **Empresa > Reportes**, que genera un archivo CSV con todos los registros.

El módulo se instala como paquete Python y se registra automáticamente en Tryton mediante el mecanismo de *entry points*, sin necesidad de copiar archivos manualmente.

---

## Estructura del proyecto

```
z_health_employee_custom/
├── __init__.py          # Registro de modelos y reportes en el Pool de Tryton
├── company.py           # Extensión del modelo Employee y clase del reporte CSV
├── company.xml          # Definición de vistas, reporte y menús
├── tryton.cfg           # Configuración del módulo (versión y dependencias)
├── report.txt           # Plantilla vacía requerida por la acción de reporte
├── setup.py             # Configuración de empaquetado con setuptools
├── pyproject.toml       # Backend de construcción (setuptools)
├── MANIFEST.in          # Archivos extra incluidos en el paquete
└── view/
    ├── employee_form.xml # XPath que agrega el campo cargo en el formulario
    └── employee_tree.xml # XPath que agrega el campo cargo en la lista
```

---

## Funcionalidades

### Campo Cargo (`cargo`)

- **Tipo:** `fields.Char`
- **Etiqueta:** `Cargo`
- **Modelo:** `company.employee`
- **Vista formulario:** aparece antes del campo `supervisor`.
- **Vista lista:** aparece después del campo `party` (nombre del empleado).

### Reporte: Descargar lista de empleados

- **Nombre interno:** `z_health_employee.employee_list`
- **Formato de salida:** CSV codificado en UTF-8 con BOM (`utf-8-sig`) para compatibilidad con Excel.
- **Nombre del archivo descargado:** `lista_empleados.csv`
- **Acceso:** menú lateral en **Empresa > Reportes > Descargar lista de empleados**.
- **Campos exportados** (en el orden definido en `EXPORT_FIELDS`):

| Campo        | Descripción                                      |
|--------------|--------------------------------------------------|
| `party`      | Nombre del tercero vinculado al empleado         |
| `cargo`      | Cargo laboral del empleado                       |
| `company`    | Empresa a la que pertenece                       |
| `supervisor` | Supervisor directo                               |
| `start_date` | Fecha de inicio del contrato                     |
| `end_date`   | Fecha de fin del contrato                        |

Los campos relacionales (`party`, `company`, `supervisor`) se exportan usando su `rec_name` (nombre de visualización). Si un campo no existe en el modelo, se omite automáticamente.

---

## Dependencias

| Componente          | Versión requerida |
|---------------------|-------------------|
| Python              | >= 3.10           |
| trytond             | >= 6.0, < 6.1     |
| trytond_company     | >= 6.0, < 6.1     |

Módulo Tryton requerido (declarado en `tryton.cfg`): `company`.

---

## Instalación

### Instalación estándar

Desde el directorio raíz del módulo, con el entorno virtual de Python 3.10 activado:

```bash
python -m pip install .
```

### Instalación en modo editable (desarrollo)

Permite editar el código sin reinstalar:

```bash
python -m pip install -e .
```

---

## Activación en Tryton

### 1. Actualizar la base de datos

Ejecutar como administrador de Tryton (reemplazar `<base_de_datos>` con el nombre real):

```bash
trytond-admin -d <base_de_datos> -u z_health_employee
```

Esto aplica los cambios de esquema y registra las vistas y acciones definidas en `company.xml`.

### 2. Reiniciar el servidor

```bash
# Ejemplo con systemd
systemctl restart trytond

# O directamente
trytond -c /etc/trytond.conf
```

---

## Notas técnicas

- El módulo usa `PoolMeta` para extender `company.employee` de forma no destructiva, compatible con otros módulos que también extiendan el mismo modelo.
- El reporte no usa una plantilla Genshi real; `report.txt` es un archivo vacío requerido por el sistema. La generación del CSV ocurre completamente en Python dentro del método `execute`.
- La codificación `utf-8-sig` (UTF-8 con BOM) permite que Excel abra el CSV correctamente sin configuración adicional.
- El entry point `trytond.modules` definido en `setup.py` hace que Tryton descubra el módulo automáticamente al iniciar, sin necesidad de copiarlo a la carpeta de módulos del servidor.
