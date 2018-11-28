from payu.enumerators import Country, Franchise as F, TransactionType as T
from payu.exceptions import InvalidCountryError


def get_available_franchise_for_payment(country, transaction_type):
    """

    Args:
        country:
        transaction_type:

    Returns:
        List of available Franchises for a country and transaction type.

    """
    if country == Country.ARGENTINA:
        if transaction_type in (T.AUTHORIZATION, T.CAPTURE):
            return F.VISA, F.MASTERCARD, F.AMEX, F.SHOPPING, F.CABAL, F.ARGENCARD, F.CENCOSUD, F.NARANJA
        else:
            return F.VISA, F.MASTERCARD, F.AMEX, F.SHOPPING, F.CABAL, F.ARGENCARD, F.CENCOSUD, F.NARANJA
    elif country == Country.BRAZIL:
        if transaction_type in (T.AUTHORIZATION, T.CAPTURE):
            return F.VISA, F.MASTERCARD, F.AMEX, F.DINERS, F.HIPERCARD, F.ELO
        else:
            return F.VISA, F.MASTERCARD, F.AMEX, F.DINERS, F.HIPERCARD, F.ELO
    elif country == Country.COLOMBIA:
        if transaction_type in (T.AUTHORIZATION, T.CAPTURE):
            return None
        else:
            return F.VISA, F.MASTERCARD, F.AMEX, F.DINERS, F.CODENSA, F.VISA_DEBIT
    elif country == Country.MEXICO:
        # Nota de Ingeniero de Payu:
        # Puede procesar en 2 pasos VISA y MASTERCARD
        # Puede procesar en 1 VISA, MASTERCARD y AMEX
        if transaction_type in (T.AUTHORIZATION, T.CAPTURE):
            return F.VISA, F.MASTERCARD
        else:
            return F.VISA, F.MASTERCARD, F.AMEX
    elif country == Country.PANAMA:
        if transaction_type in (T.AUTHORIZATION, T.CAPTURE):
            return None
        else:
            return F.VISA, F.MASTERCARD
    elif country == Country.PERU:
        # Nota de Ingeniero de Payu:
        # Puede procesar en 2 pasos MASTERCARD, DINERS, AMEX y VISA DEBIT
        # Puede procesar en 1 paso MASTERCARD VISA DEBIT y DEBIT
        if transaction_type in (T.AUTHORIZATION, T.CAPTURE):
            return F.VISA, F.MASTERCARD, F.DINERS, F.AMEX, F.VISA_DEBIT
        else:
            return F.VISA, F.MASTERCARD, F.DINERS, F.AMEX, F.VISA_DEBIT, F.MASTERCARD_DEBIT
    elif country == Country.CHILE:
        if transaction_type in (T.AUTHORIZATION, T.CAPTURE):
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
        List of available Franchises for a country and transaction type.

    """
    if country == Country.ARGENTINA:
        # Nota de Ingeniero de Payu:
        # Puede procesar en 2 pasos TODAS sin CVV excepto VISA
        # Puede procesar en 1 paso TODAS sin CVV excepto VISA
        if transaction_type in (T.AUTHORIZATION, T.CAPTURE):
            return F.VISA, F.MASTERCARD, F.AMEX, F.SHOPPING, F.CABAL, F.ARGENCARD, F.CENCOSUD, F.NARANJA
        else:
            return F.VISA, F.MASTERCARD, F.AMEX, F.SHOPPING, F.CABAL, F.ARGENCARD, F.CENCOSUD, F.NARANJA
    elif country == Country.BRAZIL:
        # Nota de Ingeniero de Payu:
        # Puede procesar en 2 pasos TODAS sin CVV
        # Puede procesar en 1 paso TODAS sin CVV
        if transaction_type in (T.AUTHORIZATION, T.CAPTURE):
            return F.VISA, F.MASTERCARD, F.AMEX, F.DINERS, F.HIPERCARD, F.ELO
        else:
            return F.VISA, F.MASTERCARD, F.AMEX, F.DINERS, F.HIPERCARD, F.ELO
    elif country == Country.COLOMBIA:
        if transaction_type in (T.AUTHORIZATION, T.CAPTURE):
            return None
        else:
            return F.VISA, F.MASTERCARD, F.AMEX, F.DINERS
    elif country == Country.MEXICO:
        # Nota de Ingeniero de Payu:
        # Puede procesar en 2 pasos TODAS sin CVV excepto AMEX
        # Puede procesar en 1 paso TODAS sin CVV excepto AMEX
        if transaction_type in (T.AUTHORIZATION, T.CAPTURE):
            return F.VISA, F.MASTERCARD
        else:
            return F.VISA, F.MASTERCARD, F.AMEX
    elif country == Country.PANAMA:
        if transaction_type in (T.AUTHORIZATION, T.CAPTURE):
            return None
        else:
            return F.VISA, F.MASTERCARD
    elif country == Country.PERU:
        # Nota de Ingeniero de Payu:
        # Puede procesar en 2 pasos TODAS sin CVV
        # Puede procesar en 1 paso TODAS sin CVV
        if transaction_type in (T.AUTHORIZATION, T.CAPTURE):
            return F.VISA, F.MASTERCARD, F.DINERS, F.AMEX
        else:
            return F.VISA, F.MASTERCARD, F.DINERS, F.AMEX
    elif country == Country.CHILE:
        if transaction_type in (T.AUTHORIZATION, T.CAPTURE):
            return None
        else:
            return F.VISA, F.MASTERCARD, F.AMEX, F.DINERS
    else:
        raise InvalidCountryError


def has_franchise_cvv_tokenization(franchise, country, transaction_type):
    """

    Args:
        franchise:
        country:
        transaction_type:

    Returns:
        True if CVV is required for a country and transaction type; otherwise, False.
    """
    if country == Country.ARGENTINA:
        franchise_list = (F.VISA,)
        if transaction_type in (T.AUTHORIZATION, T.CAPTURE) and franchise in franchise_list:
            return True
        if transaction_type == T.AUTHORIZATION_AND_CAPTURE and franchise in franchise_list:
            return True
    elif country == Country.BRAZIL:
        # Nota de Ingeniero de Payu:
        # Puede procesar todas sin CVV
        return False
    elif country == Country.COLOMBIA:
        # Nota de Ingeniero de Payu:
        # Puede procesar todas sin CVV
        return False
    elif country == Country.CHILE:
        # Nota de Ingeniero de Payu:
        # No puede procesar ninguna sin CVV
        return True
    elif country == Country.MEXICO:
        if transaction_type == T.AUTHORIZATION_AND_CAPTURE and franchise in (F.AMEX,):
            return True
    elif country == Country.PANAMA:
        # Nota de Ingeniero de Payu:
        # No puede procesar ninguna sin CVV
        return True
    elif country == Country.PERU:
        # Nota de Ingeniero de Payu:
        # Puede procesar todas sin CVV
        return False
    else:
        raise InvalidCountryError
