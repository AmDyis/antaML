import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from catboost import CatBoostRegressor, Pool

# Загрузка данных о средней температуре и координатах станций
dfMid = pd.read_excel('Средняя и коорды модель.xlsx', sheet_name='Лист1')
dfYear = pd.read_excel("Ежегодная.xlsx", sheet_name='Лист1')

# Заполнение пропущенных значений в данных о ежегодной температуре средними
dfYear.fillna(dfYear.mean(), inplace=True)

# Транспонирование данных и установка годов в качестве индекса
# print(dfYear)
dfYear = dfYear.T
dfYear.columns = dfYear.iloc[0]
dfYear = dfYear[1:]
dfYear = dfYear.astype(float)

# Создание модели K-средних
num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters, random_state=0)

# Кластеризация на координатах станций
cluster_labels = kmeans.fit_predict(dfMid[['Широта', 'Долгота', 'Высота над уровнем моря', 'средняя температура']])
dfMid["Cluster"] = cluster_labels

# Установка индекса 'станция' в DataFrame
dfMid.set_index('станция', inplace=True)


# Объединение данных
merged_df = dfYear.join(dfMid["Cluster"])
merged_df = merged_df.astype(float)
# print(merged_df)

# # Вывод результата
# print(merged_df.head())

# Разделение данных на обучающий и валидационный наборы
train_data, val_data, train_y, val_y = train_test_split(merged_df.drop(2022.0, axis=1), merged_df[2022.0], test_size=0.3)

# Создание объекта CatBoostRegressor
cat = CatBoostRegressor(iterations=150, depth=3, learning_rate=0.1, loss_function='RMSE', l2_leaf_reg=5, border_count=32, verbose=0)

# Преобразование данных в catboost.Pool
train_pool = Pool(data=train_data, label=train_y)
val_pool = Pool(data=val_data, label=val_y)

# Обучение модели
cat.fit(train_pool)

# Предсказания
# predictions = cat.predict(train_data)
# print("Предсказанные значения на обучающих данных:")
# print(predictions)
# print("Реальные значения на обучающих данных:")
# print(train_y)
#
# predictions = cat.predict(val_data)
# print("Предсказанные значения на валидационных данных:")
# print(predictions)
# print("Реальные значения на валидационных данных:")
# print(val_y)

future_years = range(2023, 2027)
for year in future_years:
    # Добавляем данные для нового года
    merged_df[year] = cat.predict(merged_df.drop(year - 1, axis=1))

    # Обучаем модель заново с учетом предсказанных значений
    train_data = merged_df.drop(year, axis=1)
    train_y = merged_df[year]

    train_pool = Pool(data=train_data, label=train_y)

    # Обучение модели
    cat.fit(train_pool)

# Вывод результата
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


merged_target = merged_df.copy()
merged_target.drop(columns=["Cluster"], inplace=True)
# print(merged_target)