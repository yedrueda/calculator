from flask import Blueprint, request, jsonify
from models.database import db
from models.mrp_models import (
    Producto,
    Material,
    Inventario,
    OrdenProduccion,
    ProductoMaterial
)
from datetime import datetime

mrp_bp = Blueprint('mrp', __name__)

# MRP Core Endpoints
@mrp_bp.route('/planificar', methods=['POST'])
def planificar_mrp():
    try:
        data = request.json
        requerimientos = {}
        
        for orden in data['ordenes']:
            producto = Producto.query.get(orden['producto_id'])
            if not producto:
                continue
                
            for material_rel in producto.materiales:
                material_id = material_rel.material_id
                requerimientos[material_id] = requerimientos.get(material_id, 0) + (material_rel.cantidad * orden['cantidad'])
        
        pedidos_sugeridos = []
        for material_id, cantidad_bruta in requerimientos.items():
            inventario = Inventario.query.get(material_id)
            if not inventario:
                continue
                
            cantidad_necesaria = max(cantidad_bruta - inventario.stock, 0)
            
            if cantidad_necesaria > 0:
                pedidos_sugeridos.append({
                    'material_id': material_id,
                    'cantidad': float(cantidad_necesaria),
                    'stock_actual': float(inventario.stock),
                    'stock_minimo': float(inventario.stock_minimo)
                })
        
        return jsonify({
            'requerimientos': requerimientos,
            'pedidos_sugeridos': pedidos_sugeridos
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Inventory Endpoints
@mrp_bp.route('/inventario', methods=['GET'])
def get_inventario():
    try:
        inventario = Inventario.query.all()
        return jsonify([{
            'material_id': item.material_id,
            'stock': float(item.stock),
            'stock_minimo': float(item.stock_minimo)
        } for item in inventario])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mrp_bp.route('/inventario/<int:material_id>', methods=['PUT'])
def actualizar_inventario(material_id):
    try:
        data = request.json
        inventario = Inventario.query.get(material_id)
        
        if not inventario:
            return jsonify({'error': 'Registro de inventario no encontrado'}), 404
            
        inventario.stock = data.get('stock', inventario.stock)
        inventario.stock_minimo = data.get('stock_minimo', inventario.stock_minimo)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Inventario actualizado',
            'inventario': {
                'material_id': inventario.material_id,
                'stock': float(inventario.stock),
                'stock_minimo': float(inventario.stock_minimo)
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Material Endpoints
@mrp_bp.route('/materiales', methods=['GET'])
def get_materiales():
    try:
        materiales = Material.query.all()
        return jsonify([{
            'id': m.id,
            'nombre': m.nombre,
            'unidad': m.unidad
        } for m in materiales])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Production Orders Endpoints
@mrp_bp.route('/ordenes-produccion', methods=['POST'])
def crear_orden_produccion():
    try:
        data = request.json
        nueva_orden = OrdenProduccion(
            producto_id=data['producto_id'],
            cantidad=data['cantidad'],
            fecha_requerida=datetime.strptime(data['fecha_requerida'], '%Y-%m-%d'),
            estado='pendiente'
        )
        
        db.session.add(nueva_orden)
        db.session.commit()
        
        return jsonify({
            'message': 'Orden de producción creada',
            'orden_id': nueva_orden.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@mrp_bp.route('/ordenes-produccion', methods=['GET'])
def get_ordenes_produccion():
    try:
        ordenes = OrdenProduccion.query.all()
        return jsonify([{
            'id': o.id,
            'producto_id': o.producto_id,
            'cantidad': o.cantidad,
            'fecha_requerida': o.fecha_requerida.strftime('%Y-%m-%d'),
            'estado': o.estado
        } for o in ordenes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    