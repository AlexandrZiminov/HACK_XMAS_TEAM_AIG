import random


def simulate_transaction(tx, candidate, limits_storage, sum_time, sum_clear_amount, final_chain):
    random_value = random.uniform(0.01, 0.99)
    tx_status = False
    # Проверяем результат транзакции
    if random_value < candidate[2]['CONVERSION']:
        # Транзакция успешна
        tx_status = True

        final_chain.append(candidate[2]["ID"])

        # Увеличиваем переменные
        sum_time += candidate[2]['AVG_TIME']
        sum_clear_amount += tx.amount
        limit_entry = limits_storage.get(candidate[2]["ID"])
        limit_entry['current_total'] += tx.amount
        # limit_entry['current_limit_by_card'][tx.card_token] = (
        #         limit_entry['current_limit_by_card'].get(tx.card_token, 0.0) + tx.amount
        # )
        limits_storage.set(candidate[2]["ID"], limit_entry)
        return [sum_time, sum_clear_amount, final_chain, tx_status]
    else:
        # Транзакция неудачна
        final_chain.append(candidate[2]["ID"])
        sum_time += candidate[2]['AVG_TIME']
        return [sum_time, sum_clear_amount, final_chain, tx_status]
