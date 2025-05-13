import os
from flask import Flask, render_template, redirect, url_for,abort, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from aplicacion import config
from werkzeug.utils import secure_filename
from aplicacion.forms import formArticulo, FormCategoria,FormSINO, FormTipo,FormDigimones, \
    formBuscarDigi, formBuscarTipo, FormTipo, LoginForm, FormUsuario,FormChangePassword
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__, static_folder='static')
app.config.from_object(config)


#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

Bootstrap(app)
db = SQLAlchemy(app)
#Importamos los modelos una vez existe una instancia de app y otra instancia de db,
# En otras palabras si no hay base de datos, no puedo utilizar los modelos
# no base de datos (objeto) => No puedo acceder a las tablas
from aplicacion.models import *

#Esto es Nuevo
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/error_permisos')
def error_permisos():
    return render_template('error_permisos.html', usuario=current_user.username, error="Acción no permitida")

@app.route('/login', methods=['get', 'post'])
def login():
    from aplicacion.models import Usuarios
    # Control de permisos
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('inicio'))
        form.username.errors.append("Usuario o contraseña incorrectas.")
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/registro", methods=["get", "post"])
def registro():
    from aplicacion.models import Usuarios
    # Control de permisos
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))
    form = FormUsuario()
    if form.validate_on_submit():
        existe_usuario = Usuarios.query.\
            filter_by(username=form.username.data).first()
        if existe_usuario is None:
            user = Usuarios()
            form.populate_obj(user)
            user.admin = False
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("inicio"))
        form.username.errors.append("Nombre de usuario ya existe.")
    return render_template("usuarios_new.html", form=form)


@app.route('/perfil/<username>', methods=["get", "post"])
@login_required
def perfil(username):
    from aplicacion.models import Usuarios
    user = Usuarios.query.filter_by(username=username).first()
    if user is None or user.id!=current_user.id:
        abort(404)
    form = FormUsuario(request.form, obj=user)
    del form.password
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("usuarios_new.html", form=form, perfil=True)

@app.route('/changepassword/<username>', methods=["get", "post"])
@login_required
def changepassword(username):
    from aplicacion.models import Usuarios
    user = Usuarios.query.filter_by(username=username).first()
    if user is None or user.id!=current_user.id:
        abort(404)
    form = FormChangePassword()
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("changepassword.html", form=form)

@login_manager.user_loader
def load_user(user_id):
    from aplicacion.models import Usuarios
    return Usuarios.query.get(int(user_id))

@app.route('/usuarios', methods=["GET"])
@login_required
def usuarios():
    if not current_user.is_admin():
        return redirect(url_for('error_permisos'))
    usuarios = Usuarios.query.all()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route('/')
def bienvenido():
    return render_template ("bienvenido.html")

@app.route('/inicializar')
def inicializar():
    from aplicacion.inicializacion_datos import add_data_tables, drop_tables
    drop_tables()
    add_data_tables()
    return "Datos Inicializados"


@app.route('/tipos', methods=["GET"])
def tipos():
    tipos = Tipos.query.all()
    return render_template("tipos.html", tipos=tipos)

@app.route('/digimones')
@app.route('/tipo/<id>')
def inicio(id='0'):
    tipo=Tipos.query.get(id)
    if id=='0':
        digimones=Digimones.query.all()
    else:
        digimones=Digimones.query.filter_by(TipoId=id)
    tipos=Tipos.query.all()
    return render_template("inicio.html",digimones=digimones,tipos=tipos,tipo=tipo)


@app.route('/tipos/new', methods=["get", "post"])
@login_required
def tipos_new():
    if not current_user.is_admin():
        return redirect(url_for('error_permisos'))
    form = FormTipo()
    if form.validate_on_submit():
        tipo = Tipos(tipo=form.tipo.data)
        db.session.add(tipo)
        db.session.commit()
        return redirect(url_for('tipos'))
    return render_template("tipos_new.html", form=form)

@app.route('/tipo/<id>/edit', methods=["get", "post"])
@login_required
def tipo_edit(id):
    if not current_user.is_admin():
        return redirect(url_for('error_permisos'))
    tipo = Tipos.query.get_or_404(id)
    form = FormTipo(obj=tipo)
    if form.validate_on_submit():
        tipo.tipo = form.tipo.data
        db.session.commit()
        return redirect(url_for('tipos'))
    return render_template("tipo_edit.html", form=form, tipo=tipo)


@app.route('/tipo/<id>/delete', methods=["get", "post"])
@login_required
def tipo_delete(id):
    if not current_user.is_admin():
        return redirect(url_for('error_permisos'))
    tipo = Tipos.query.get_or_404(id)
    form = FormSINO()
    if form.validate_on_submit() and form.si.data:
        db.session.delete(tipo)
        db.session.commit()
        return redirect(url_for('tipos'))
    return render_template("confirmar_tipos_delete.html", form=form, tipo=tipo)


