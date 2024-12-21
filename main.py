import numpy as np
<<<<<<< Updated upstream
=======
from domain.transaction import Transaction
from domain.limitStorage import limitStorage
from filtration.filter import filter_source
from filtration.PrioritizationStrategy import calculate_weight
>>>>>>> Stashed changes

from domain.transaction import Transaction
from filtration.filter import _by_currency, _by_time

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

<<<<<<< Updated upstream
index_of_tx = 0
for tx in data_tx:
=======
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

# Обработка транзакций
for tx_row in data_tx:
>>>>>>> Stashed changes
    tx = Transaction(
        eventTimeRes=data_tx[index_of_tx]["eventTimeRes"],
        amount=data_tx[index_of_tx]["amount"],
        cur=data_tx[index_of_tx]["cur"],
        payment=data_tx[index_of_tx]["payment"],
        cardToken=data_tx[index_of_tx]["cardToken"]
    )

    print("-----------------------")

    print(tx)

    for j in _by_time(tx, _by_currency(tx, data_bank)):
        print(j)

<<<<<<< Updated upstream
=======
    # Сортируем провайдеров по убыванию веса
    candidates.sort(key=lambda x: x[1], reverse=True)

    # Вывод приоритизированных провайдеров
    print("Prioritized Providers:")
    for provider_id, weight, row in candidates:
        print(f"Provider {provider_id}: Weight={weight}")

    # Проведение транзакции с провайдером с наивысшим приоритетом
    transaction_handled = False
    for provider_id, weight, row in candidates:
        print(f"Attempting transaction with provider {provider_id} (weight={weight})...")

        # Успешная обработка транзакции
        provider_data = limits_storage.get(provider_id)
        provider_data['current_total'] += tx.amount  # Обновляем лимиты

        limits_storage.set(provider_id, provider_data)  # Сохраняем изменения
        print(f"Transaction SUCCESS with provider {provider_id}. Updated current_total: {provider_data['current_total']}")

        transaction_handled = True
        break

    # Если ни один провайдер не обработал транзакцию
    if not transaction_handled:
        print(f"Transaction could NOT be processed for {tx}. No available providers.")
>>>>>>> Stashed changes

    print("-----------------------")
    index_of_tx += 1





