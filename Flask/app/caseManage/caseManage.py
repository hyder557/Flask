from flask import Blueprint, jsonify, request
from .caseModel import EarthquakeCase
from app import db

case_manager = Blueprint('case_manager', __name__)

@case_manager.route('/cases', methods=['GET'])
def get_cases():
    cases = EarthquakeCase.query.all()
    results = []
    for case in cases:
        results.append({
            'id': case.id,
            'occurrence_time': case.occurrence_time,
            'magnitude': case.magnitude,
            'intensity': case.intensity,
            'population_density': case.population_density,
            'earthquake_forecast': case.earthquake_forecast,
            'death_rate': case.death_rate,
            'injury_rate': case.injury_rate
        })
    return jsonify(results)

@case_manager.route('/cases', methods=['POST'])
def create_case():
    data = request.json
    case = EarthquakeCase(
        occurrence_time=data['occurrence_time'],
        magnitude=data['magnitude'],
        intensity=data['intensity'],
        population_density=data['population_density'],
        earthquake_forecast=data['earthquake_forecast'],
        death_rate=data['death_rate'],
        injury_rate=data['injury_rate']
    )
    db.session.add(case)
    db.session.commit()
    return jsonify({'message': 'Case created successfully'})

@case_manager.route('/cases/<int:case_id>', methods=['PUT'])
def update_case(case_id):
    case = EarthquakeCase.query.get(case_id)
    if not case:
        return jsonify({'message': 'Case not found'})
    data = request.json
    case.occurrence_time = data['occurrence_time']
    case.magnitude = data['magnitude']
    case.intensity = data['intensity']
    case.population_density = data['population_density']
    case.earthquake_forecast = data['earthquake_forecast']
    case.death_rate = data['death_rate']
    case.injury_rate = data['injury_rate']
    db.session.commit()
    return jsonify({'message': 'Case updated successfully'})

@case_manager.route('/cases/<int:case_id>', methods=['DELETE'])
def delete_case(case_id):
    case = EarthquakeCase.query.get(case_id)
    if not case:
        return jsonify({'message': 'Case not found'})
    db.session.delete(case)
    db.session.commit()
    return jsonify({'message': 'Case deleted successfully'})