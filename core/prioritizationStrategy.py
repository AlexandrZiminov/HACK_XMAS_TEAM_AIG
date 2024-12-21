def calculate_weight(row):
    conversion, commission, avg_time, min_limit, max_limit = _dynamic_weights(row['amount'])

    success_rate = conversion * row['CONVERSION']
    commission_penalty = commission * row['COMMISSION']
    time_penalty = avg_time * row['AVG_TIME']
    limit_incentive = _calculate_limit_incentive(row)
    limit_incentive_bonus = min_limit * limit_incentive
    limit_risk = _calculate_limit_risk(row)
    limit_risk_penalty = max_limit * limit_risk

    weight = success_rate - commission_penalty - time_penalty + limit_incentive_bonus - limit_risk_penalty
    return weight


def _dynamic_weights(amount):
    conversion = 3.0 if amount > 10000 else 1.0
    commission = 2.0 if amount > 10000 else 1.0
    avg_time = 2.0 if amount < 5000 else 0.5
    min_limit = 1.0
    max_limit = 1.0
    return conversion, commission, avg_time, min_limit, max_limit


def _calculate_limit_incentive(row):
    if row['current_total'] < row['LIMIT_MIN']:
        return 1 - (row['current_total'] / row['LIMIT_MIN'])
    return 0


def _calculate_limit_risk(row):
    if row['LIMIT_MAX'] > row['current_total']:
        return 1 - (row['LIMIT_MAX'] - row['current_total']) / row['LIMIT_MAX']
    return 1
