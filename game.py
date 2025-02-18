import deck as d
import logger as l
import player as p
import "round" as r


RANKS = {
'2': 2, '3': 3, '4': 4, '5': 5,
'6': 6, '7': 7, '8': 8, '9': 9,
'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

class Game:

    def __init__(self, small_blind: float, big_blind: float, ante: float, time_to_decide=10, no_limit=True, max_players=9, timeout_leniancy=1) -> None:

        self.deck = d.Deck()
        self.logs = l.Logger()
        # log original deck
        self.table = [] # list of players
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.ante = ante
        self.time_to_decide = time_to_decide
        self.no_limit = no_limit
        self.max_players = max_players
        self.timeout_leniancy = timeout_leniancy
        self.dealer_button_idx = 0 # we call _newRound, which includes a += 1
        self.playing = True
        self.waiting_list = deque()

    def _stopGame(self):

        # log info, return logger
        self.playing = False

    def _handlePot(self, pot_outcome: tuple):

        pot, winner = pot_outcome
        won = sum(pot)
        for idx, amount in pot:
            self.table[idx].bank -= amount
            if self.table[idx].bank.id = winner:
                self.table[idx].bank + won

    def _waitlist(self, player: Player):

        self.waitlist.append(player)

    def _updateTable(self):

        for player in self.table:
            if player.model.leave():
                self.table.remove(player)
            elif player.turn_limit <= player.turns_played:
                self.table.remove(player)

        while len(self.table) <= self.max_players and len(self.waitlist) > 0:
            self.table.append(self.waitlist.pop_left())
        if len(self.table) < 2:
            self._stopGame()

    def play(self):

        while self.is_playing:
            active_players = self.table.copy()
            cround = Round(self.dealer_button_idx, self.table.copy(), self.small_blind, self.big_blind, self.ante, self.time_to_decide, self.no_limit, self.deck)
            pot_outcome, logs = cround.play()
            self._handlePot(pot_outcome)
            self._updateTable()




