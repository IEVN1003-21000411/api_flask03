from flask import Flask, render_template, request

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
