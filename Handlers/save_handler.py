import json
from pathlib import Path
from .base_handler import TransactionHandler


class SaveHandler:
    """
    Handler, który dokonuje głębokiej kopii (clone) bloku i zapisuje go do pliku w formacie JSON.
    """

    def __init__(self, output_filename="saved_blocks.json"):
        self.output_file = Path(output_filename)

    def save(self, transaction):
        """
        Otrzymuje obiekt klasy Block (z Blockchain/Block.py).
        1. Tworzy głęboką kopię bloku metodą block.clone().
        2. Zapisuje kopię do pliku w formacie JSON (jeden blok w jednej linii).
        3. Deleguje dalej do kolejnego handlera w łańcuchu (jeśli istnieje).
        """
        with self.output_file.open('a', encoding='utf-8') as f:
            f.write(json.dumps(transaction.to_dict(), ensure_ascii=False))
            f.write("\n")
