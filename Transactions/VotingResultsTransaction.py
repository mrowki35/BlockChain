from .Transaction import Transaction

class VotingResultsTransaction(Transaction):
    """
    Transakcja dotycząca wyników głosowania nad uchwałami na Zgromadzeniu Wspólników.
    """
    def __init__(self, resolution_id: str, total_votes: int, votes_for: int, votes_against: int, votes_abstain: int) -> None:
        """
        :param resolution_id: ID lub opis uchwały
        :param total_votes: Łączna liczba głosów
        :param votes_for: Liczba głosów za
        :param votes_against: Liczba głosów przeciw
        :param votes_abstain: Liczba głosów wstrzymujących się
        """
        data = {
            "resolution_id": resolution_id,
            "total_votes": total_votes,
            "votes_for": votes_for,
            "votes_against": votes_against,
            "votes_abstain": votes_abstain
        }
        super().__init__(transaction_type="VOTING_RESULTS", data=data)

    def validate(self) -> bool:
        """
        Walidacja wyników głosowania:
        1. `resolution_id` nie może być pusty.
        2. Liczby głosów (`total_votes`, `votes_for`, itd.) muszą być nieujemne.
        3. `votes_for + votes_against + votes_abstain` == `total_votes`.
        """
        return (
            bool(self.data["resolution_id"]) and
            isinstance(self.data["total_votes"], int) and self.data["total_votes"] >= 0 and
            isinstance(self.data["votes_for"], int) and self.data["votes_for"] >= 0 and
            isinstance(self.data["votes_against"], int) and self.data["votes_against"] >= 0 and
            isinstance(self.data["votes_abstain"], int) and self.data["votes_abstain"] >= 0 and
            (self.data["votes_for"] + self.data["votes_against"] + self.data["votes_abstain"] == self.data["total_votes"])
        )
