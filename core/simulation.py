import random


def simulate_transaction(tx, candidate, limits_storage, sum_time, sum_clear_amount, final_chain, rate):
    random_value = random.uniform(0.01, 0.99)
    tx_status = False
    tx_time = candidate[2]['AVG_TIME']
    # Проверяем результат транзакции
    if random_value < candidate[2]['CONVERSION']:
        # Транзакция успешна
        tx_status = True

        final_chain.append(candidate[2]["ID"])

        # Увеличиваем переменные
        sum_time += candidate[2]['AVG_TIME']
        usd_amount = tx.amount * rate
        sum_clear_amount += usd_amount
        limit_entry = limits_storage.get(candidate[2]["ID"])
        limit_entry['current_total'] += tx.amount
        # limit_entry['current_limit_by_card'][tx.card_token] = (
        #         limit_entry['current_limit_by_card'].get(tx.card_token, 0.0) + tx.amount
        # )
        limits_storage.set(candidate[2]["ID"], limit_entry)
        return [sum_time, sum_clear_amount, final_chain, tx_status, tx_time]
    else:
        # Транзакция неудачна
        final_chain.append(candidate[2]["ID"])
        sum_time += candidate[2]['AVG_TIME']
        return [sum_time, sum_clear_amount, final_chain, tx_status, tx_time]
