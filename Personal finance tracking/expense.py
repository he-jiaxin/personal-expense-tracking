class Expense:
    def __init__(self, name: str, category: str, amount: float) -> None:
        self._name = name
        self._category = category
        self._amount = amount

    @property
    def name(self) -> str:
        return self._name.title()

    @property
    def category(self) -> str:
        return self._category

    @property
    def amount(self) -> float:
        return self._amount

    def __repr__(self) -> str:
        return f"<Expense:{self.name}, {self.category}, £{self.amount:.2f}>"
