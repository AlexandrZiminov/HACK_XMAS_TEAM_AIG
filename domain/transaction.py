from collections import namedtuple

Transaction = namedtuple('Transaction', ['eventTimeRes', 'amount', 'cur', 'payment', 'cardToken'])
