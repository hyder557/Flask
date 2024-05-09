# 在 app/predict/train.py
from flask import current_app
from sqlalchemy import create_engine, text
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler
import joblib

def initialize_model():
    # 数据库连接，使用 Flask 应用的配置
    engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])

    # 从数据库读取数据
    query = text("SELECT magnitude, intensity, population_density, earthquake_forecast, occurrence_time, death_rate, injury_rate FROM earthquake_case")
    with engine.connect() as conn:
        result = conn.execute(query)
        rows = result.fetchall()

    # 将查询结果转换为DataFrame
    df = pd.DataFrame(rows, columns=result.keys())

    # 准备特征和目标
    X = df[['magnitude', 'intensity', 'population_density', 'earthquake_forecast', 'occurrence_time']].values
    y_death = df['death_rate'].values
    y_injury = df['injury_rate'].values

    # 数据归一化
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    # 训练 KNN 模型
    knn_death = KNeighborsRegressor(n_neighbors=1)
    knn_death.fit(X_scaled, y_death)
    knn_injury = KNeighborsRegressor(n_neighbors=1)
    knn_injury.fit(X_scaled, y_injury)

    # 保存模型和缩放器
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(knn_death, 'knn_death.pkl')
    joblib.dump(knn_injury, 'knn_injury.pkl')

    print("Models initialized and saved")
