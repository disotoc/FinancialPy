"""Paquete superior Financial py."""
# financial_py/__init__.py

__app_name__ = "financial_py"
__version__ = "0.0.1"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

ERRORS = {
    DIR_ERROR: "Error en el directorio de configuración",
    FILE_ERROR: "Error en el archivo de configuración",
    DB_READ_ERROR: "Error al leer la base de datos",
    DB_WRITE_ERROR: "Error al escribir en la base de datos",
    ID_ERROR: "Error de id de registro",
}