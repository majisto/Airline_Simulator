from city import Negotiation
from player import Player


class Game_Date:
    month_list = ["Jan", "Apr", "Jul", "Oct"]

    def __init__(self, year):
        self.current_year = year
        self.current_month_index = 0

    def advance_date(self):
        self.current_month_index += 1
        if self.current_month_index == 4: #New Year, start over at January with next year.
            self.current_month_index = 0
            self.current_year += 1

    def get_date(self):
        return "{0}. {1}".format(self.month_list[self.current_month_index], self.current_year)

def resolve_negotiations(player):
    assert isinstance(player, Player)
    for neg in player.negotiation_list:
        assert isinstance(neg, Negotiation)
        neg.resolve_negotiation()