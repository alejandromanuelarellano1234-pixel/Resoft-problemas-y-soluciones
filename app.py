from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'resoft-clave-secreta-super-segura'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resoft_soporte.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelo de Usuarios
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

# Modelo de Problemas y Respuestas
class Problema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    respuesta = db.Column(db.Text, nullable=True)
    
    autor = db.relationship('Usuario', backref=db.backref('problemas', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

# Crear base de datos
with app.app_context():
    db.create_all()

# --- RUTAS DE LA APLICACIÓN ---

@app.route('/')
@login_required
def index():
    problemas = Problema.query.all()
    return render_template('index.html', problemas=problemas)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        usuario = Usuario.query.filter_by(username=username).first()
        
        if usuario and check_password_hash(usuario.password_hash, password):
            login_user(usuario)
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if Usuario.query.filter_by(username=username).first():
            flash('El usuario ya existe')
            return redirect(url_for('registro'))
            
        hashed_pw = generate_password_hash(password)
        nuevo_usuario = Usuario(username=username, password_hash=hashed_pw)
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('Cuenta creada con éxito. Iniciá sesión.')
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/crear-problema', methods=['POST'])
@login_required
def crear_problema():
    titulo = request.form.get('titulo')
    descripcion = request.form.get('descripcion')
    nuevo_problema = Problema(titulo=titulo, descripcion=descripcion, autor=current_user)
    db.session.add(nuevo_problema)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/responder/<int:problema_id>', methods=['POST'])
@login_required
def responder_problema(problema_id):
    problema = db.session.get(Problema, problema_id)
    if problema:
        respuesta = request.form.get('respuesta')
        problema.respuesta = respuesta
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

