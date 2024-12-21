import numpy as np
import random  # Для эмуляции вероятности успеха
from domain.transaction import Transaction
from domain.limitStorage import limitStorage
from filtration.filter import filter_source
from filtration.PrioritizationStrategy import calculate_weight

# Загрузка данных транзакций
data_tx = np.genfromtxt(
    'data/payments_1.csv',
    delimiter=',',
    dtype=[
        ('eventTimeRes', 'U19'),
        ('amount', 'f8'),
        ('cur', 'U5'),
        ('payment', 'U50'),
        ('cardToken', 'U50')
    ],
    names=True,
)

# Загрузка данных провайдеров
data_bank = np.genfromtxt(
    'data/providers_1.csv',
    delimiter=',',
    dtype=[
        ('TIME', 'U19'),
        ('ID', 'i4'),
        ('CONVERSION', 'f8'),
        ('AVG_TIME', 'f8'),
        ('MIN_SUM', 'f8'),
        ('MAX_SUM', 'f8'),
        ('LIMIT_MIN', 'f8'),
        ('LIMIT_MAX', 'f8'),
        ('LIMIT_BY_CARD', 'f8'),
        ('COMMISSION', 'f8'),
        ('CURRENCY', 'U10')
    ],
    names=True,
)

# Инициализация LimitStorage
limits_storage = limitStorage()
for row in data_bank:
    limits_storage.set(row['ID'], {
        'current_total': 0.0,
        'limit_by_card': row['LIMIT_BY_CARD'],
        'limit_max': row['LIMIT_MAX'],
        'limit_min': row['LIMIT_MIN'],
    })

print("Инициализация limitStorage завершена:")
for key, value in limits_storage.items():
    print(f"Provider {key}: {value}")

# Имитация попытки провести транзакцию
def attempt_transaction(conversion_prob):
    """
    Проверяет, успешна ли транзакция на основе вероятности конверсии.
    """
    return random.random() < conversion_prob

# Обработка транзакций
for tx_row in data_tx:
    tx = Transaction(
        eventTimeRes=tx_row["eventTimeRes"],
        amount=tx_row["amount"],
        cur=tx_row["cur"],
        payment=tx_row["payment"],
        cardToken=tx_row["cardToken"]
    )

    print("-----------------------")
    print(f"Transaction: {tx}")

    # Фильтрация провайдеров
    filtered_providers = filter_source(tx, data_bank, limits_storage)

    # Рассчитываем веса для провайдеров
    candidates = []
    for row in filtered_providers:
        provider_id = row['ID']
        row_dict = {
            'ID': provider_id,
            'CONVERSION': row['CONVERSION'],
            'AVG_TIME': row['AVG_TIME'],
            'COMMISSION': row['COMMISSION'],
            'LIMIT_MIN': row['LIMIT_MIN'],
            'LIMIT_MAX': row['LIMIT_MAX'],
            'current_total': limits_storage.get(provider_id)['current_total'],
            'amount': tx.amount
        }
        weight = calculate_weight(row_dict)
        candidates.append((provider_id, weight, row))

    # Сортируем провайдеров по убыванию веса
    candidates.sort(key=lambda x: x[1], reverse=True)

    # Вывод приоритизированных провайдеров
    print("Prioritized Providers:")
    for provider_id, weight, row in candidates:
        print(f"Provider {provider_id}: Weight={weight}")

    # Попытка провести транзакцию
    transaction_handled = False
    for provider_id, weight, row in candidates:
        print(f"Trying provider {provider_id} with weight={weight}...")

        # Попытка провести транзакцию
        conversion_prob = row['CONVERSION']
        success = attempt_transaction(conversion_prob)

        if success:
            # Получаем текущие данные провайдера
            provider_data = limits_storage.get(provider_id)
            provider_data['current_total'] += tx.amount  # Обновляем current_total

            # Сохраняем обратно обновлённые данные
            limits_storage.set(provider_id, provider_data)

            print(f"Transaction SUCCESS with provider {provider_id}. Updated current_total: {provider_data['current_total']}")
            transaction_handled = True
            break

    if not transaction_handled:
        print(f"Transaction could NOT be processed for {tx}. No available providers.")

    print("-----------------------")
