from flask import Flask, render_template
from forms.forms import LoginForm
app = Flask(__name__)
app.config ["SECRET_KEY"]="MY SECRET KEY"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/clientes/')
def clientes():
    return render_template ('clientes.html')

@app.route('/credit/')
def credit():
    return render_template ('credito.html')

@app.route('/contact/')
def contact():
    return render_template ('contacto.html')
@app.route('/sesion/')
def sesion():
    form = LoginForm()
    return render_template ('sesion.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)