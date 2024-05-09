import re

from flask import Blueprint, jsonify, request
from sqlalchemy import func

from app import db
from .demandModel import Demand
from ..goodsManage.goodsModel import Goods

demand_manager = Blueprint('demand_manager', __name__)

# 创建需求
@demand_manager.route('/demands', methods=['POST'])
def create_demand():
    data = request.json
    demand = Demand(
        name=data.get('name'),
        contact=data.get('contact'),
        location=data.get('location'),
        description=data.get('description'),
        resources=data.get('resources')
    )
    db.session.add(demand)
    db.session.commit()
    return jsonify({'message': 'Demand created successfully'})

# 获取所有需求
@demand_manager.route('/demands', methods=['GET'])
def get_demands():
    demands = Demand.query.all()
    demands_list = [demand.to_dict() for demand in demands]
    return jsonify(demands_list)

# 获取单个需求
@demand_manager.route('/demands/<int:demand_id>', methods=['GET'])
def get_demand(demand_id):
    demand = Demand.query.get(demand_id)
    if not demand:
        return jsonify({'message': 'Demand not found'})
    return jsonify(demand.to_dict())

# 更新需求
@demand_manager.route('/demands/<int:demand_id>', methods=['PUT'])
def update_demand(demand_id):
    demand = Demand.query.get(demand_id)
    if not demand:
        return jsonify({'message': 'Demand not found'})

    data = request.json
    demand.name = data['name']
    demand.contact = data['contact']
    demand.location = data['location']
    demand.description = data['description']
    demand.resources = data['resources']
    demand.status = data['status']

    db.session.commit()
    return jsonify({'message': 'Demand updated successfully'})

# 删除需求
@demand_manager.route('/demands/<int:demand_id>', methods=['DELETE'])
def delete_demand(demand_id):
    demand = Demand.query.get(demand_id)
    if not demand:
        return jsonify({'message': 'Demand not found'})
    db.session.delete(demand)
    db.session.commit()
    return jsonify({'message': 'Demand deleted successfully'})

#统计计数
@demand_manager.route('/unique_demands',methods=['GET'])
def get_unique_demands():
    unique_demands = db.session.query(
        Demand.resources,
        Demand.location,
        func.min(Demand.description).label('description')
    ).filter(Demand.resources.isnot(None), Demand.location.isnot(None)) \
    .group_by(Demand.resources, Demand.location) \
    .all()

    demands = []
    for resources, location, description in unique_demands:
        demand = {
            'resources': resources,
            'location': location,
            'description': description
        }
        demands.append(demand)

    return jsonify(demands)

    return demands


@demand_manager.route('/showdemands', methods=['GET','POST'])
def get_all_demands():
    # 通过去重获取 demands
    demand_query = db.session.query(
        Demand.resources,
        Demand.location,
        func.min(Demand.description).label('description')
    ).group_by(Demand.resources, Demand.location).all()

    demands_with_goods = []
    for demand in demand_query:
        goods_data = get_related_goods(demand.resources)
        demands_with_goods.append({
            'resources': demand.resources,
            'location': demand.location,
            'description': demand.description,
            'goods': goods_data
        })

    return jsonify(demands_with_goods)

def get_related_goods(resources):
    keywords = sorted(set(re.split(r'[\s,]+', resources)), key=len, reverse=True)
    goods = []
    for keyword in keywords:
        goods.extend(Goods.query.filter(Goods.name.contains(keyword)).all())
    return [{
        'name': g.name,
        'quantity': g.quantity,
        'unit': g.unit,
        'unit_price': g.unit_price,
        'expiration_date': g.expiration_date,
        'supplier': g.supplier,
        'update_time': g.update_time,
        'description': g.description
    } for g in goods]
