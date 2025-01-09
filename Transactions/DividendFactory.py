from .AbstractTransactionFactory import AbstractTransactionFactory
from .PayingDividendsTransaction import PayingDividendsTransaction


class DividendFactory(AbstractTransactionFactory):
    def create_transaction(self, **kwargs) -> PayingDividendsTransaction:
        """
        Tworzy obiekt transakcji wypłaty dywidend.
        """
        return PayingDividendsTransaction(
            company=kwargs.get("company"),
            shareholder=kwargs.get("shareholder"),
            shares=kwargs.get("shares"),
            dividend_per_share=kwargs.get("dividend_per_share")
        )
