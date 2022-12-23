# Flask

Una vez que hemos podido ejecutar `flask run` podemos seguir modificando el proyecto.

## Crear una plantilla de HTML

`app.py`
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
```

`templates/index.html`
```html
<!DOCTYPE html>
<html>

<head>
	<title>Notas - Todo App</title>
</head>

    <body>
	<h1>Welcome To Notas</h1>
	<p>Notas es una app de todos</p>

    {% block body %}

    <p>This is a Flask application.</p>

    {% endblock %}

    </body>
</html>

```
## Añadimos hojas de estilo
- Bootstrap 5
- style.css
Dentro de etiqueta `<head>` del `index.html`:
```html
    <!-- Hoja de Bootstrap 5 -->
    <link rel="stylesheet"  type="text/css" href="{{url_for('.static', filename='bootstrap.min.css')}}">
    <!-- Hojas de estilo -->
    <link rel="stylesheet"  type="text/css" href="{{url_for('.static', filename='style.css')}}">
	<title>Notas - Todo App</title>
```

## Añadimos plantilla base.html

Objetivo: tener una plantilla base que se extienda a todas las demás plantillas e importar las secciones necesarias desde sus archivos html.

**base.html**
```html 
<!DOCTYPE html>
<head>
    <title>Notas - Todo App</title>
    <!-- Hoja de Bootstrap 5 -->
    <link rel="stylesheet"  type="text/css" href="{{url_for('.static', filename='bootstrap.min.css')}}">
    <!-- Hojas de estilo -->
    <link rel="stylesheet"  type="text/css" href="{{url_for('.static', filename='style.css')}}">
</head>
<html>
    <body>
    {% block home %}
    {% endblock %}
    </body>
    {% include 'footer.html' %}
</html>
```
**Notación:**
- `{{url_for('.static', filename='bootstrap.min.css')}}` -> `url_for` es una función de Flask que nos permite acceder a los archivos estáticos de la aplicación. En este caso, `bootstrap.min.css` está en la carpeta `static` de la aplicación.
- **extender** -> `{% extends 'base.html' %}` -> `extends` es una directiva de Jinja2 que nos permite extender una plantilla.
- **importar** -> `{% block home %}` -> `block` es una directiva de Jinja2 que nos permite definir un bloque de código que se puede extender en otras plantillas.
- **incluir:** -> `{% include 'footer.html' %}` -> `include` es una directiva de Jinja2 que nos permite incluir el contenido de un archivo html en otro.
**Estructura:**
```
├── app.py -> render_template("home.html")
├── /templates
        ├── base.html (plantilla que importa `block home` e incluye `footer.html`)
            `block home`
            ├── home.html (extiende `base.html`)
                ├── about.html (se incluye en home.html)
                ├── what_you_can_do.html (se incluye en home.html)
            `endblock`
            ├── footer.html (se incluye en base.html)
```

## Footer
Iconos:
    - [Font Awesome](https://fontawesome.com/)
    - [Flaticon](https://www.flaticon.com/) -> descargar PNG