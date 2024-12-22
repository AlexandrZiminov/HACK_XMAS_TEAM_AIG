import numpy as np
from domain.limitStorage import LimitStorage
from domain.transaction import Transaction
from core.filter import filter_source
from core.prioritizationStrategy import calculate_weight
from core.simulation import simulate_transaction
import csv


headers = ['eventTimeRes', 'amount', 'cur', 'payment', 'cardToken', 'flow']
csv_file_name = 'result/result_payments.csv'


with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

data_rates = np.genfromtxt(
    'data/ex_rates.csv',
    delimiter=',',
    dtype=[
        ('rate', 'f8'),
        ('destination', 'U10'),
    ],
    names=True,
)

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

limits_storage = LimitStorage()
sum_time = 0.0
sum_clear_amount = 0.0

unique_ids = np.unique(data_bank['ID'])

for unique_id in unique_ids:
    row = data_bank[data_bank['ID'] == unique_id][0]

    limits_storage.set(row['ID'], {
        'current_total': 0.0,
        'limit_by_card': row['LIMIT_BY_CARD'],
        'current_limit_by_card': {},
        'limit_max': row['LIMIT_MAX'],
        'limit_min': row['LIMIT_MIN'],
    })

# for key, value in limits_storage.items():
#     print(f"Provider {key}: {value}")

for tx_row in data_tx:
    tx = Transaction(
        eventTimeRes=tx_row["eventTimeRes"],
        amount=tx_row["amount"],
        cur=tx_row["cur"],
        payment=tx_row["payment"],
        cardToken=tx_row["cardToken"]
    )
    

    filtered_providers = filter_source(tx, data_bank, limits_storage)

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

    candidates.sort(reverse=True, key=lambda x: x[1])

    final_chain = []

    rates = data_rates['rate'][data_rates['destination'] == tx.cur]
    rate = float(rates[0])

    if candidates:
        tx_time = 0.0
        for candidate in candidates:
            if tx_time < 60.0:
                simulated_tx = simulate_transaction(tx, candidate, limits_storage, sum_time, sum_clear_amount, final_chain,
                                                    rate)
                if simulated_tx[3]:
                    sum_time = simulated_tx[0]
                    sum_clear_amount = simulated_tx[1]
                    cur = simulated_tx[1]
                    final_chain = simulated_tx[2]
                    with open(csv_file_name, mode='a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)

                        final_chain = '-'.join([str(i) for i in simulated_tx[2]])
                        tx_row_list = list(tx_row)
                        tx_row_list.append(final_chain)

                        writer.writerow(tx_row_list)
                    break
                else:
                    sum_time = simulated_tx[0]
                    final_chain = simulated_tx[2]
                    index = candidates.index(candidate)
                    tx_time += simulated_tx[4]
                    if index == (len(candidates) - 1):
                        with open(csv_file_name, mode='a', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)

                            final_chain = '-'.join([str(i) for i in simulated_tx[2]])
                            tx_row_list = list(tx_row)
                            tx_row_list.append(final_chain)

                            writer.writerow(tx_row_list)
            else:
                with open(csv_file_name, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)

                    final_chain = '-'.join([str(i) for i in final_chain])
                    tx_row_list = list(tx_row)
                    tx_row_list.append(final_chain)

                    writer.writerow(tx_row_list)
                print("Time for chain more than 60 sec")
    else:
        with open(csv_file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            final_chain = '-'
            tx_row_list = list(tx_row)
            tx_row_list.append(final_chain)

            writer.writerow(tx_row_list)

print(str(sum_time) + "seconds")
print("$" + str(sum_clear_amount))
