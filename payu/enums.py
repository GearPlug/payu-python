from enum import Enum


class TransactionType(Enum):
    AUTHORIZATION = 'AUTHORIZATION'
    CAPTURE = 'CAPTURE'
    AUTHORIZATION_AND_CAPTURE = 'AUTHORIZATION_AND_CAPTURE'
    VOID = 'VOID'
    REFUND = 'REFUND'


class Country(Enum):
    ARGENTINA = 'AR'
    BRASIL = 'BR'
    COLOMBIA = 'CO'
    MEXICO = 'MX'
    PANAMA = 'PA'
    PERU = 'PE'
    CHILE = 'CL'

    BRAZIL = BRASIL
