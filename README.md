[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=18163322)
# Uso di Template HTML in Flask

Flask consente di utilizzare template HTML per rendere dinamica la generazione del contenuto delle pagine web. I template HTML in Flask sono generalmente creati utilizzando il motore di template **Jinja2**, che offre funzionalità di rendering avanzate. Ecco una breve introduzione su come integrare template HTML in un'app Flask:

## Creazione del Template:

Inizia creando una directory chiamata `templates` nella stessa directory del tuo file Flask (per esempio, `app.py`). All'interno di questa directory, puoi creare i tuoi file HTML. Ad esempio, crea un file chiamato `index.html`:

1. **html**

```html
   <!DOCTYPE html> 
   <html lan="it"> 
   <head> 
     <meta charset="UTF-8">
     <title>Flask Template Example</title> 
   </head> 
   <body> 
     <h1>{{ message }}</h1>
   </body> 
   </html>
```

Nota l'uso della sintassi `{{ }}` - questa è la sintassi di **Jinja2** per incorporare variabili dinamiche all'interno del tuo HTML.

2. **python**

```python
from flask import Flask, render_template 

app = Flask(__name__) 

@app.route('/') 
def hello_world(): 
    return render_template('index.html', message='Hello, World!') 

if __name__ == '__main__': 
    app.run(debug=True)`
```

Qui, `render_template` è una funzione fornita da Flask che carica il template e passa variabili a esso. Nella nostra route '/', stiamo passando la variabile `message` al template.

3. **Esecuzione dell'applicazione:**

Esegui l'applicazione come prima (`python app.py`) e visita `http://localhost:5000` nel tuo browser. Ora dovresti vedere il contenuto del template HTML con il messaggio dinamico "Hello, World!".

### Variabili nei Template

Le variabili possono essere passate ai template per renderle dinamiche. Puoi passare variabili complesse come liste, dizionari, ecc. e utilizzarle nel tuo template. Ad esempio:

**python**

```python
@app.route('/') 
def hello_world(): 
    users = ['Alice', 'Bob', 'Charlie'] 
    return render_template('index.html', users=users)`
```

Nel tuo template HTML, puoi iterare attraverso la lista degli utenti:

**html**

```html
<!DOCTYPE html> 
<html lang="it">
  <head>
    <meta charset="UTF-8">
    <title>Flask Template Example</title> 
  </head> 
  <body> 
    <h1>Users:</h1> 
    <ul> 
    {% for user in users %} 
      <li>{{ user }}</li> 
    {% endfor %} 
    </ul> 
  </body>
</html>
```

Questa è solo un'introduzione, ma ti offre un punto di partenza per iniziare a creare applicazioni web dinamiche utilizzando Flask e template HTML.
