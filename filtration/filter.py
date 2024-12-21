from datetime import datetime

from domain import limitStorage
from domain.transaction import Transaction
import numpy as np


def filter_source(tx: Transaction, data: np.ndarray, limits: limitStorage):
    # 1st filter _by_currency

    # 2nd filter byTime _by_time

    # byMaxLimit

    pass


def _by_currency(tx: Transaction, data: np.ndarray):
    filtered_data = data[
        (data['CURRENCY'] == tx.cur) & (data['MIN_SUM'] <= tx.amount) & (data['MAX_SUM'] >= tx.amount)]
    return filtered_data


def _by_time(tx: Transaction, data: np.ndarray):
    tx_creation_time = datetime.strptime(tx.eventTimeRes, '%Y-%m-%d %H:%M:%S')
    filtered_data_by_time = data[[datetime.strptime(row['TIME'], '%Y-%m-%d %H:%M:%S') <= tx_creation_time for row in data]]

    filtered_data_by_time['TIME'] = np.array(
        [datetime.strptime(row, '%Y-%m-%d %H:%M:%S') for row in filtered_data_by_time['TIME']]
    )

    unique_ids = np.unique(filtered_data_by_time['ID'])

    filtered_data = []
    for unique_id in unique_ids:

        filtered = filtered_data_by_time[filtered_data_by_time['ID'] == unique_id]

        max_time_index = np.argmax(filtered['TIME'])
        filtered_data.append(filtered[max_time_index])

    filtered_data = np.array(filtered_data, dtype=filtered_data_by_time.dtype)

    return filtered_data


