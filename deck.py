import Typing
import time
import queue
import secrets

deck_of_cards = queue(["Aa", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a", "Ta", "Ja", "Qa", "Ka", "Ab", "2b", "3b", "4b", "5b", "6b", "7b", "8b", "9b", "Tb", "Jb", "Qb", "Kb","Ac", "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "Tc", "Jc", "Qc", "Kc","Ad", "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "Td", "Jd", "Qd", "Kd"])

class Deck:

    def __init__(self, deck = deck_of_cards) -> None:

        self.deck = deck
        self.shuffle()
        self.original_deck = self.deck
        self.discard_pile = []

    def shuffle(self):

        for i in range(len(self.deck) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            self.deck[i], self.deck[j] = self.deck[j], self.deck[i]

    def flop(self) -> List:

        self.burn()
        to_display = []
        for num_card in range(3):
            to_display.append(self.deck.pop_left())
        return to_display

    def turn(self) -> str:

        self.burn()
        return self.deck.pop_left()

    def river(self) -> str:

        self.burn()
        return self.deck.pop_left()

    def deal_card(self) -> None:

        return self.deck.pop_left()

    def burn(self):

        next_card = self.deck.pop_left()
        self.discard_pile.append(next_card)

