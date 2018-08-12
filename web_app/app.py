import flask_admin
from flask import Flask, render_template, request, session, url_for, flash
from flask_admin import Admin, helpers as admin_helpers
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from flask_security import SQLAlchemyUserDatastore, Security
from flask_security.utils import verify_password
from werkzeug.utils import redirect

from web_app.form import LoginFormView, AddRuteForm, EditRuteForm
from web_app.models import db, Data_pesanan, Role, User, Rute, PO
from web_app.views import Data_pesananView, MyModelView, RuteView, PoView

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

        urutan_tampilan = db.session.query(Rute.id_rute, Rute.dari, Rute.tujuan, Rute.ongkos, Rute.tanggal_keberangkatan, Rute.jam).\
            filter(Rute.tanggal_keberangkatan == tanggal_keberangkatan, Rute.dari == dari, Rute.tujuan == tujuan)



        session['jumlah_kursi_yang_di_booking'] = jumlah_kursi_yang_di_booking


        if request.method == "get":
            return render_template("pastikan_harga.html")

        return render_template('pilih_bis.html', URUTAN_TAMPILAN = urutan_tampilan)


    @app.route('/pastikan_harga', methods = ['GET', 'POST'])
    def pastikan_harga():
        id_rute = request.args.get('id_rute')
        jumlah_kursi_yang_di_booking = session['jumlah_kursi_yang_di_booking']

        harga = db.session.query(Rute.ongkos).filter(Rute.id_rute == id_rute).first()
        harga = harga[0]
        harga_total = int(harga) * int(jumlah_kursi_yang_di_booking)

        jam = db.session.query(Rute.jam).filter(Rute.id_rute == id_rute).first()
        jam = jam[0]
        tanggal_keberangkatan = db.session.query(Rute.tanggal_keberangkatan).filter(Rute.id_rute == id_rute).first()
        tanggal_keberangkatan = tanggal_keberangkatan[0]
        dari = db.session.query(Rute.dari).filter(Rute.id_rute == id_rute).first()
        dari = dari[0]
        tujuan = db.session.query(Rute.tujuan).filter(Rute.id_rute == id_rute).first()
        tujuan = tujuan[0]

        if request.method == "get":
            return render_template("kontak.html")

        return render_template("pastikan_harga.html", HARGA_TOTAL=harga_total, TANGGAL_KEBERANGKATAN=tanggal_keberangkatan,
                               JAM=jam, DARI=dari, TUJUAN=tujuan)

    @app.route('/kontak', methods = ['GET', 'POST'])
    def kontak():
        if request.method == "POST":
            nama_pemesan = request.form.get('nama_pemesan')
            email = request.form.get('email')
            nomor_telepon = request.form.get('nomor_telepon')

            title_penumpang = request.form.get('title_penumpang')
            nama_penumpang = request.form.get('nama_penumpang')
            tanggal_lahir = request.form.get('tanggal_lahir')

            return render_template("payment.html")

        return render_template('kontak.html')

    @app.route('/payment', methods = ['GET', 'POST'])
    def payment():
        if request.method == "get":
            return render_template('invoice.html')
        return render_template('payment.html')

    @app.route('/invoice')
    def invoice():
        return render_template('invoice.html')


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
                new_rute = Rute(form.dari.data, form.tujuan.data, form.ongkos.data,
                                form.tanggal_keberangkatan.data, form.jam.data,
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
                    new_dari_rute = form.dari.data
                    new_tujuan_rute = form.tujuan.data
                    new_ongkos_rute = form.ongkos.data
                    new_tanggal_keberangkatan_rute = form.tanggal_keberangkatan.data
                    try:
                        data.nama_rute = new_dari_rute
                        data.keterangan_rute = new_tujuan_rute
                        data.harga_rute = new_ongkos_rute
                        data.status = new_tanggal_keberangkatan_rute
                        db.session.commit()

                    except Exception as e:
                        return {'error': str(e)}
                return redirect(url_for('dashboard'))

        return render_template('rute_edit.html', form=form, rute=data, NAMA_PO=nama_po)


    return app