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
    tujuan = Column(String)
    ongkos = Column(Integer)
    jadwal_keberangkatan = Column(Date)
    jam = Column(Time)

    user_id = Column(Integer, ForeignKey(User.id))

    def __repr__(self):
        return self.tujuan


class Data_pesanan(db.Model):
    __tablename__ = 'data pesanan'
    kode_pemesanan = Column(String, primary_key=True, unique=True)
    nama_pemesan = Column(String)
    nomor_telepon = Column(VARCHAR)
    alamat = Column(String)
    tanggal_lahir = Column(DateTime)
    tanggal_pesanan_tiket = Column(DateTime)
    jadwal_berangkat = Column(DateTime)
    jumlah_kursi = Column(Integer)
    harga_total = Column(Integer)

    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    status_pembayaran = Column(Enum(PENDING, CONFIRMED, REJECTED, name='status_pembayaran', default=PENDING))

    rute_id = Column(Integer, ForeignKey(Rute.id_rute))
    po_id = Column(Integer, ForeignKey(PO.id_po))


