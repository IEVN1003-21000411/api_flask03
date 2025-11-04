from flask import Flask, render_template, request
import forms
import math

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello world!"

@app.route('/index')
def index():
    #Tipos de variables que puede manejar para que pueda recibir
    titulo = "IENV1003"
    listado = ["Opera1","Opera2","Opera3","Opera4"]
    #Cuado nosotros definismo calores pode recibir parametos en la pagina
    return render_template('index.html', titulo = titulo, list = listado)#Estamos mandado hablar al index desde las importacion de render_template

@app.route('/operaciones', methods=['GET','POST'])
def operaciones():
    resultado = None
    if request.method == 'POST':
        X1 = request.form.get('n1')
        x2 = request.form.get('n2')
        resultado=X1 + x2
    return render_template('operas.html', result = resultado)

@app.route('/distancia')
def distancia():
    return render_template('distancia.html')

@app.route('/alumnos', methods=['GET','POST'])
def alumnos():
    #Vinculamos los parametros del html a la calse alumnos_calses
    mat = 0
    nom = ""
    ape = ""
    em = ""
    alumnos_clase = forms.UserForm(request.form)
    if request.method == 'POST' and alumnos_clase.validate():#Mandamos los datos del html a from.py
        mat= alumnos_clase.matricula.data
        nom = alumnos_clase.nombre.data
        ape=alumnos_clase.apellido.data
        em=alumnos_clase.correo.data
    return render_template('Alumnos.html', form = alumnos_clase, mat = mat, nom = nom, ape= ape, em = em)

@app.route('/figura', methods=['GET','POST'])
def figura():
    area = None
    figura_forms = forms.FigurasForm(request.form)
    if request.method == 'POST' and figura_forms.validate():
        fig = figura_forms.figura.data
        base = altura = 0
    #Si es rectangulos o trangulos la base y la altura va ser flotante o o
        if fig in ['rect', 'tri']:
            try:
                base = float(figura_forms.base.data or 0)
            except ValueError:
                base = 0
            try:
                altura = float(figura_forms.altura.data or 0)
            except ValueError:
                altura = 0
    #Si es circulo o pentagono solo la base va ser flotante o 0
        elif fig in ['cir', 'pent']:
            try:
                base = float(figura_forms.base.data or 0)
            except ValueError:
                base = 0
                
        if fig == 'rect':
            area = base * altura
        elif fig == 'tri':
            area = (base * altura) / 2
        elif fig == 'cir':
            area = math.pi * (base ** 2)
        elif fig == 'pent':
            area = (5 *base**2)/(4 * math.tan(math.pi/5))
    return render_template('figuras.html', form = figura_forms, area = area)









@app.route('/about')
def about():
    return "<h1>This is the about page.<h1>"

@app.route("/user/<string:user>")
def user(user):
    return "Hello " + user

@app.route("/numero/<int:n>")
def numero(n):
    return "Numero : {}".format(n)

@app.route("/user/<int:id>/<string:username>")
def username(id,username):
    return "ID: {} nombre: {}".format(id,username)

@app.route("/suma/<float:n1>/<float:n2>")
def func(n1, n2):
    return "la suma es : {}".format(n1+n2)

@app.route("/prueba")
def prueba():
    return '''
    <h1>Prueba de Html</h1>
    <p>Esto es un parrafo</p>
    <ul>
        <li>Elemento 1</li>
        <li>Elemento 2</li>
        <li>Elemento 2</li>
    </ul>
    '''

if __name__ == '__main__':
    app.run(debug=True)
