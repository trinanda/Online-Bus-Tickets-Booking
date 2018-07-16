from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from flask_security import RoleMixin, UserMixin
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()


class Jadwal(db.Model):
    __tablename__ = 'jadwal'
    id_jadwal = Column(Integer, primary_key=True)
    hari = Column(String)
    jam = Column(String)

class Rute(db.Model):
    __tablename__ = 'rute'
    id_rute = Column(Integer, primary_key=True)
    kode_rute = Column(String)
    tujuan = Column(String)
    ongkos = Column(Integer)

    def __repr__(self):
        return self.tujuan

class Data_pesanan(db.Model):
    __tablename__ = 'data pesanan'
    id_pemesan = Column(Integer, primary_key=True)
    kode_pemesan = Column(String, unique=True)
    nama_pemesan = Column(String)
    nomor_telepon = Column(Numeric)
    alamat = Column(String)

    rute_id = Column(Integer, ForeignKey(Rute.id_rute), nullable=False, default=1)
    # id_rute = relationship('Rute', backref=backref('Link dari Data Pesanan', uselist=False))

    tanggal_pemesanan = Column(DateTime)
    tanggal_ingin_berangkat = Column(DateTime)
    jam_ingin_berangkat = Column(String)

    harga_tiket = Column(Integer)

    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    status_pembayaran = db.Column(db.Enum(PENDING, CONFIRMED, REJECTED, name='status_pembayaran', default=PENDING))

    def __init__(self,  id_rute, kode_pemesan, nama_pemesan, nomor_telepon, alamat_anda,
                 tanggal_pemesanan, tanggal_ingin_berangkat,
                 jam_ingin_berangkat, harga_tiket, status_pembayaran):
        self.rute_id = id_rute
        self.kode_pemesan = kode_pemesan
        self.nama_pemesan = nama_pemesan
        self.nomor_telepon = nomor_telepon
        self.alamat = alamat_anda
        self.tanggal_pemesanan = tanggal_pemesanan
        self.tanggal_ingin_berangkat = tanggal_ingin_berangkat
        self.jam_ingin_berangkat = jam_ingin_berangkat
        self.harga_tiket = harga_tiket
        self.status_pembayaran = status_pembayaran

    def __repr__(self):
        return self.id_rute

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