


class Round:

    def __init__(self, dealer_button_idx: int, active_players: list, small_blind: float, big_blind: float, ante: float, time_to_decide: float, no_limit: bool, deck: Deck) -> None:

        self.dealer_button_idx = dealer_button_idx
        self.action_idx = (self.dealer_button_idx + 3) % len(active_players)
        self.active_players = active_players[:]
        self.all_players = active_players[:]
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.ante = ante
        self.time_to_decide = time_to_decide
        self.no_limit = no_limit
        self.player_pots = [self.ante] * len(active_players)
        self.pot_total = 0 # need to add logic for side pot. might just make pot class
        self.deck = deck
        self.community_cards = []

    def _start(self):

        player_pots[(self.dealer_button_idx + 1) % len(self.active_players)] += self.small_blind

        player_pots[(self.dealer_button_idx + 2) % len(self.active_players)] += self.big_blind

        for deal_num in range(len(self.active_players) * 2):

            self.active_players[(self.action_idx + deal_num) % len(self.active_players)].hand.append(deck.deal_card)

        # log all this

    def _end(self):

        self.deck = Deck(deck = self.deck.deck + self.discard_pile)

 
    def _calcWinner(self):


        def evaluate_hand(cards):
            """
            Evaluate a 5-card poker hand and return a tuple representing its rank.
            Higher tuples compare as better hands.

            Hand categories (first tuple element):
              9: Straight flush
              8: Four of a kind
              7: Full house
              6: Flush
              5: Straight
              4: Three of a kind
              3: Two pair
              2: One pair
              1: High card
            The remaining tuple elements are tiebreakers.
            """
            # Extract card values and suits
            values = [RANKS[card[0]] for card in cards]
            suits = [card[1] for card in cards]
            values.sort(reverse=True)  # sort descending

            # Count frequency of each card value
            value_counts = Counter(values)
            counts = value_counts.most_common()  # sorted by count then value

            # Check for flush: all cards same suit
            is_flush = len(set(suits)) == 1

            # Check for straight: look for 5 consecutive unique values
            unique_values = sorted(set(values), reverse=True)
            straight_high = None
            if len(unique_values) >= 5:
                for i in range(len(unique_values) - 4):
                    # If the highest minus the lowest in this 5-card run is 4, they are consecutive
                    if unique_values[i] - unique_values[i+4] == 4:
                        straight_high = unique_values[i]
                        break
                # Ace-low straight: Ace, 5, 4, 3, 2 (Ace counts as 1)
                if not straight_high and set([14, 5, 4, 3, 2]).issubset(set(values)):
                    straight_high = 5

            # Straight flush (if flush and straight)
            if is_flush and straight_high:
                return (9, straight_high)

            # Four-of-a-kind: one value appears four times
            if counts[0][1] == 4:
                quad = counts[0][0]
                kicker = max([v for v in values if v != quad])
                return (8, quad, kicker)

            # Full house: one three-of-a-kind and one pair
            if counts[0][1] == 3 and len(counts) > 1 and counts[1][1] >= 2:
                triple = counts[0][0]
                pair = counts[1][0]
                return (7, triple, pair)

            # Flush: all cards same suit
            if is_flush:
                return (6, values)  # tiebreaker: sorted card values

            # Straight (but not flush)
            if straight_high:
                return (5, straight_high)

            # Three-of-a-kind
            if counts[0][1] == 3:
                triple = counts[0][0]
                kickers = sorted([v for v in values if v != triple], reverse=True)
                return (4, triple, kickers)

            # Two pair
            if len(counts) >= 2 and counts[0][1] == 2 and counts[1][1] == 2:
                pair1 = counts[0][0]
                pair2 = counts[1][0]
                kicker = max([v for v in values if v != pair1 and v != pair2])
                return (3, max(pair1, pair2), min(pair1, pair2), kicker)

            # One pair
            if counts[0][1] == 2:
                pair = counts[0][0]
                kickers = sorted([v for v in values if v != pair], reverse=True)
                return (2, pair, kickers)

            # High card: nothing else qualifies
            return (1, values)

        def best_hand_from_seven(cards):
            """
            Given a list of cards (typically 7 in Texas Hold'em),
            find the best 5-card hand.
            """
            best_rank = None
            for combo in itertools.combinations(cards, 5):
                rank = evaluate_hand(combo)
                if best_rank is None or rank > best_rank:
                    best_rank = rank
            return best_rank

        best_score = None
        # Evaluate each player's best hand
        for p in self.active_players:
            # Combine player's hole cards with community cards
            all_cards = p.hand + self.community_cards
            player_best = best_hand_from_seven(all_cards)
            # Optionally store the best hand on the player object:
            p.best_hand_rank = player_best
            if best_score is None or player_best > best_score:
                best_score = player_best

        # Return the IDs of players whose best hand equals the highest found
        winners = [p.id for p in active_players if p.best_hand_rank == best_score]
        return winners

    def betting_round(self):
        """
        Handles a betting round using a rotated order.
        For preflop, the first to act is the player to the left of the big blind.
        Forced bets (ante and blinds) are already in place, so we start with current_bet
        equal to the big blind.
        """
        # Rotate the active players so that the first-to-act is at index 0.
        start_index = self.action_idx
        ordered_players = self.active_players[start_index:] + self.active_players[:start_index]

        # Set the current bet to the big blind (as posted in _start).
        current_bet = self.big_blind
        # Reset each player's bet for this betting round.
        for idx in range(len(self.active_players)):
            self.active_players[idx].current_bet = self.player_pots[idx]

        # Initialize the action queue using the rotated order.
        to_act = ordered_players.copy()

        while to_act and len(self.active_players) >= 2:
            player = to_act.pop(0)
            # The player takes an action. Expected actions are:
            # ["fold"], ["check"], ["call"], or ["raise", amount]
            action = player.model.action()
            self.log.append((player.id, action))

            if action[0] == "fold":
                # Remove the player from active_players.
                self.active_players.remove(player)
                # Also update the ordered list.
                ordered_players = [p for p in ordered_players if p != player]
                continue

            elif action[0] == "check":
                if player.current_bet != current_bet:
                    self.log.append(f"Invalid check by player {player.id}; current bet not met.")
                # No chips are added if it's a valid check.

            elif action[0] == "call":
                call_amt = current_bet - player.current_bet
                player.current_bet += call_amt
                idx = self.active_players.index(player)
                self.player_pots[idx] += call_amt

            elif action[0] == "raise":
                raise_amt = action[1]
                call_amt = current_bet - player.current_bet
                total_contrib = call_amt + raise_amt
                player.current_bet += total_contrib
                idx = self.active_players.index(player)
                self.player_pots[idx] += total_contrib
                # Update the current bet.
                current_bet = player.current_bet
                # After a raise, all other players in the ordered list must respond.
                to_act = [p for p in ordered_players if p != player]

        self.log.append("Betting round complete.")


    def play(self) -> tuple: # return ((self.player_pot, winner_idx), logs)

        self._start()
        self._bettingRound()
        if len(self.active_players) < 2:
            # return
        self.community_cards = self.deck.flop()
        self._bettingRound()
        if len(self.active_players) < 2:
            # return
        self.community_cards = self.deck.turn()
        self._bettingRound()
        if len(self.active_players) < 2:
            # return
        self.community_cards = self.deck.river()
        self._bettingRound()
        if len(self.active_players) < 2:
            # return
        winners = self._calcWinner()
        


