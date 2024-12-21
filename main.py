import numpy as np

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

index_of_tx = 0
for tx in data_tx:
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


    print("-----------------------")
    index_of_tx += 1





