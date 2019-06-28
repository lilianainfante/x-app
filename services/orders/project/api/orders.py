# services/users/project/api/pedido.py
from flask import Blueprint, jsonify, request

from project.api.models import Customers
from project import db
from sqlalchemy import exc

orders_blueprint = Blueprint('orders', __name__)

@orders_blueprint.route('/orders/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@orders_blueprint.route('/customers', methods=['POST'])
def add_customer():
    post_data=request.get_json()
    response_object = {
        'status': 'fallo',
        'message': 'carga Invalida'
    }
    if not post_data:
        return jsonify(response_object), 400
    name=post_data.get('name')
    try:
        customer = Customers.query.filter_by(name=name).first()
        if not customer:
            db.session.add(Customers(name=name))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{name} was added!'
            return jsonify(response_object), 201
        else :
            response_object['messaje'] = 'Lo siento, el nombre ya existe'
            return jsonify(response_object), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(response_object), 400


@orders_blueprint.route('/curtomers/<customers_id>', methods=['GET'])
def get_single_custormer(customer_id):
    """Obtener detalles de usuario unico"""
    response_object = {
        'estado': 'fallo',
        'mensaje': 'EL usuario no existe'
    }
    try: 
        customer = Customers.query.filter_by(id=int(customer_id)).first()
        if not customer:
            return jsonify(response_object), 404
        else:
            response_object = {
                'estado': 'satisfactoria',
                'data': {
                    'id': customer.id,
                    'name': customer.name
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@orders_blueprint.route('/customers', methods=['GET'])
def get_all_customers():
    """Obteniendo todos los usuarios"""
    response_object = {
        'estado': 'satisfactorio',
        'data': {
            'customers': [customer.json() for customer in Customers.query.all()]
        }
    }
    return jsonify(response_object), 200