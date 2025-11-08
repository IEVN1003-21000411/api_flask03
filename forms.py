from wtforms import Form
from wtforms import StringField, FloatField, PasswordField, IntegerField, EmailField
from wtforms import validators
from wtforms import RadioField, SelectMultipleField


class UserForm(Form):
    matricula = IntegerField('Matricula',[validators.DataRequired(message="La matricula es obligatoria")])
    nombre = StringField("Nombre", [validators.DataRequired(message="El campo es requerido")])
    apellido = StringField("Apellido", [validators.DataRequired(message="El campo es requerido")])
    correo = EmailField("Correo",[validators.Email(message="Ingresar Correo valido")])
    
class FigurasForm(Form):
    figura = RadioField('Selecciona una figura', choices=[('tri','Triangulo'),
                                                          ('rect','Rectangulo'),
                                                          ('cir','Circulo'),
                                                          ('pent','Pentagono')],
                        validators=[validators.DataRequired(message="Seleccione una figura")])
    base = FloatField("Base")
    altura = FloatField("Altura")
    largo = FloatField("Largo")
    ancho = FloatField("Ancho")
    radio = FloatField("Radio")
    lado = FloatField("Lado")
    
    
class ClientesForm(Form):
    nombre = StringField("Nombre", [validators.DataRequired(message="El campo es requerido")])
    
    telefono = StringField("Telefono",[validators.DataRequired(message="El campo es requerido")])
    
    direccion = StringField("Direccion",[validators.DataRequired(message="El campo es requerido")])
     
    tamano = RadioField('Tamaño Pizza', choices=[('chica','Chica $40'),
                                           ('mediana','Mediana $80'),
                                           ('grande','Grande $120')],
                        validators=[validators.DataRequired(message="Seleccione un tamaño")])
    ingredientes = SelectMultipleField('Ingredientes', choices=[('jamon','Jamon $10'),
                                                                ('piña','Piña $10'),
                                                                ('champiñones','Champiñones $10'),])
    cantidad = IntegerField("Numero de pizzas",
                            [validators.DataRequired(message="Ingresa la cantidad")]
                            )
    