@app.route('/digimones/new', methods=["get", "post"])
@login_required
def digimones_new():
    if not current_user.is_admin():
        return redirect(url_for('error_permisos'))
    form = FormDigimones()
    tipos = [(t.id, t.tipo) for t in Tipos.query.all()]
    form.TipoId.choices = tipos 

    if form.validate_on_submit():
        try:
            f = form.imagen.data
            nombre_fichero = secure_filename(f.filename)
            f.save(app.root_path + "/static/upload/" + nombre_fichero)
        except:
            nombre_fichero = ""
        
        digimon = Digimones()
        form.populate_obj(digimon)
        digimon.imagen = nombre_fichero  
        db.session.add(digimon)
        db.session.commit()

        return redirect(url_for("inicio"))

    return render_template("digimones_new.html", form=form)


@app.route('/tipos/search', methods=["get", "post"])
def tipos_search():
    form = formBuscarTipo(request.form)

    if form.validate_on_submit():
        textoBuscar = form.tipo.data  
        modo = form.modo.data  

        if modo == "Empieza":
            search = f"{textoBuscar}%"  
        elif modo == "Acaba":
            search = f"%{textoBuscar}"  
        elif modo == "Contiene":
            search = f"%{textoBuscar}%"  
        elif modo == "Igual a":
            search = f"{textoBuscar}" 
        else:
            search = f"%"

        tipos = Tipos.query.filter(Tipos.tipo.like(search)).all()  
        busqueda = True  
        cantidad = len(tipos)  

        return render_template("tipos_search.html", form=form, busqueda=busqueda, textoBuscar=textoBuscar, tipos=tipos, cantidad=cantidad)
    else:
        tipos = Tipos.query.all()
        cantidad = len(tipos)
        return render_template("tipos_search.html", form=form, tipos=tipos, cantidad=cantidad)


@app.route('/digimones/<id>/edit', methods=["get", "post"])
@login_required
def digimon_edit(id):
    if not current_user.is_admin():
        return redirect(url_for('error_permisos'))
    digimon = Digimones.query.get(id)
    if digimon is None:
        abort(404)
    form = FormDigimones(obj=digimon)
    tipos = [(t.id, t.tipo) for t in Tipos.query.all()]
    form.TipoId.choices = tipos

    if form.validate_on_submit():
        if form.imagen.data:
            os.remove(app.root_path + "/static/upload/" + digimon.imagen)
            try:
                f = form.imagen.data
                nombre_fichero = secure_filename(f.filename)
                f.save(app.root_path + "/static/upload/" + nombre_fichero)
            except:
                nombre_fichero = ""
        else:
            nombre_fichero = digimon.imagen

        form.populate_obj(digimon)
        digimon.imagen = nombre_fichero

        db.session.commit()
        return redirect(url_for("inicio"))
    

    return render_template("digimon_edit.html", form=form, digimon=digimon, id=id)



@app.route('/digimon/<id>/delete', methods=["get", "post"])
@login_required
def digimon_delete(id):
    if not current_user.is_admin():
        return redirect(url_for('error_permisos'))
    form = FormSINO()
    digimon = Digimones.query.get(id)
    if form.validate_on_submit():
        if form.si.data:
            if digimon is None:
                abort(404)
            if digimon.imagen != "" and digimon.imagen!=None    :
                try:
                    os.remove(app.root_path + "/static/upload/" + digimon.imagen)
                except:
                    abort (404)
            db.session.delete(digimon)
            db.session.commit()
        return redirect(url_for("inicio"))
    else:
        return render_template("confimar_digimones_delete.html", form=form, digimon=digimon)
    


@app.route('/digimones/search',methods=["get","post"])
def digimones_search():
    form=formBuscarDigi(request.form)
    if form.validate_on_submit():
        campo=form.campo.data
        modo=form.modo.data
        textoBuscar=form.textoBuscar.data
        if form.modo.data=="Empieza":
            search = f"{textoBuscar}%"
        elif form.modo.data=="Acaba":
            search = f"%{textoBuscar}"
        elif form.modo.data=="Contiene":
            search = f"%{textoBuscar}%"
        elif form.modo.data=="Igual a":
            search = f"{textoBuscar}"
        else:
            search = f"%"
        digimones=Digimones.query.filter(getattr(Digimones, campo.lower()).like(search))
        busqueda= True
        cantidad= digimones.count()
        textoBuscar=textoBuscar.replace("%","")
        return render_template("digimones_search.html",form=form, busqueda=busqueda, campo=campo, modo=modo, textoBuscar=textoBuscar, digimones=digimones, cantidad=cantidad)  
    else:
        digimones=Digimones.query.all()
        cantidad=len(digimones)
        
        return render_template("digimones_search.html",digimones=digimones, cantidad=cantidad,form=form)     

def bienvenido():
    return render_template ("bienvenido.html")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404


