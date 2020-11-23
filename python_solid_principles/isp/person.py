from typing import List


class Money:
    def __init__(self, amount: float) -> None:
        self.__amount = amount

    @property
    def amount(self):
        return self.__amount


class Pants:
    pass


class Underwear:
    pass


class Shirt(object):
    pass


class OutOfFundsError(Exception):
    pass


class MoneyHandler:
    def __init__(self, money: List[Money]) -> None:
        self.__money = money

    def get_money(self, amount: float) -> List[Money]:
        money_to_give = []

        money = sorted(self.__money, key=lambda m: m.amount, reverse=True)

        for m in money:
            if amount <= 0:
                break

            if m.amount <= amount:
                money_to_give.append(m)
                self.__money.remove(m)

                amount -= m.amount

        if amount > 0:
            raise OutOfFundsError()

        return money_to_give

    def add_money(self, money: List[Money]) -> None:
        self.__money += money


class PantsWearer:
    def __init__(self, pants: Pants) -> None:
        self.pants = pants


class UnderwearWearer:
    def __init__(self, underwear: Underwear) -> None:
        self.underwear = underwear


class ShirtWearer:
    def __init__(self, shirt: Shirt) -> None:
        self.shirt = shirt


class Person(MoneyHandler, PantsWearer, UnderwearWearer, ShirtWearer):
    def __init__(
        self, money: List[Money], pants: Pants, underwear: Underwear, shirt: Shirt
    ) -> None:
        MoneyHandler.__init__(self, money)
        PantsWearer.__init__(self, pants)
        UnderwearWearer.__init__(self, underwear)
        ShirtWearer.__init__(self, shirt)


def pay(person: MoneyHandler, amount: float) -> List[Money]:
    return person.get_money(amount)


def test_pay():
    money_1 = Money(10)
    money_2 = Money(5)
    money = [money_1, money_2]
    money_handler = MoneyHandler(money)

    received_money = pay(money_handler, 15)

    assert received_money == [money_1, money_2]
