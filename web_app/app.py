from datetime import date
import sys, os
sys.path.append(os.getcwd() + '/web_app') #sesuai dengan mark directory as sources
import flask_admin
from flask import Flask, render_template, request, session, url_for, flash, make_response, redirect
from flask_admin import Admin, helpers as admin_helpers
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from flask_security import SQLAlchemyUserDatastore, Security
from flask_security.utils import verify_password

from form import LoginFormView, AddRuteForm, EditRuteForm
from models import db, Data_pesanan, Role, User, Rute, PO
from views import Data_pesananView, MyModelView, RuteView, PoView

import string
import random
import time
import pdfkit

################################## TWILIO ##################################
from web_app.settings import TWLIO_ACCOUNT_SID_NONE_UPGRADED_FOR_ADMIN, TWLIO_AUTH_TOKEN_NONE_UPGRADED_FOR_ADMIN, \
    TWLIO_ACCOUNT_SID_UPGRADED_FOR_USER, TWLIO_AUTH_TOKEN_UPGRADED_FOR_USER
from twilio.rest import Client
################################## TWILIO ##################################

################################## GMAIL ##################################
import base64
import httplib2
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
################################## GMAIL ##################################

def create_app():

    app = Flask(__name__)

    app.config.from_pyfile('settings.py')

    db.init_app(app)

    bootstrap = Bootstrap(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    admin = flask_admin.Admin(app, 'Admin Dashboard', base_template='my_master.html', template_mode='bootstrap3')
    admin.add_view(PoView(PO, db.session))
    admin.add_view(MyModelView(Role, db.session))
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(RuteView(Rute, db.session))
    admin.add_view(Data_pesananView(Data_pesanan, db.session))


    @security.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
            get_url=url_for
        )


    @app.route('/', methods = ['GET', 'POST'])
    def index():

        if request.method == "get":

            dari = request.form['dari']
            tujuan = request.form['tujuan']
            tanggal_keberangkatan = request.form['tanggal_keberangkatan']
            jumlah_kursi_yang_di_booking = request.form['jumlah_kursi_yang_di_booking']

            session['tanggal_keberangkatan'] = tanggal_keberangkatan
            session['jumlah_kursi_yang_di_booking'] = jumlah_kursi_yang_di_booking

            cari_bis = db.session.query(Rute.id_rute, Rute.tujuan, Rute.ongkos, Rute.tanggal_keberangkatan, Rute.jam). \
                filter(Rute.dari == dari, Rute.tujuan == tujuan, Rute.tanggal_keberangkatan == tanggal_keberangkatan).first()

            return render_template("bis.html")

        return render_template('halaman_utama.html')

    @app.route('/bis', methods = ['GET', 'POST'])
    def bis():

        tanggal_keberangkatan = request.args.get('tanggal_keberangkatan')
        dari = request.args.get('dari')
        tujuan = request.args.get('tujuan')
        jumlah_kursi_yang_di_booking = request.args.get('jumlah_kursi_yang_di_booking')

        urutan_tampilan = db.session.query(Rute.id_rute, Rute.dari, Rute.tujuan, Rute.ongkos, Rute.tanggal_keberangkatan,
                                           Rute.jam, PO.nama_po, Rute.jumlah_kursi).join(PO).\
            filter(Rute.tanggal_keberangkatan == tanggal_keberangkatan, Rute.dari == dari, Rute.tujuan == tujuan,
                             Rute.jumlah_kursi >= jumlah_kursi_yang_di_booking).all()


        session['jumlah_kursi_yang_di_booking'] = jumlah_kursi_yang_di_booking



        if request.method == "get":
            return render_template("pastikan_harga.html")

        return render_template('pilih_bis.html', URUTAN_TAMPILAN = urutan_tampilan)


    @app.route('/pastikan_harga', methods = ['GET', 'POST'])
    def pastikan_harga():
        id_rute = request.args.get('id_rute')

        session['rute_id'] = id_rute
        jumlah_kursi_yang_di_booking = session['jumlah_kursi_yang_di_booking']

        harga = db.session.query(Rute.ongkos).filter(Rute.id_rute == id_rute).first()
        harga = harga[0]
        session['harga_tiket'] = harga
        harga_total = int(harga) * int(jumlah_kursi_yang_di_booking)

        session['harga_total'] = harga_total

        jam = db.session.query(Rute.jam).filter(Rute.id_rute == id_rute).first()
        jam = jam[0]
        session['jam'] = str(jam)
        tanggal_keberangkatan = db.session.query(Rute.tanggal_keberangkatan).filter(Rute.id_rute == id_rute).first()
        tanggal_keberangkatan = tanggal_keberangkatan[0]
        session['tanggal_keberangkatan'] = tanggal_keberangkatan
        dari = db.session.query(Rute.dari).filter(Rute.id_rute == id_rute).first()
        dari = dari[0]
        session['dari'] = dari
        tujuan = db.session.query(Rute.tujuan).filter(Rute.id_rute == id_rute).first()
        tujuan = tujuan[0]
        session['tujuan'] = tujuan

        nama_po = db.session.query(Rute.po_name, PO.nama_po).join(PO).filter(Rute.id_rute == id_rute).first()
        nama_po = nama_po[1]
        session['nama_po'] = nama_po

        jumlah_kursi = jumlah_kursi_yang_di_booking
        session['jumlah_kursi_yang_di_booking'] = jumlah_kursi

        if request.method == "get":
            return render_template("kontak.html")

        return render_template("pastikan_harga.html", NAMA_PO=nama_po, JUMLAH_KURSI=jumlah_kursi, HARGA_TOTAL=harga_total, TANGGAL_KEBERANGKATAN=tanggal_keberangkatan,
                               JAM=jam, DARI=dari, TUJUAN=tujuan)

    @app.route('/kontak', methods = ['GET', 'POST'])
    def kontak():
        if request.method == "get":
            session['nama_pemesan'] = request.form.get('nama_pemesan')
            session['email'] = request.form.get('email')
            session['nomor_handphone'] = request.form.get('nomor_handphone')

            session['title_penumpang'] = request.form.get('title_penumpang')
            session['nama_penumpang'] = request.form.get('nama_penumpang')
            session['tanggal_lahir'] = request.form.get('tanggal_lahir')

            return render_template("payment.html")

        return render_template('kontak.html')

    @app.route('/payment', methods = ['GET', 'POST'])
    def payment(status='pending'):

        rute_id = session['rute_id']
        nama_pemesan = request.args.get('nama_pemesan')
        email = request.args.get('email')
        nomor_telepon = request.args.get('nomor_handphone')
        title_penumpang = request.args.get('title_penumpang')
        nama_penumpang = request.args.get('nama_penumpang')
        tanggal_lahir = request.args.get('tanggal_lahir')
        nama_po = session['nama_po']
        dari = session['dari']
        tujuan = session['tujuan']
        jam = session['jam']
        harga_tiket = session['harga_tiket']
        jumlah_kursi = session['jumlah_kursi_yang_di_booking']

        tanggal_keberangkatan = session['tanggal_keberangkatan']
        tanggal_keberangkatan = tanggal_keberangkatan[4:17]
        day = tanggal_keberangkatan[:3]
        month = tanggal_keberangkatan[3:7]
        year = tanggal_keberangkatan[7:12]

        tanggal_keberangkatan = tanggal_keberangkatan

        rute_user_id = db.session.query(Rute.user_id).join(User).filter(Rute.id_rute == rute_id).first()[0]
        nomor_telepon_user_PO = db.session.query(User.nomor_telepon).filter_by(id=rute_user_id).first()[0]

        # get invoice number
        def generator_random(size=6, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for x in range(size))

        generate_invoice = 'TK' + generator_random() + 'INV'
        kode_pembeli = generate_invoice
        session['KODE_PEMBELI'] = kode_pembeli
        # /get invoice number

        # get current date
        import time
        tanggal_pemesanan = time.strftime("%d/%m/%Y")
        tanggal_pemesanan_untuk_admin = time.strftime("%Y-%m-%d %H:%M:%S")
        session['TANGGAL_PEMESANAN'] = tanggal_pemesanan
        session['TANGGAL_PEMESANAN_UNTUK_ADMIN'] = tanggal_pemesanan_untuk_admin
        tanggal_pemesanan = session['TANGGAL_PEMESANAN']
        tanggal_pemesanan_untuk_admin = session['TANGGAL_PEMESANAN_UNTUK_ADMIN']
        # /get current date

        if request.method == "POST":

            kode_pemesanan = kode_pembeli
            session['kode_pemesanan'] = kode_pemesanan
            po_name = nama_po
            nama_pemesan = nama_pemesan
            email_pemesan = email
            nomor_telepon_pemesan = nomor_telepon
            title_penumpang = title_penumpang
            nama_penumpang = nama_penumpang
            tanggal_lahir_penumpang = tanggal_lahir
            tanggal_pesanan_tiket = tanggal_pemesanan_untuk_admin
            jadwal_berangkat = tanggal_keberangkatan
            jumlah_kursi_yang_di_booking = jumlah_kursi
            harga_total = session['harga_total']
            status_pembayaran = status

            message_to_user_PO = 'Ada yang memesan tiket dengan kode ' + kode_pemesanan + ' atas nama ' + nama_pemesan + \
                                 ' dan jumlah kursi yang di booking sebanyak ' + str(jumlah_kursi_yang_di_booking) + \
                                 ' dan harga totalnya adalah ' + 'Rp.' + str(harga_total) + ',00' + ', jadwal keberangkatan nya adalah ' + \
                                 ' pada tanggal ' + tanggal_keberangkatan + ' jam ' + jam

            message_to_admin = 'Ada yang memesan tiket dengan kode ' + kode_pemesanan

            subject_to_pemesan = '---Nadia Tiket---'

            msg_to_pemesan = 'Terima kasih ' + nama_pemesan + ' telah memesan tiket melalui layanan kami,' \
                                                                  ' Silahkan melakukan pembayaran ke rekening berikut 012301230123 a/n Nadia Tiket,' \
                                                                  ' sesuai dengan jumlah tiket yang Anda pesan, yaitu ' + \
                                 str(jumlah_kursi_yang_di_booking) + ' dan total harga nya adalah ' + 'Rp.' + str(harga_total) + ',00'

            msg_to_admin = 'Ada yang memesan tiket ' + str(jumlah_kursi_yang_di_booking) + ' kursi ' + \
                           ' dan harga totalnya adalah ' + 'Rp.' + str(harga_total) + ',00'


            ##################################
            ######-->/ TWILIO ########
            ##################################
            ############################ SMS for user PO ##########################
            # for user notifications
            ## Your Account SID from twilio.com/console
            account_sid_user = TWLIO_ACCOUNT_SID_UPGRADED_FOR_USER
            # # # # Your Auth Token from twilio.com/console
            auth_token_user = TWLIO_AUTH_TOKEN_UPGRADED_FOR_USER
            # # #
            sms_client = Client(account_sid_user, auth_token_user)
            # # #
            nomor_telepon_pemesan = nomor_telepon
            message_pemesan = sms_client.messages.create(
                to=nomor_telepon_user_PO,
                from_="+12014307127",   # this upgraded number
                body=message_to_user_PO)
            # #
            ######-->/ TWILIO ########
            ##################################


            ###################################
            ##########-- GMAIL --##############
            ###################################

            CLIENT_SECRET_FILE = 'web_app/api/client_secret.json'

            # Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
            OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'

            # Location of the credentials storage file
            STORAGE = Storage('web_app/api/gmail.storage')

            # Start the OAuth flow to retrieve credentials
            flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
            http = httplib2.Http()

            # Try to retrieve credentials from storage or run the flow to generate them
            credentials = STORAGE.get()
            if credentials is None or credentials.invalid:
                credentials = run_flow(flow, STORAGE, http=http)

            # Authorize the httplib2.Http object with our credentials
            http = credentials.authorize(http)

            # Build the Gmail service from discovery
            gmail_service = build('gmail', 'v1', http=http)

            # TO PEMESAN
            # create a message to send
            message_to_pemesan = MIMEText(msg_to_pemesan)
            message_to_pemesan['to'] = email_pemesan
            message_to_pemesan['from'] = "nadiaazizah7676@gmail.com"
            message_to_pemesan['subject'] = subject_to_pemesan
            raw_to_pemesan = base64.urlsafe_b64encode(message_to_pemesan.as_bytes())
            raw_to_pemesan = raw_to_pemesan.decode()
            body_to_pemesan = {'raw': raw_to_pemesan}

            # send it
            try:
                message_to_pemesan = (
                    gmail_service.users().messages().send(userId="me", body=body_to_pemesan).execute())
                print('Message Id: %s' % message_to_pemesan['id'])
                print(message_to_pemesan)
            except Exception as error:
                print('An error occurred: %s' % error)

            # TO ADMIN
            # create a message to send
            message_to_admin = MIMEText(msg_to_admin)
            message_to_admin['to'] = "nadiaazizah1111@gmail.com"
            message_to_admin['from'] = "nadiaazizah7676@gmail.com"
            message_to_admin['subject'] = "Ada yang pesan tiket"
            raw_to_admin = base64.urlsafe_b64encode(message_to_admin.as_bytes())
            raw_to_admin = raw_to_admin.decode()
            body_to_admin = {'raw': raw_to_admin}

            # send it
            try:
                message_to_admin = (
                    gmail_service.users().messages().send(userId="me", body=body_to_admin).execute())
                print('Message Id: %s' % message_to_admin['id'])
                print(message_to_admin)
            except Exception as error:
                print('An error occurred: %s' % error)

            ###################################
            ##########-- GMAIL --##############
            ###################################


            insert_to_db = Data_pesanan(rute_id ,kode_pemesanan, po_name, nama_pemesan, email_pemesan, nomor_telepon_pemesan,
                                        title_penumpang,nama_penumpang, tanggal_lahir_penumpang, tanggal_pesanan_tiket,
                                        jadwal_berangkat, jumlah_kursi_yang_di_booking, harga_total, status_pembayaran)
            db.session.add(insert_to_db)
            db.session.commit()

            db.session.query(Rute).filter_by(id_rute=rute_id).update({Rute.jumlah_kursi: Rute.jumlah_kursi - jumlah_kursi_yang_di_booking})
            db.session.commit()


            return render_template('invoice.html', KODE_INVOICE=kode_pemesanan, TANGGAL_PESANAN=tanggal_pesanan_tiket,
                                   DARI=dari, TUJUAN=tujuan, JUMLAH_BANGKU=jumlah_kursi_yang_di_booking, TANGGAL_BERANGKAT=jadwal_berangkat, JAM=jam,
                                   HARGA_TIKET=harga_tiket, HARGA_TOTAL=harga_total)

        return render_template('payment.html')

    @app.route('/invoice', methods= ['POST', 'GET'])
    def invoice():
        kode_pemesanan = session['kode_pemesanan']
        tanggal_pesanan_tiket = session['TANGGAL_PEMESANAN']
        dari = session['dari']
        tujuan = session['tujuan']
        jumlah_kursi = session['jumlah_kursi_yang_di_booking']
        tanggal_keberangkatan = session['tanggal_keberangkatan']
        tanggal_keberangkatan = tanggal_keberangkatan[4:17]
        jam = session['jam']
        harga_tiket = session['harga_tiket']
        harga_total = session['harga_total']

        if request.method == "POST":
            data_pdf =  render_template('invoice.html', KODE_INVOICE=kode_pemesanan, TANGGAL_PESANAN=tanggal_pesanan_tiket,
                                   DARI=dari, TUJUAN=tujuan, JUMLAH_BANGKU=jumlah_kursi,
                               TANGGAL_BERANGKAT=tanggal_keberangkatan, JAM=jam, HARGA_TIKET=harga_tiket, HARGA_TOTAL=harga_total)
            css = "web_app/static/style.css"
            pdf = pdfkit.from_string(data_pdf, False, css=css)
            response = make_response(pdf)
            response.headers['Content-Type'] = 'applications/pdf'
            response.headers['Content-Disposition'] = 'inline; filename=invoice.pdf'
            return response


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginFormView(request.form)
        if request.method == 'POST':
            if form.validate_on_submit():
                session['email'] = request.form['email']
                user = User.query.filter_by(email=form.email.data).first()
                if verify_password(user.password, form.password.data):
                    user.authenticated = True
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    login_user(user, remember=form.remember.data)
                    return redirect(url_for('dashboard'))
                else:
                    return '<h1>Invalid username or password</h1>'

        return render_template('login.html', form=form)

    @app.route('/dashboard')
    @login_required
    def dashboard():
        if 'email' in session:
            nama_po = current_user.po_name
            all_user_data = Rute.query.filter_by(user_id=current_user.id)
            return render_template('dashboard.html', rute=all_user_data, NAMA_PO=nama_po)
        else:
            return redirect(url_for('index'))

    @app.route('/user_profile')
    @login_required
    def user_profile():
        return render_template('user_profile.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/add', methods=['GET', 'POST'])
    @login_required
    def tambah_rute():
        form = AddRuteForm(request.form)
        nama_po = current_user.po_name
        if request.method == 'POST':
            if form.validate_on_submit():
                add_jam = request.form['jam']
                new_rute = Rute(form.dari.data, form.tujuan.data, form.ongkos.data,
                                form.tanggal_keberangkatan.data, add_jam, form.jumlah_kursi.data,
                                current_user.id, current_user.po_id, False)
                db.session.add(new_rute)
                db.session.commit()
                return redirect(url_for('dashboard'))

        return render_template('tambah_rute.html', form=form,  NAMA_PO=nama_po)

    @app.route('/rute/<rute_id>')
    def rute_details(rute_id):
        rute_with_user = db.session.query(Rute, PO).join(PO).filter(Rute.id_rute == rute_id).first()
        if rute_with_user is not None:
            if rute_with_user.Rute.is_public:
                return render_template('rute_detail.html', rute=rute_with_user)
            else:
                if current_user.is_authenticated and rute_with_user.Rute.user_id == current_user.id:
                    return render_template('rute_detail.html', rute=rute_with_user)
                # else:
                #    flash('Error! Incorrect permissions to access this mantan.', 'error')
        else:
            flash('Error! Recipe does not exist.', 'error')
        return redirect(url_for('index'))

    @app.route('/rute_delete/<rute_id>')
    def rute_delete(rute_id):
        data = db.session.query(Rute, User).join(User).filter(Rute.id_rute == rute_id).first()
        if data.Rute.is_public:
            return render_template('rute_detail.html', rute=data)
        else:
            try:
                if current_user.is_authenticated and data.Rute.user_id == current_user.id:
                    data = Rute.query.filter_by(id_rute=rute_id).first()
                    db.session.delete(data)
                    db.session.commit()
            except:
                return 'Tidak bisa delete data rute, karena data rute sedang digunakan'
        return redirect(url_for('dashboard'))

    @app.route('/rute_edit/<rute_id>', methods=['GET', 'POST'])
    def rute_edit(rute_id):
        nama_po = current_user.po_name
        data = db.session.query(Rute, User).join(User).filter(Rute.id_rute == rute_id).first()
        form = EditRuteForm(request.form)
        if request.method == 'POST':
            if form.validate_on_submit():
                if current_user.is_authenticated and data.Rute.user_id == current_user.id:
                    data = Rute.query.filter_by(id_rute=rute_id).first()
                    new_dari = form.dari.data
                    new_tujuan = form.tujuan.data
                    new_ongkos= form.ongkos.data
                    new_tanggal_keberangkatan = form.tanggal_keberangkatan.data
                    new_jam = request.form['jam']
                    new_jumlah_kursi = form.jumlah_kursi.data
                    try:
                        data.dari = new_dari
                        data.tujuan = new_tujuan
                        data.ongkos = new_ongkos
                        data.tanggal_keberangkatan = new_tanggal_keberangkatan
                        data.jam = new_jam
                        data.jumlah_kursi = new_jumlah_kursi
                        db.session.commit()

                    except Exception as e:
                        return {'error': str(e)}
                return redirect(url_for('dashboard'))

        return render_template('edit_rute.html', form=form, rute=data, NAMA_PO=nama_po)


    return app