


class Player:

    def __init__(self, bank: float, turn_limit: int, model: Serialize):

        self.hand = []
        self.best_hand_rank = None
        self.current_bet = 0
        self.id = 0
        self.bank = bank
        self.turn_limit = turn_limit
        self.turns_player = 0
        self.model = model


    def action(self, logs) -> list:

        # this is where the model does what it wants to do
        decision = self.model.choose(logs, self.bank, self.turns_player, self.turn_limit)
        return decision

