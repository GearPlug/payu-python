class BaseError(Exception):
    pass


class FranchiseUnavailableError(BaseError):
    pass


class CVVRequiredError(BaseError):
    pass


class InvalidCountryError(BaseError):
    pass
