import math
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

app.secret_key = 'Menda_PakBoko_GAyyyy_354236yyyyyy'

def is_logged_in():
    return 'username' in session

@app.route('/')
def index():

    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        
        session['username'] = username

        flash(f'Selamat datang, {username}!', 'success')
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
def logout():
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
    return render_template('home.html', shapes=shapes, username=session['username'])

# --- Halaman 4: Kalkulator (Input Dimensi) ---

@app.route('/kalkulator/<string:shape_id>')
def kalkulator(shape_id):
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
    shape_name = shape_map.get(shape_id)
    
    if not shape_name:
        flash('Bangun ruang tidak ditemukan.', 'danger')
        return redirect(url_for('home'))
        
    return render_template('kalkulator.html', shape_id=shape_id, shape_name=shape_name)

# --- Halaman 5: Result (Hasil Perhitungan) ---

@app.route('/hitung', methods=['POST'])
def hitung():
    if not is_logged_in():
        return redirect(url_for('login'))
    
    shape_id = request.form['shape_id']
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
            'volume': round(volume, 4)
        }
        
        return render_template('result.html', data=result_data)
        
    except ValueError:
        flash('Input tidak valid, harap masukkan angka.', 'danger')
        return redirect(url_for('kalkulator', shape_id=shape_id))
    except Exception as e:
        flash(f'Terjadi error: {e}', 'danger')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)