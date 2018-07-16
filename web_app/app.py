import flask_admin
from flask import Flask, render_template, request, session, url_for
from flask_admin import Admin, helpers as admin_helpers
from flask_security import SQLAlchemyUserDatastore, Security

from web_app.models import db, Data_pesanan, Role, User, Rute
from web_app.views import Data_pesananView, MyModelView, RuteView


def create_app():

    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    db.init_app(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    admin = flask_admin.Admin(app, 'Admin Dashboard', base_template='my_master.html', template_mode='bootstrap3')
    # admin = flask_admin.Admin(app, 'Admin Dashboard', template_mode='bootstrap3')
    admin.add_view(Data_pesananView(Data_pesanan, db.session))
    admin.add_view(RuteView(Rute, db.session))
    admin.add_view(MyModelView(Role, db.session))
    admin.add_view(MyModelView(User, db.session))

    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )

    @app.route('/', methods = ["GET", "POST"])
    def form_pemesanan():

        if request.method == "get":
            nama_pemesan = request.form.get('nama_pemesan')
            nomor_telepon = request.form.get('nomor_telepon')
            alamat_anda = request.form.get('alamat_anda')
            kode_rute = request.form.get('tujuan')
            # kode_rute = None
            tanggal_ingin_berangkat = request.form.get('tanggal_ingin_berangkat')
            jam_ingin_berangkat = request.form.get('jam_ingin_berangkat')

            session['NAMA_PEMESAN'] = nama_pemesan
            session['NOMOR_TELEPON'] = nomor_telepon
            # session['ALAMAT_ANDA'] = alamat_anda
            session['TUJUAN'] = kode_rute
            session['TANGGAL_INGIN_BERANGKAT'] = tanggal_ingin_berangkat
            session['JAM_INGIN_BERANGKAT'] = jam_ingin_berangkat
            session['KODE_RUTE'] = kode_rute

            return render_template("metode_pembayaran.html")
        else:
            pass


        return render_template('form_pesan_tiket.html')

    @app.route('/metode_pembayaran', methods = ["GET", "POST"])
    def metode_pembayaran(status_pembayaran="pending"):

        nama_pemesan = request.args.get('nama_pemesan')
        nomor_telepon = request.args.get('nomor_telepon')
        alamat_anda = request.args.get('alamat_anda')
        tujuan = request.args.get('tujuan')
        tujuan = str(tujuan)
        tanggal_ingin_berangkat = request.args.get('tanggal_ingin_berangkat')
        jam_ingin_berangkat = request.args.get('jam_ingin_berangkat')
        kode_rute = request.args.get('kode_rute')



        if request.method == 'POST':
            session['NAMA_PEMESAN'] = nama_pemesan
            session['NOMOR_TELEPON'] = nomor_telepon
            session['ALAMAT_ANDA'] = alamat_anda
            session['TUJUAN'] = tujuan
            session['TANGGAL_INGIN_BERANGKAT'] = tanggal_ingin_berangkat
            session['JAM_INGIN_BERANGKAT'] = jam_ingin_berangkat

            rute = Rute()
            harga_tiket = None
            kode_rute = None
            id_rute = None
            if kode_rute == 'PDG':
                id_rute = Rute.query.get(1)
                id_rute = id_rute.id_rute
                harga_tiket = id_rute.ongkos
                id_rute = 1
            elif kode_rute == 'BKT':
                id_rute = Rute.query.get(2)
                id_rute = id_rute.id_rute
                harga_tiket = id_rute.ongkos
                id_rute = 2
            elif kode_rute == 'SCC':
                id_rute = Rute.query.get(3)
                id_rute = id_rute.id_rute
                harga_tiket = id_rute.ongkos
                id_rute = 3
            else:
                pass

            import string
            import random
            def generator_random(size=5, chars=string.ascii_uppercase + string.digits):
                return ''.join(random.choice(chars) for x in range(size))

            generate_invoice = 'NL' + generator_random() + 'INV'
            kode_pemesan = generate_invoice

            import time
            tanggal_pemesanan = time.strftime("%Y-%m-%d %H:%M:%S")

            nama_pemesan = session['NAMA_PEMESAN']
            nomor_telepon = session['NOMOR_TELEPON']
            alamat_anda = session['ALAMAT_ANDA']
            tujuan = session['TUJUAN']
            tujuan = str(tujuan)
            tanggal_ingin_berangkat = session['TANGGAL_INGIN_BERANGKAT']
            jam_ingin_berangkat = session['JAM_INGIN_BERANGKAT']
            status_pembayaran = status_pembayaran
            # id_rute = 1
            insert_to_db = Data_pesanan(id_rute, kode_pemesan, nama_pemesan, nomor_telepon, alamat_anda,
                                        tanggal_pemesanan, tanggal_ingin_berangkat,
                                        jam_ingin_berangkat, harga_tiket, status_pembayaran)
            db.session.add(insert_to_db)
            db.session.commit()

            return render_template('success.html')

        return render_template('metode_pembayaran.html')

    @app.route('/success')
    def success():
        return render_template('success.html')


    return app