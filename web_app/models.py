from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, VARCHAR, Enum, Boolean, Date, Time
from flask_security import RoleMixin, UserMixin
from sqlalchemy.orm import relationship, backref


db = SQLAlchemy()

class PO(db.Model):
    __tablename__ = 'PO'
    id_po = Column(Integer, primary_key=True)
    nama_po = Column(String)

    def __repr__(self):
        return '{}'.format(self.nama_po)


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary=roles_users,
                            backref=backref('users', lazy='dynamic'))

    po_id = Column(Integer, ForeignKey(PO.id_po))
    po_name = relationship(PO)

    def __repr__(self):
        return '{}'.format(self.po_name)


class Rute(db.Model):
    __tablename__ = 'rute'
    id_rute = Column(Integer, primary_key=True)
    dari = Column(String)
    tujuan = Column(String)
    ongkos = Column(Integer)
    tanggal_keberangkatan = Column(Date)
    jam = Column(Time)

    user_id = Column(Integer, ForeignKey(User.id))
    po_id = Column(Integer, ForeignKey(PO.id_po))
    po_name = relationship(PO)

    is_public = Column(Boolean(), nullable=False)

    def __repr__(self):
        return self.tujuan

    def __init__(self, dari='', tujuan='', ongkos='', tanggal_keberangkatan='', jam='', id=1, po_id='', is_public=False):
        self.dari = dari
        self.tujuan = tujuan
        self.ongkos = ongkos
        self.tanggal_keberangkatan = tanggal_keberangkatan
        self.jam = jam
        self.user_id = id
        self.po_id = po_id
        self.is_public = is_public

class Data_pesanan(db.Model):
    __tablename__ = 'data pesanan'
    kode_pemesanan = Column(String, primary_key=True, unique=True)
    nama_pemesan = Column(String)
    email_pemesan = Column(VARCHAR)
    nomor_telepon_pemesan = Column(VARCHAR)
    title_penumpang = Column(String)
    nama_penumpang = Column(String)
    tanggal_lahir_penumpang = Column(Date)
    tanggal_pesanan_tiket = Column(DateTime)
    jadwal_berangkat = Column(Date)
    jumlah_kursi_yang_di_booking = Column(Integer)
    harga_total = Column(Integer)

    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    status_pembayaran = Column(Enum(PENDING, CONFIRMED, REJECTED, name='status_pembayaran', default=PENDING))

    rute_id = Column(Integer, ForeignKey(Rute.id_rute))
    po_id = Column(Integer, ForeignKey(PO.id_po))

    def __init__(self, rute_id, kode_pemesanan, nama_pemesan, email_pemesan, nomor_telepon_pemesan, title_penumpang,
                 nama_penumpang, tanggal_lahir_penumpang, tanggal_pesanan_tiket, jadwal_berangkat,
                 jumlah_kursi_yang_di_booking, harga_total, status_pembayaran):

        self.rute_id = rute_id
        self.kode_pemesanan = kode_pemesanan
        self.nama_pemesan = nama_pemesan
        self.email_pemesan = email_pemesan
        self.nomor_telepon_pemesan = nomor_telepon_pemesan
        self.title_penumpang = title_penumpang
        self.nama_penumpang = nama_penumpang
        self.tanggal_lahir_penumpang = tanggal_lahir_penumpang
        self.tanggal_pesanan_tiket = tanggal_pesanan_tiket
        self.jadwal_berangkat = jadwal_berangkat
        self.jumlah_kursi_yang_di_booking = jumlah_kursi_yang_di_booking
        self.harga_total = harga_total
        self.status_pembayaran = status_pembayaran


