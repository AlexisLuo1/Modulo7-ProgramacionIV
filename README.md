# Biblioteca Personal

Aplicación web desarrollada con Flask para gestionar una biblioteca personal utilizando una base de datos SQLite. Las páginas HTML se generan con plantillas Jinja2 organizadas mediante herencia y componentes reutilizables.

## Requisitos

* Python 3.10 o superior
* Dependencias incluidas en `requirements.txt`

Instalación:

```
pip install -r requirements.txt
```

## Ejecución

Inicializa la base de datos y ejecuta la aplicación:

```
flask --app app run --debug
```

La aplicación estará disponible en:
**[http://localhost:5000](http://localhost:5000)**

## Funcionalidades

* Listado general de libros.
* Registro de nuevos libros.
* Edición y eliminación de libros.
* Búsqueda por título, autor o género.
* Mensajes de confirmación para acciones realizadas.

---

