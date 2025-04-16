from .database import db

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    materiales = db.relationship('ProductoMaterial', backref='producto')

class Material(db.Model):
    __tablename__ = 'materiales'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    unidad = db.Column(db.String(20), nullable=False)
    inventario = db.relationship('Inventario', uselist=False, backref='material')

class Inventario(db.Model):
    __tablename__ = 'inventario'
    material_id = db.Column(db.Integer, db.ForeignKey('materiales.id'), primary_key=True)
    stock = db.Column(db.Numeric(10,2), nullable=False)
    stock_minimo = db.Column(db.Numeric(10,2), nullable=False)

class OrdenProduccion(db.Model):
    __tablename__ = 'ordenes_produccion'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_requerida = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(20), nullable=False)

class ProductoMaterial(db.Model):
    __tablename__ = 'productos_materiales'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    material_id = db.Column(db.Integer, db.ForeignKey('materiales.id'))
    cantidad = db.Column(db.Integer, nullable=False)
    unidad = db.Column(db.String(20), nullable=False)
    material = db.relationship('Material', backref='materiales')
    inventario = db.relationship('Inventario', uselist=False, backref='materiales')
    orden_produccion = db.relationship('OrdenProduccion', uselist=False, backref='materiales')
    db.create_all()
    print('Base de datos inicializada')
# Compare this snippet from backend/routes/api.py:
# from flask import Blueprint, jsonify    