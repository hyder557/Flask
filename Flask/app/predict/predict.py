# 在 app/predict/predict.py
from flask import Blueprint, request, jsonify
import numpy as np
import joblib

prediction = Blueprint('prediction', __name__)

# 加载模型和缩放器
scaler = joblib.load('scaler.pkl')
knn_death = joblib.load('knn_death.pkl')
knn_injury = joblib.load('knn_injury.pkl')

@prediction.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = np.array([
            [data['magnitude'],
             data['intensity'],
             data['population_density'],
             int(data['earthquake_forecast']),
             int(data['occurrence_time'])]
        ])

        # 缩放特征
        scaled_features = scaler.transform(features)

        # 使用模型进行预测
        death_rate = knn_death.predict(scaled_features)[0]
        injury_rate = knn_injury.predict(scaled_features)[0]

        return jsonify({
            'predicted_death_rate': death_rate,
            'predicted_injury_rate': injury_rate
        })
    except Exception as e:
        return jsonify({'error': str(e)})
