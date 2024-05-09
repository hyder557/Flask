from flask import request, jsonify, Blueprint

from app.goodsManage.goodsModel import Goods

task = Blueprint('task', __name__)

@task.route('/tasks',methods=['POST', 'GET'])
def create_tasks():
    demands = request.get_json()
    response_list = []

    for demand in demands:
        resources = demand.get('resources')
        goods_query = Goods.query.filter(Goods.name.like(f"%{resources}%")).all()
        goods_list = [{'id': g.id, 'name': g.name} for g in goods_query]  # 根据实际字段调整

        response_data = {
            'demand': demand,
            'goods': goods_list
        }
        response_list.append(response_data)

    return jsonify(response_list)