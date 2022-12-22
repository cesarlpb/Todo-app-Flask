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