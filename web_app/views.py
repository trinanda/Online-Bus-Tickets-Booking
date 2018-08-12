from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask import url_for, abort, redirect, request

class UserAkses(ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('user'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


class AdminAkses(ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))



class Data_pesananView(AdminAkses):
    column_list = ('kode_pemesanan', 'po_name', 'nama_pemesan', 'email_pemesan', 'nomor_telepon_pemesan', 'title_penumpang',
                   'nama_penumpang', 'tanggal_lahir_penumpang', 'tanggal_pesanan_tiket', 'jadwal_berangkat',
                   'jumlah_kursi_yang_di_booking', 'harga_total', 'status_pembayaran')

# Create customized model view class
class MyModelView(AdminAkses):
    pass

class RuteView(AdminAkses):
    pass

class PoView(AdminAkses):
    pass

