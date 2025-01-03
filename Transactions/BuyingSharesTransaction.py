
from .Transaction import Transaction


class BuyingSharesTransaction(Transaction):
    def __init__(self, seller: str, buyer: str, shares: int, price: float) -> None:
        """
        Tworzy transakcję typu BUYING_SHARES.
        :param seller: Sprzedający
        :param buyer: Kupujący
        :param shares: Liczba akcji
        :param price: Cena
        """
        data = {
            "seller": seller,
            "buyer": buyer,
            "shares": shares,
            "price": price
        }
        super().__init__(transaction_type="BUYING_SHARES", data=data)

    def validate(self) -> bool:
        """
        Walidacja transakcji kupna akcji.
        W przykładzie przyjmujemy podobną logikę jak w SellingSharesTransaction.
        """
        return (
            isinstance(self.data["shares"], int) and self.data["shares"] > 0 and
            isinstance(self.data["price"], float) and self.data["price"] > 0.0 and
            bool(self.data["seller"]) and bool(self.data["buyer"]) and
            self.data["seller"] != self.data["buyer"]
        )
