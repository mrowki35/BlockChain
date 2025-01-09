from .Transaction import Transaction


class IssuingStocksTransaction(Transaction):
    def __init__(self, company: str, shares: int, price: float) -> None:
        """
        Tworzy transakcję typu ISSUING_SHARES.
        :param company: Firma emitująca akcje
        :param shares: Liczba nowych akcji
        :param price: Cena emisyjna jednej akcji
        """
        data = {
            "company": company,
            "shares": shares,
            "price": price
        }
        super().__init__(transaction_type="ISSUING_SHARES", data=data)

    def validate(self) -> bool:
        """
        Walidacja transakcji emisji akcji.
        """
        return (
                isinstance(self.data["shares"], int) and self.data["shares"] > 0 and
                isinstance(self.data["price"], float) and self.data["price"] > 0.0 and
                bool(self.data["company"])
        )
