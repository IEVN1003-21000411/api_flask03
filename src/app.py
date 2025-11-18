from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)
CORS(app, request = {r"/alumnos/*": {"origins" : "http://localhost:4200"}})#con esto si permitimos el acceso desde angular
conexion = MySQL(app)

@app.route('/alumnos', methods=['GET'])
def listar_usuarios():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT matricula, nombre, apaterno, amaterno, correo FROM alumnos"
        cursor.execute(sql)
        datos = cursor.fetchall()
 
        alumnos = []
        for fila in datos:
            alumno = {
                'matricula': fila[0],
                'nombre': fila[1],
                'apaterno': fila[2],
                'amaterno': fila[3],
                'correo': fila[4]
            }
            alumnos.append(alumno)
        return jsonify({'alumnos': alumnos, 'mensaje': 'alumno encontrado', "exito": True})
    except Exception as ex:
        return jsonify({'mensaje': 'error', "exito": False})
    
    
    
    
    
    
def leer_alumno_bd(matricula):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT matricula,nombre,apaterno,amaterno,correo FROM alumnos WHERE matricula = {0}".format(matricula)
        cursor.execute(sql)
        datos = cursor.fetchone()
        alumnos=[]
        if datos != None:
            alumnos = {'matricuala':datos[0],'nombre':datos[1],'apaterno':datos[2],'amaterno':datos[3],'correo':datos[4]}
            return alumnos
        else:
            return None
    except Exception as ex:
        raise ex


@app.route('/alumnos/<mat>', methods=['GET'])
def leer_curso(mat):
    try:
        alumnos = leer_alumno_bd(mat)
        if alumnos != None:
            return jsonify({'alumnos':alumnos,
                            'mensaje':'Alumno encontrado', 'exito':True})
        else:
            return jsonify({'mensaje':'Alumno no encontrado',
                            'exito':False})
    except Exception as ex:
        return jsonify({'mensaje':'Error',
                        'exito':False})


# Rota para registrar un alumno
# Se recibe un JSON con los datos del alumno        
@app.route('/alumnos', methods=['POST'])
def registrar_alumno():
    try:
        alumnos = leer_alumno_bd(request.json['matricula'])
        if alumnos != None:
            return jsonify({'mensaje': "Alunno ya existe, no sde puede duplicar",
                            'exito': False})
        else:
            cursor = conexion.connection.cursor()
            sql = """insert into alumnos(matricula, nombre, apaterno, amaterno, correo)
                    values('{0}', '{1}', '{2}', '{3}', '{4}')""".format(request.json['matricula'],
                                                                        request.json['nombre'],
                                                                        request.json['apaterno'],
                                                                        request.json['amaterno'],
                                                                        request.json['correo'])
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': "Alumno registrado",'exito': True})
        
    except Exception as ex:
        return jsonify({'mensaje': "Error al registrar el alumno",
                        'exito': False})
        

@app.route('/alumnos/<mat>', methods=['PUT'])
def actualizar_curso(mat):
        try:
            alumno = leer_alumno_bd(mat)
            if alumno != None:
                cursor = conexion.connection.cursor()
                sql = """UPDATE alumnos SET nombre = '{0}', apaterno = '{1}', amaterno='{2}', correo='{3}'
                WHERE matricula = {4}""".format(request.json['nombre'], request.json['apaterno'], request.json['amaterno'],request.json['correo'], mat)
                cursor.execute(sql)
                conexion.connection.commit()  # Confirma la acción de actualización.
                return jsonify({'mensaje': "Alumno actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error {0} ".format(ex), 'exito': False})           



@app.route('/alumnos/<mat>', methods=['DELETE'])
def eliminar_curso(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM alumnos WHERE matricula = {0}".format(mat)
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la acción de eliminación.
            return jsonify({'mensaje': "Alumno eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})    
    
    
    
    
    
def pagina_no_encontrada(error):
    return "<h1>La página que intentas buscar no existe...</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()   