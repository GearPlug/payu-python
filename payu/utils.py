from .enumerators import Country, Franchise as F, TransactionType
from .exceptions import InvalidCountryError


def get_available_franchise_for_payment(country, transaction_type):
    """

    Args:
        country:
        transaction_type:

    Returns:

    """
    if country == Country.ARGENTINA:
        if transaction_type in (TransactionType.AUTHORIZATION, TransactionType.CAPTURE):
            return F.VISA, F.MASTERCARD, F.AMEX, F.SHOPPING, F.CABAL, F.ARGENCARD, F.CENCOSUD
        else:
            return F.VISA, F.MASTERCARD, F.AMEX, F.SHOPPING, F.CABAL, F.ARGENCARD, F.CENCOSUD, F.NARANJA
    elif country == Country.BRAZIL:
        if transaction_type in (TransactionType.AUTHORIZATION, TransactionType.CAPTURE):
            return F.VISA, F.MASTERCARD, F.AMEX, F.DINERS, F.HIPERCARD, F.ELO
        else:
            return F.VISA, F.MASTERCARD, F.AMEX, F.DINERS, F.HIPERCARD, F.ELO
    elif country == Country.COLOMBIA:
        if transaction_type in (TransactionType.AUTHORIZATION, TransactionType.CAPTURE):
            return None
        else:
            return F.VISA, F.MASTERCARD, F.AMEX, F.DINERS, F.CODENSA, F.VISA_DEBIT
    elif country == Country.MEXICO:
        if transaction_type in (TransactionType.AUTHORIZATION, TransactionType.CAPTURE):
            return None
        else:
            return F.VISA, F.MASTERCARD, F.AMEX
    elif country == Country.PANAMA:
        if transaction_type in (TransactionType.AUTHORIZATION, TransactionType.CAPTURE):
            return None
        else:
            return F.VISA, F.MASTERCARD
    elif country == Country.PERU:
        if transaction_type in (TransactionType.AUTHORIZATION, TransactionType.CAPTURE):
            return F.VISA
        else:
            return F.VISA, F.MASTERCARD, F.DINERS, F.AMEX
    elif country == Country.CHILE:
        if transaction_type in (TransactionType.AUTHORIZATION, TransactionType.CAPTURE):
            return None
        else:
            return F.VISA, F.MASTERCARD, F.AMEX, F.DINERS
    else:
        raise InvalidCountryError


def get_available_franchise_for_tokenization(country, transaction_type):
    """

    Args:
        country:
        transaction_type:

    Returns:

    """
    if country == Country.ARGENTINA:
        if transaction_type in (TransactionType.AUTHORIZATION, TransactionType.CAPTURE):
            return None
        else:
            return F.VISA, F.MASTERCARD, F.AMEX, F.NARANJA, F.SHOPPING, F.CABAL, F.ARGENCARD, F.CENCOSUD
    elif country == Country.BRAZIL:
        if transaction_type in (TransactionType.AUTHORIZATION, TransactionType.CAPTURE):
            return F.VISA, F.MASTERCARD, F.AMEX, F.DINERS, F.ELO
        else:
            return None
    elif country == Country.COLOMBIA:
        if transaction_type in (TransactionType.AUTHORIZATION, TransactionType.CAPTURE):
            return None
        else:
            return F.VISA, F.MASTERCARD, F.AMEX, F.DINERS
    elif country == Country.MEXICO:
        if transaction_type in (TransactionType.AUTHORIZATION, TransactionType.CAPTURE):
            return None
        else:
            return F.VISA, F.MASTERCARD, F.AMEX
    elif country == Country.PANAMA:
        if transaction_type in (TransactionType.AUTHORIZATION, TransactionType.CAPTURE):
            return None
        else:
            return F.VISA, F.MASTERCARD
    elif country == Country.PERU:
        if transaction_type in (TransactionType.AUTHORIZATION, TransactionType.CAPTURE):
            return None
        else:
            return F.VISA, F.MASTERCARD
    else:
        raise InvalidCountryError


def has_franchise_cvv_tokenization(franchise, country, transaction_type):
    """

    Args:
        franchise:
        country:
        transaction_type:

    Returns:

    """
    if country == Country.ARGENTINA:
        franchise_list = (F.VISA, F.MASTERCARD, F.AMEX, F.NARANJA, F.SHOPPING, F.CABAL, F.ARGENCARD, F.CENCOSUD)
        if transaction_type == TransactionType.AUTHORIZATION_AND_CAPTURE and franchise in franchise_list:
            return True
    if country == Country.MEXICO:
        if transaction_type == TransactionType.AUTHORIZATION_AND_CAPTURE and franchise in (F.AMEX,):
            return True
    if country == Country.PANAMA:
        if transaction_type == TransactionType.AUTHORIZATION_AND_CAPTURE and franchise in (F.VISA, F.MASTERCARD):
            return True
    if country == Country.PERU:
        if transaction_type == TransactionType.AUTHORIZATION_AND_CAPTURE and franchise in (F.MASTERCARD,):
            return True
    return False
