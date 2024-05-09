from datetime import datetime

from flask import Blueprint, jsonify, request
from sqlalchemy import func, case, distinct
from app import db
from .goodsModel import Goods

goods_manager = Blueprint('goods_manager', __name__)

@goods_manager.route('/goods', methods=['GET'])
def get_all_goods():
    goods = Goods.query.all()
    return jsonify([good.to_dict() for good in goods])

@goods_manager.route('/goods/<int:id>', methods=['GET'])
def get_good(id):
    good = Goods.query.get(id)
    if good:
        return jsonify(good.to_dict())
    else:
        return jsonify({'error': 'Not found'}), 404


@goods_manager.route('/goods', methods=['POST'])
def create_good():
    good = request.json
    name = good.get('name')
    quantity = good.get('quantity')
    unit = good.get('unit')
    unit_price = good.get('unit_price')
    supplier = good.get('supplier')
    description = good.get('description')

    expiration_date_string = good.get('expiration_date')
    expiration_date = datetime.strptime(expiration_date_string, "%Y-%m-%dT%H:%M:%S.%fZ").date()
    today = datetime.now().date()
    difference = expiration_date - today
    expiration_days = difference.days

    total_value = quantity * unit_price

    good_entry = Goods(name=name, quantity=quantity, unit=unit, unit_price=unit_price,
                       expiration_date=expiration_days, supplier=supplier, description=description,
                       total_value=total_value)

    db.session.add(good_entry)
    db.session.commit()

    return jsonify({'message': 'Created successfully'}), 201



@goods_manager.route('/goods/<int:id>', methods=['PUT'])
def update_good(id):
    data = request.json
    good = Goods.query.get(id)

    if good:
        expiration_date_str = data.get('expiration_date')
        if expiration_date_str:
            expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d')
            days_difference = (expiration_date - datetime.now().date()).days
            good.expiration_date = days_difference
        else:
            return jsonify({'error': 'Expiration date is missing in the request'}), 400

        # Update other attributes of the good
        for key, value in data.items():
            if key != 'expiration_date':
                setattr(good, key, value)

        db.session.commit()
        return jsonify({'message': 'Updated successfully'})
    else:
        return jsonify({'error': 'Good not found'}), 404


@goods_manager.route('/goods/<int:id>', methods=['DELETE'])
def delete_good(id):
    good = Goods.query.get(id)
    if good:
        db.session.delete(good)
        db.session.commit()
        return jsonify({'message': 'Deleted successfully'})
    else:
        return jsonify({'error': 'Not found'}), 404

@goods_manager.route('/goods_stats', methods=['GET'])
def get_all_goods_stats():
    goods_stats = db.session.query(
        Goods.name,
        Goods.supplier,
        Goods.unit_price,
        Goods.unit,
        func.sum(Goods.quantity).label('quantity'),
        func.sum(Goods.total_value).label('total_value'),
        func.min(Goods.expiration_date).label('expiration_date'),
        func.max(Goods.update_time).label('update_time'),
        case((func.count(Goods.description) > 0, func.max(Goods.description)), else_='')
        .label('description')
    ).group_by(Goods.name, Goods.supplier, Goods.unit_price, Goods.unit).all()

    results = []
    for stat in goods_stats:
        result = {
            'name': stat.name,
            'supplier': stat.supplier,
            'unit_price': stat.unit_price,
            'unit': stat.unit,
            'quantity': stat.quantity,
            'total_value': stat.total_value,
            'expiration_date': stat.expiration_date,
            'update_time': stat.update_time.strftime('%Y-%m-%d') if stat.update_time else None,
            'description': stat.description
        }
        results.append(result)

    return jsonify(results)

@goods_manager.route('/delete_goods', methods=['POST','GET'])
def delete_goods():
    data = request.get_json()
    name = data.get('name')
    supplier = data.get('supplier')
    unit_price = data.get('unit_price')
    unit = data.get('unit')

    if not all([name, supplier, unit_price, unit]):
        return jsonify({'status': 'error', 'message': 'Missing key information for deletion'}), 400

    Goods.query.filter(
        Goods.name == name,
        Goods.supplier == supplier,
        Goods.unit_price == unit_price,
        Goods.unit == unit
    ).delete(synchronize_session='fetch')
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'All related records have been deleted'})
