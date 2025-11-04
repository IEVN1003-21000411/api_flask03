from wtforms import Form
from wtforms import StringField,FloatField, EmailField,PasswordField,IntegerField,RadioField
from wtforms.validators import InputRequired,NumberRange,Email
from wtforms import validators


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