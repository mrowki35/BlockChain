from .Transaction import Transaction


class IncreasingCapitalTransaction(Transaction):
    """
    Transakcja zwiększania kapitału (np. w spółce z o.o.).
    """

    def __init__(self, company: str, additional_capital: float, new_shares: int) -> None:
        data = {
            "company": company,
            "additional_capital": additional_capital,
            "new_shares": new_shares
        }
        super().__init__(transaction_type="INCREASING_CAPITAL", data=data)

    def validate(self) -> bool:
        """
        Przykładowa walidacja – w realnym systemie byłoby tu więcej logiki.
        """
        return (
                bool(self.data["company"]) and
                isinstance(self.data["additional_capital"], float) and self.data["additional_capital"] > 0.0 and
                isinstance(self.data["new_shares"], int) and self.data["new_shares"] > 0
        )
