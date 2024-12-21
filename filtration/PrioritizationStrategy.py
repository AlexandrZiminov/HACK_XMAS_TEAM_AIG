import numpy as np

def dynamic_weights(amount):
    conversion = 3.0 if amount > 10000 else 1.0
    comission = 2.0 if amount > 10000 else 1.0
    avg_time = 2.0 if amount < 5000 else 0.5
    min_limit = 1.0
    max_limit = 1.0
    return conversion, comission, avg_time, min_limit, max_limit

def calculate_limit_incentive(row):
    if row['current_total'] < row['LIMIT_MIN']:
        return 1 - (row['current_total'] / row['LIMIT_MIN'])
    return 0

def calculate_limit_risk(row):
    if row['LIMIT_MAX'] > row['current_total']:
        return 1 - (row['LIMIT_MAX'] - row['current_total']) / row['LIMIT_MAX']
    return 1

def calculate_weight(row):

    conversion, commission, avg_time, min_limit, max_limit = dynamic_weights(row['amount'])

    success_rate = conversion * row['CONVERSION']
    commission_penalty = commission * row['COMMISSION']
    time_penalty = avg_time * row['AVG_TIME']
    limit_incentive = calculate_limit_incentive(row)
    limit_incentive_bonus = min_limit * limit_incentive
    limit_risk = calculate_limit_risk(row)
    limit_risk_penalty = max_limit * limit_risk

    weight = success_rate - commission_penalty - time_penalty + limit_incentive_bonus - limit_risk_penalty
    # Логирование для отладки
    print(f"Provider {row['ID']}:")
    print(f"  Success Rate: {success_rate}")
    print(f"  Commission Penalty: {commission_penalty}")
    print(f"  Time Penalty: {time_penalty}")
    print(f"  Limit Incentive Bonus: {limit_incentive_bonus}")
    print(f"  Limit Risk Penalty: {limit_risk_penalty}")
    print(f"  Final Weight: {weight}\n")
    return weight

#     weight = (
#         conversion * np.log(row['CONVERSION']) -
#         comission * row['COMMISSION']**2 -
#         avg_time * (1 / row['AVG_TIME']) +
#         min_limit * limit_incentive -
#         max_limit * limit_risk
#     )
#     return weight