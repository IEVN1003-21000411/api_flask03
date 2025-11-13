from flask import Flask, render_template, request
import forms
import math
from flask import make_response, jsonify
from datetime import datetime
import json

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
    
    estudiantes=[]
    tem = []
    datos={}
    
    alumnos_clase = forms.UserForm(request.form)
    if request.method == 'POST' and alumnos_clase.validate():#Mandamos los datos del html a from.py
        mat= alumnos_clase.matricula.data
        nom = alumnos_clase.nombre.data
        ape=alumnos_clase.apellido.data
        em=alumnos_clase.correo.data
        datos={"matricula":mat,"nombre":nom,"appellido":ape,"correo":em}
        
        datos_str = request.cookies.get('Estudiantes')
        if not datos_str:
            return "No hay cookies"
        
        tem = json.loads(datos_str)#Los esta pasado como diccionario y no como lista primero hay que convertirlos a lista
        estudiantes = tem
        estudiantes.append(datos)
        
    response = make_response(render_template('Alumnos.html', form = alumnos_clase, mat = mat, nom = nom, ape= ape, em = em))
    
    response.set_cookie('Estudiantes', json.dumps(estudiantes))
    
    return response


# @app.get("/get_cookie")
# def get_cookie():
#     datos_str = request.cookies.get('Estudiantes')
#     if not datos_str:
#         return "No hay cookies"
    
#     datos = json.loads(datos_str)
#     return jsonify(datos)
    




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
    
    
    
    
    












#pizzas
@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    form = forms.ClientesForm(request.form)
    pedido = []
    ventas = []
    total_dia = 0

    pedido_cookie = request.cookies.get('pedido')
    ventas_cookie = request.cookies.get('ventas')

    if pedido_cookie:
        try:
            pedido = json.loads(pedido_cookie)
        except:
            pedido = []

    if ventas_cookie:
        try:
            ventas = json.loads(ventas_cookie)
        except:
            ventas = []

    if request.method == 'POST':
        accion = request.form.get('action')
        
        if accion == 'agregar' and form.validate():
            nombre = form.nombre.data
            direccion = form.direccion.data
            telefono = form.telefono.data
            tamano = form.tamano.data
            ingredientes = form.ingredientes.data
            cantidad = form.cantidad.data

            precios = {'chica': 40, 'mediana': 80, 'grande': 120}
            subtotal = precios[tamano] * cantidad + (10 * len(ingredientes))

            nueva_pizza = {
                'tamano': tamano,
                'ingredientes': ingredientes,
                'cantidad': cantidad,
                'subtotal': subtotal
            }

            pedido.append(nueva_pizza)
        
        elif accion and accion.startswith('quitar_'):
            try:
                indice = int(accion.split('_')[1])
                if 0 <= indice < len(pedido):
                    pedido.pop(indice)
                    print(f"Pizza eliminada en índice {indice}")
            except Exception as e:
                print("Error al eliminar:", e)

       
        elif accion == 'terminar':
            pedido_cookie = request.cookies.get('pedido')
            if pedido_cookie:
                pedido = json.loads(pedido_cookie)
                print("Pedido cargado de cookie:", pedido)
            else:
                print("No hay cookie de pedido")

            if pedido:
                total_cliente = sum(p['subtotal'] for p in pedido)
                nombre = form.nombre.data or "Cliente sin nombre"
                direccion = form.direccion.data or "Sin direccion"
                telefono = form.telefono.data or "Sin telefono"
                fecha = datetime.now().strftime('%d-%m-%Y')

                venta = {
                    'nombre': nombre,
                    'direccion': direccion,
                    'telefono': telefono,
                    'fecha': fecha,
                    'total': total_cliente
                }

                print("Venta creada:", venta)
                ventas.append(venta)
                pedido = []
            else:
                print("Pedido vacío, no se registró venta.")

 
    
    hoy = datetime.now().strftime('%d-%m-%Y')
    ventas_hoy = []
    total_dia = 0

    for v in ventas:
        if v.get('fecha') == hoy:
            ventas_hoy.append((v.get('nombre', 'Cliente'), v.get('total', 0)))
            total_dia += v.get('total', 0)

    response = make_response(render_template(
        'pedidos.html',
        form=form,
        pedido=pedido,
        ventas=ventas,
        ventas_hoy=ventas_hoy,
        total_dia=total_dia
    ))
    
    response.set_cookie('pedido', json.dumps(pedido))
    response.set_cookie('ventas', json.dumps(ventas))
    print("Cookies actualizadas con:", {'pedido': pedido, 'ventas': ventas})

    return response

@app.route("/get_cookie")
def get_cookie():
    ventas_cookie = request.cookies.get('ventas')
    if not ventas_cookie:
        return jsonify([])

    try:
        ventas = json.loads(ventas_cookie)
    except Exception as e:
        print("Error leyendo ventas:", e)
        ventas = []

    return jsonify(ventas)

 

    
    
    
    
    
    
    
    
 

if __name__ == '__main__':
    app.run(debug=True)
