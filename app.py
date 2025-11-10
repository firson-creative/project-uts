import math
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Menda_PakBoko_GAyyyy_354236yyyyyy'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pixel_volume.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    history_entries = db.relationship('History', backref='user', lazy=True)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shape_name = db.Column(db.String(50), nullable=False)
    inputs_str = db.Column(db.String(200), nullable=False)
    volume = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def is_logged_in():
    return 'user_id' in session

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']

        user = User.query.filter_by(username=username).first()
        
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
            flash(f'User baru "{username}" telah dibuat!', 'success')
        else:
            flash(f'Selamat datang kembali, {username}!', 'success')
        
        session['user_id'] = user.id
        session['username'] = user.username 

        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    shapes = [
        {'name': 'Kubus', 'id': 'kubus', 'image': 'kubus.png'},
        {'name': 'Balok', 'id': 'balok', 'image': 'balok.png'},
        {'name': 'Bola', 'id': 'bola', 'image': 'bola.png'},
        {'name': 'Tabung', 'id': 'tabung', 'image': 'tabung.png'},
        {'name': 'Prisma', 'id': 'prisma', 'image': 'prisma.png'},
        {'name': 'Kerucut', 'id': 'kerucut', 'image': 'kerucut.png'},
        {'name': 'Limas', 'id': 'limas', 'image': 'limas.png'}
    ]

    user_history = History.query.filter_by(user_id=session['user_id']).order_by(History.timestamp.desc()).all()
    
    return render_template('home.html', shapes=shapes, username=session['username'], history_list=user_history)

@app.route('/kalkulator/<string:bangun_ruang>')
def kalkulator(bangun_ruang):
    if not is_logged_in():
        return redirect(url_for('login'))
    
    shape_map = {
        'kubus': 'Kubus',
        'balok': 'Balok',
        'bola': 'Bola',
        'tabung': 'Tabung',
        'prisma': 'Prisma',
        'kerucut': 'Kerucut',
        'limas': 'Limas'
    }
    shape_name = shape_map.get(bangun_ruang)
    
    if not shape_name:
        flash('Bangun ruang tidak ditemukan.', 'danger')
        return redirect(url_for('home'))

    return render_template('kalkulator.html', bangun_ruang=bangun_ruang, shape_name=shape_name)

@app.route('/hitung', methods=['POST'])
def hitung():
    if not is_logged_in():
        return redirect(url_for('login'))
    shape_id = request.form['bangun_ruang'] 
    data_input = {'shape_id': shape_id}
    volume = 0
    
    try:
        if shape_id == 'kubus':
            sisi = float(request.form['sisi'])
            volume = sisi ** 3
            data_input['Sisi'] = sisi

        elif shape_id == 'balok':
            panjang = float(request.form['panjang'])
            lebar = float(request.form['lebar'])
            tinggi = float(request.form['tinggi'])
            volume = panjang * lebar * tinggi
            data_input['Panjang'] = panjang
            data_input['Lebar'] = lebar
            data_input['Tinggi'] = tinggi
            
        elif shape_id == 'bola':
            jari_jari = float(request.form['jari_jari'])
            volume = (4/3) * math.pi * (jari_jari ** 3)
            data_input['Jari-jari'] = jari_jari
            
        elif shape_id == 'tabung':
            jari_jari = float(request.form['jari_jari_tabung'])
            tinggi = float(request.form['tinggi_tabung'])
            volume = math.pi * (jari_jari ** 2) * tinggi
            data_input['Jari-jari'] = jari_jari
            data_input['Tinggi'] = tinggi

        elif shape_id == 'prisma':
            alas_segitiga = float(request.form['alas_segitiga'])
            tinggi_segitiga = float(request.form['tinggi_segitiga'])
            tinggi = float(request.form['tinggi'])
            volume = (alas_segitiga * tinggi_segitiga) / 2 * tinggi
            data_input['Alas_segitiga'] = alas_segitiga
            data_input['Tinggi_segitiga'] = tinggi_segitiga
            data_input['Tinggi'] = tinggi

        elif shape_id == 'kerucut':
            jari_jari_alas = float(request.form['jari_jari_alas'])
            tinggi = float(request.form['tinggi'])
            volume = (math.pi * jari_jari_alas ** 2) / 3 * tinggi
            data_input['Jari_jari_alas'] = jari_jari_alas
            data_input['Tinggi'] = tinggi

        elif shape_id == 'limas':
            sisi_alas = float(request.form['sisi_alas'])
            tinggi = float(request.form['tinggi'])
            volume = sisi_alas ** 2 / 3 * tinggi
            data_input['Sisi_alas'] = sisi_alas
            data_input['Tinggi'] = tinggi

        
        result_data = {
            'inputs': data_input,
            'volume': round(volume, 3)
        }
        inputs_str = ", ".join([f"{key}: {value}" for key, value in data_input.items() if key != 'shape_id'])
        
        new_history = History(
            shape_name=shape_id.capitalize(),
            inputs_str=inputs_str,
            volume=round(volume, 4),
            user_id=session['user_id']
        )
        db.session.add(new_history)
        db.session.commit()
        
        return render_template('result.html', data=result_data)
        
    except ValueError:
        flash('Input tidak valid, harap masukkan angka.', 'danger')
        return redirect(url_for('kalkulator', bangun_ruang=shape_id))
    except Exception as e:
        flash(f'Terjadi error: {e}', 'danger')
        return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)