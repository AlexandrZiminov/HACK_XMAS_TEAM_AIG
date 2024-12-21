from datetime import datetime
from domain import limitStorage
from domain.transaction import Transaction
import numpy as np


def filter_source(tx: Transaction, data: np.ndarray, limits: limitStorage):
    """
    Фильтруем провайдеров по валюте, времени и лимитам.
    """
    # 1st filter by currency
    res = _by_currency(tx, data)

    # 2nd filter by time
    res = _by_time(tx, res)

    # 3rd filter by limits
    res = _by_limit(tx, res, limits)

    return res


def _by_currency(tx: Transaction, data: np.ndarray):
    """
    Фильтрует провайдеров по валюте и диапазону суммы.
    """
    filtered_data = data[
        (data['CURRENCY'] == tx.cur) & (data['MIN_SUM'] <= tx.amount) & (data['MAX_SUM'] >= tx.amount)
        ]
    return filtered_data


def _by_time(tx: Transaction, data: np.ndarray):
    """
    Фильтрует провайдеров по времени действия их параметров.
    """
    tx_creation_time = datetime.strptime(tx.eventTimeRes, '%Y-%m-%d %H:%M:%S')
    filtered_data_by_time = data[
        [datetime.strptime(row['TIME'], '%Y-%m-%d %H:%M:%S') <= tx_creation_time for row in data]
    ]

    # Преобразуем TIME обратно в формат datetime для сортировки
    filtered_data_by_time['TIME'] = np.array(
        [datetime.strptime(row, '%Y-%m-%d %H:%M:%S') for row in filtered_data_by_time['TIME']]
    )

    unique_ids = np.unique(filtered_data_by_time['ID'])

    filtered_data = []
    for unique_id in unique_ids:
        filtered = filtered_data_by_time[filtered_data_by_time['ID'] == unique_id]
        max_time_index = np.argmax(filtered['TIME'])  # Берём запись с максимальным временем
        filtered_data.append(filtered[max_time_index])

    filtered_data = np.array(filtered_data, dtype=filtered_data_by_time.dtype)

    return filtered_data


def _by_limit(tx: Transaction, data: np.ndarray, limits: limitStorage):
    """
    Фильтрует провайдеров по лимитам (LIMIT_MAX, LIMIT_BY_CARD).
    """
    filtered_rows = []

    for row in data:
        provider_id = row['ID']
        provider_limits = limits.get(provider_id)

        if not provider_limits:
            continue  # Пропускаем, если провайдер не найден

        current_total = provider_limits['current_total']
        limit_max = provider_limits['limit_max']
        limit_by_card = provider_limits['limit_by_card']

        # Проверяем превышение LIMIT_MAX
        if current_total + tx.amount > limit_max:
            continue

        # Проверяем LIMIT_BY_CARD, если платёж по карте и лимит существует
        if tx.payment == "card" and limit_by_card > 0:
            if tx.amount > limit_by_card:
                continue

        filtered_rows.append(row)

    return np.array(filtered_rows, dtype=data.dtype)
