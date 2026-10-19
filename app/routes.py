import os
from flask import render_template, request, redirect, flash, url_for, session, jsonify
from itsdangerous import serializer

from run_app import app
from app.models import Database, Teknisi, Services, Login, Customers, Dispath, Complation

# Load variables from the .env file
app.secret_key = "your_super_secret_session_key"

@app.route('/')
def home():
    if 'username' in session:
        months = ["January", "February", "March", "April", "May", "June"]
        sales = [12, 19, 3, 5, 2, 3]

        return render_template('home/dashboard.html', labels=months, values=sales)

    return redirect(url_for('login'))


# Service
@app.route('/services')
def services():
    service = Services().tampil_services()

    return jsonify(service)

@app.route('/data-services')
def data_services():
    data_list = Services().tampil_services()

    return render_template('service/data-service.html', service=data_list)

@app.route('/coba-form-services/<int:id>')
def coba_form_services(id):
    service = Services()
    return jsonify(service.form_ubah_services(id))

@app.route('/tambah-services/<int:id>', methods=['POST', 'GET'])
def tambah_services(id):
    services = Services()

    if request.method == 'POST':
        customer_id=id
        teknisi_id = request.form.get("teknisi_id")
        remark_unit = request.form.get("remark_unit")
        tanggal_kunjungan = request.form.get("tanggal_kunjungan")
        tanggal_selesai = request.form.get("tanggal_selesai")

        services.tambah_services(customer_id, teknisi_id, tanggal_kunjungan, tanggal_selesai, remark_unit)
        
        return redirect(url_for('data_services'))

    data_form = services.form_tambah_services(id)
    data_teknisi = Teknisi().tampil_teknisi()

    return render_template('service/tambah-service.html', data=data_form[0], teknisi=data_teknisi)
    
@app.route('/ubah-services/<int:id>', methods=['GET', 'POST'])
def ubah_services(id):
    services = Services()

    if request.method == 'POST':
        teknisi_id = request.form.get('teknisi_id')
        tanggal_kunjungan = request.form.get('tanggal_kunjungan')
        tanggal_selesai = request.form.get('tanggal_selesai')
        remark_unit = request.form.get('remark_unit')
        status_pekerjaan = request.form.get("status_pekerjaan")
        keterangan_service = request.form.get("keterangan_service")

        services.ubah_services(teknisi_id, tanggal_kunjungan, tanggal_selesai, remark_unit, status_pekerjaan, keterangan_service, id)

        return redirect(url_for('data_services'))


    data_form = services.form_ubah_services(id)
    data_teknisi = Teknisi().tampil_teknisi()

    return render_template('service/ubah-service.html', data=data_form[0], teknisi=data_teknisi)

@app.route('/hapus-services/<int:id>')
def hapus_services(id):
    Services().hapus_services(id)

    return redirect(url_for('data_services'))

#Customer
@app.route('/data-customer')
def data_customer():
    data_list = Customers().tampil_customers()

    return render_template('customer/data-customer.html', customer=data_list)

@app.route('/tambah-customer', methods = ['POST'])
def tambah_customer():
    data_input = request.form.to_dict()

    Customers().tambah_customers(no_spk=data_input['no_spk'], 
        nama=data_input['nama'], 
        alamat=data_input['alamat'], 
        no_tlpn=data_input['no_tlpn'], 
        sn_indoor=data_input['sn_indoor'], 
        model_indoor=data_input['model_indoor'], 
        sn_outdoor=data_input['sn_outdoor'], 
        model_outdoor=data_input['model_outdoor'],
        tgl_spk=data_input['tgl_spk'], 
        kerusakan=data_input['kerusakan'], 
        garansi=data_input['garansi'])
    
    return redirect(url_for('data_customer'))

@app.route('/ubah-customer/<int:id>', methods = ['GET','POST'])
def ubah_customer(id):
    customer = Customers()

    if request.method == 'POST':
        data_input = request.form.to_dict()

        customer.ubah_customers(no_spk=data_input['no_spk'], 
            nama=data_input['nama'], 
            alamat=data_input['alamat'], 
            no_tlpn=data_input['no_tlpn'], 
            sn_indoor=data_input['sn_indoor'], 
            model_indoor=data_input['model_indoor'], 
            sn_outdoor=data_input['sn_outdoor'], 
            model_outdoor=data_input['model_outdoor'],
            tgl_spk=data_input['tgl_spk'], 
            kerusakan=data_input['kerusakan'], 
            garansi=data_input['garansi'],
            id=id)

        return redirect(url_for('data_customer'))

    data_form = customer.form_ubah_customer(id)
    
    return render_template('customer/ubah-customer.html', data=data_form[0])

@app.route('/hapus-customer/<int:id>', methods=['POST'])
def hapus_customer(id):
    Customers().hapus_customer(id)

    return redirect(url_for('data_customer'))

#Teknisi
@app.route('/data-teknisi')
def data_teknisi():
    data_list = Teknisi().tampil_teknisi()

    return render_template('teknisi/data-teknisi.html', teknisi=data_list)

@app.route('/tambah-teknisi', methods = ["POST"])
def tambah_teknisi():
    data_input = request.form.to_dict()

    Teknisi().tambah_teknisi(nama=data_input['nama'], 
        no_tlpn=data_input['no_tlpn'])

    return redirect(url_for('data_teknisi'))

@app.route('/ubah-teknisi/<int:id>', methods = ["POST", "GET"])
def ubah_teknisi(id):
    teknisi = Teknisi()

    if request.method == 'POST':
        data_input = request.form.to_dict()

        teknisi.ubah_teknisi(id=id, 
            nama=data_input['nama'], 
            no_tlpn=data_input['no_tlpn'])

        return redirect(url_for('data_teknisi'))

    data_form = teknisi.form_ubah_teknisi(id)

    return render_template('teknisi/ubah-teknisi.html', data=data_form[0])

@app.route('/hapus-teknisi/<int:id>', methods = ['POST'])
def hapus_teknisi(id):
    Teknisi().hapus_teknisi(id)

    return redirect(url_for('data_teknisi'))

#Data 1 hari service
@app.route('/dispath/<int:bulan>')
def dispath(bulan):
    dispath = Dispath()
    data = dispath.tampil_data_dispath(bulan)
    return jsonify(data)


#Data 3 Hari Service
@app.route('/complation/<int:bulan>')
def somplation(bulan):
    complation = Complation()
    data = complation.tampil_data_complation(bulan)
    return jsonify(data)

# Login Session
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Login(username, password)

        if user.authenticate():
            session['username'] = username

            return redirect(url_for('home'))
        
        flash('Username dan password anda salah', 'text-danger')

        return redirect(url_for('login'))

    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.pop("username", None)

    return redirect(url_for('login'))

# Error Handler
@app.errorhandler(404)  # Halaman Tidak Ditemukan
def page_not_found(error):
    return render_template('error/page_not_found.html'), 404

# User Setting
@app.route('/user-setting', methods=['GET', 'POST'])
def user_setting():
    return render_template('account/user-setting.html')



