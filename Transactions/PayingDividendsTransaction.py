from .Transaction import Transaction

class PayingDividendsTransaction(Transaction):
    def __init__(self, company: str, shareholder: str, shares: int, dividend_per_share: float) -> None:
        """
        Tworzy transakcję typu PAYING_DIVIDENDS.
        :param company: Firma wypłacająca dywidendy
        :param shareholder: Akcjonariusz otrzymujący dywidendy
        :param shares: Liczba akcji posiadanych przez akcjonariusza
        :param dividend_per_share: Kwota dywidendy przypadająca na jedną akcję
        """
        total_dividend = shares * dividend_per_share
        data = {
            "company": company,
            "shareholder": shareholder,
            "shares": shares,
            "dividend_per_share": dividend_per_share,
            "total_dividend": total_dividend
        }
        super().__init__(transaction_type="PAYING_DIVIDENDS", data=data)

    def validate(self) -> bool:
        """
        Walidacja transakcji wypłaty dywidend.
        """
        return (
            bool(self.data["company"]) and
            bool(self.data["shareholder"]) and
            self.data["company"] != self.data["shareholder"] and
            isinstance(self.data["shares"], int) and self.data["shares"] > 0 and
            isinstance(self.data["dividend_per_share"], float) and self.data["dividend_per_share"] > 0.0
        )
