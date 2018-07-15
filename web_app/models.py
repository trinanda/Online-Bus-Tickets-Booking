from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from flask_security import RoleMixin, UserMixin

db = SQLAlchemy()

class Data_pesanan(db.Model):
    __tablename__ = 'data_pesanan'
    id_pemesan = Column(Integer, primary_key=True)
    kode_pemesan = Column(String, unique=True)
    nama_pemesan = Column(String)
    nomor_telepon = Column(Numeric)
    alamat = Column(String)
    tujuan = Column(String)
    tanggal_pemesanan = Column(DateTime)
    tanggal_ingin_berangkat = Column(DateTime)
    jam_ingin_berangkat = Column(String)

    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    status_pembayaran = db.Column(db.Enum(PENDING, CONFIRMED, REJECTED, name='status_pembayaran', default=PENDING))

    def __init__(self, kode_pemesan, nama_pemesan, nomor_telepon, alamat,
                 tujuan, tanggal_pemesanan, tanggal_ingin_berangkat, jam_ingin_berangkat, status_pembayaran):
        self.kode_pemesan = kode_pemesan
        self.nama_pemesan = nama_pemesan
        self.nomor_telepon = nomor_telepon
        self.alamat = alamat
        self.tujuan = tujuan
        self.tanggal_pemesanan = tanggal_pemesanan
        self.tanggal_ingin_berangkat = tanggal_ingin_berangkat
        self.jam_ingin_berangkat = jam_ingin_berangkat
        self.status_pembayaran = status_pembayaran


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
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email