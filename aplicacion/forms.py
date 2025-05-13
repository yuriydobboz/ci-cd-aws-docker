from flask_wtf import FlaskForm

from wtforms import Form, IntegerField,SelectField,SubmitField,StringField, DecimalField, TextAreaField, FileField, PasswordField, EmailField
from wtforms.validators import InputRequired, DataRequired, NumberRange

class formBuscarDigi(FlaskForm):                      
	campo= SelectField("Campo",choices=["Nombre","Defensa","Ataque"])
	modo= SelectField("Modo",choices=["Empieza","Acaba","Contiene","Igual a"])
	textoBuscar=StringField("Texto a Buscar",validators=[DataRequired("Tienes que introducir el dato")])
	buscar = SubmitField('Buscar')

class formArticulo(FlaskForm): 
	nombre=StringField("Nombre:",validators=[InputRequired("Tienes que introducir el dato")])
	precio=DecimalField("Precio:",default=0,validators=[InputRequired("Tienes que introducir el dato")])
	iva=IntegerField("IVA:",default=21,validators=[InputRequired("Tienes que introducir el dato")])
	descripcion= TextAreaField("Descripción:")
	photo = FileField('Selecciona imagen:')
	stock=IntegerField("Stock:",default=1,validators=[InputRequired("Tienes que introducir el dato")])
	CategoriaId=SelectField("Categoría:",coerce=int)
	submit = SubmitField('Enviar')


class FormCategoria(FlaskForm):
    nombre = StringField("Nombre:",
                        validators=[InputRequired("Tienes que introducir el dato")]
                        )
    submit = SubmitField('Enviar')
    

class FormTipo(FlaskForm):
    tipo = StringField("Tipo:",
                        validators=[InputRequired("Tienes que introducir el dato")]
                        )
    submit = SubmitField('Enviar')
    
class formBuscarTipo(FlaskForm):
    tipo = StringField("Tipo:", validators=[InputRequired("Tienes que introducir el dato")])
    modo = SelectField("Modo de búsqueda:", choices=[("Empieza", "Empieza"), ("Contiene", "Contiene"), ("Igual a", "Igual a"), ("Acaba", "Acaba")])
    submit = SubmitField('Buscar')


class FormDigimones(FlaskForm): 
	nombre=StringField("Nombre:",validators=[InputRequired("Tienes que introducir el dato")])
	ataque = IntegerField("Ataque", validators=[InputRequired("Este campo es obligatorio."), NumberRange(min=1, max=300, message="El valor debe ser entre 1 y 300.")])
	defensa = IntegerField("Defensa", validators=[InputRequired("Este campo es obligatorio."), NumberRange(min=1, max=300, message="El valor debe ser entre 1 y 300.")])
	nivel= SelectField("Nivel:",choices=[('Inicial', 'Bebito'), ('Medio', 'Ya sabe algo'),('Experto','Se mucho Flask'),('Experto','Puto Amo')])
	imagen = FileField('Selecciona imagen:')
	TipoId=SelectField("Tipo:",coerce=int)
	submit = SubmitField('Enviar')    

class FormSINO(FlaskForm):
    si = SubmitField('Si')
    no = SubmitField('No')
    
class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Entrar')
    
class FormUsuario(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    nombre = StringField('Nombre completo')
    email = EmailField('Email')
    submit = SubmitField('Aceptar')

class FormChangePassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Aceptar')