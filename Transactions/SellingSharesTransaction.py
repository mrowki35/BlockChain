
from Transaction import Transaction
class SellingSharesTransaction(Transaction):
    def __init__(self, seller: str, buyer: str, shares: int, price: float) -> None:
        data = {
            "seller": seller,
            "buyer": buyer,
            "shares": shares,
            "price": price
        }
        super().__init__(transaction_type="SELLING_SHARES", data=data)

    def validate(self) -> bool:
        return (
            isinstance(self.data["shares"], int) and self.data["shares"] > 0 and
            isinstance(self.data["price"], float) and self.data["price"] > 0.0 and
            bool(self.data["seller"]) and bool(self.data["buyer"]) and
            self.data["seller"] != self.data["buyer"]
        )