from .Transaction import Transaction

class GrantingStocksTransaction(Transaction):
    def __init__(self, company: str, grantee: str, shares: int) -> None:
        """
        Tworzy transakcję typu GRANTING_SHARES.
        :param company: Firma przyznająca akcje
        :param grantee: Odbiorca akcji
        :param shares: Liczba przyznanych akcji
        """
        data = {
            "company": company,
            "grantee": grantee,
            "shares": shares
        }
        super().__init__(transaction_type="GRANTING_SHARES", data=data)

    def validate(self) -> bool:
        """
        Walidacja transakcji przyznania akcji.
        """
        return (
            isinstance(self.data["shares"], int) and self.data["shares"] > 0 and
            bool(self.data["company"]) and
            bool(self.data["grantee"]) and
            self.data["company"] != self.data["grantee"]
        )
