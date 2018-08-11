import flask_admin
from flask import Flask, render_template, request, session, url_for
from flask_admin import Admin, helpers as admin_helpers
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_security import SQLAlchemyUserDatastore, Security
from flask_security.utils import verify_password, login_user
from werkzeug.utils import redirect

from web_app.form import LoginFormView
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
        tujuan = 'Padang'
        tanggal_keberangkatan = '2018-08-11'
        car_bis = db.session.query(Rute.id_rute, Rute.tujuan, Rute.ongkos, Rute.tanggal_keberangkatan, Rute.jam).\
            filter(Rute.tujuan == tujuan, Rute.tanggal_keberangkatan == tanggal_keberangkatan).first()
        print('test', car_bis)

        return render_template('halaman_utama.html')


    @app.route('/pilih_bis')
    def pilih_bis():

        return render_template('pilih_bis.html')

    @app.route('/check')
    def check():
        return render_template('pilih_bis.html')

    @app.route('/kontak')
    def kontak():
        return render_template('kontak.html')

    @app.route('/payment')
    def payment():
        return render_template('payment.html')

    @app.route('/invoice')
    def success():
        return render_template('invoice.html')

    @app.route('/form')
    def form():
        return render_template('form_pesan_tiket.html')

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




    return app