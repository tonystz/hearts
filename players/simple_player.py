from players.player import Player
from random import shuffle
from card import Suit, Rank, Card, Deck
from rules import is_card_valid


class SimplePlayer(Player):

    """
    This player has a notion of a card being undesirable.
    It will try to get rid of the most undesirable cards while trying not to win a trick.
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        if verbose:
            deck = Deck()
            deck.cards.sort(key=self.undesirability)
            self.say('Card undesirability: ')
            for card in deck.cards:
                self.say('{}: {}', card, self.undesirability(card))

    def say(self, message, *formatargs):
        if self.verbose:
            print(message.format(*formatargs))

    def undesirability(self, card):
        return (
            card.rank.value
            + (10 if card.suit == Suit.spades and card.rank >= Rank.queen else 0)
        )

    def pass_cards(self, hand):
        hand.sort(key=self.undesirability, reverse=True)
        return hand[:3]
                    
    def play_card(self, hand, trick, trick_nr, are_hearts_broken, is_spade_queen_played):
        # Lead with a low card
        if not trick:
            hand.sort(key=lambda card:
                      100 if not are_hearts_broken and card.suit == Suit.hearts else
                      card.rank.value)
            return hand[0]

        hand.sort(key=self.undesirability, reverse=True)
        self.say('Hand: {}', hand)
        self.say('Trick so far: {}', trick)

        # Safe cards are cards which will not result in winning the trick
        leading_suit = trick[0].suit
        max_rank_in_leading_suit = max([card.rank for card in trick
                                        if card.suit == leading_suit])
        valid_cards = [card for card in hand
                       if is_card_valid(hand, trick, card, trick_nr, are_hearts_broken)]
        safe_cards = [card for card in valid_cards
                      if card.suit != leading_suit or card.rank <= max_rank_in_leading_suit]

        self.say('Valid cards: {}', valid_cards)
        self.say('Safe cards: {}', safe_cards)

        try:
            return safe_cards[0]
        except IndexError:
            queen_of_spades = Card(Suit.spades, Rank.queen)
            # Don't try to take a trick by laying the queen of spades
            if valid_cards[0] == queen_of_spades and len(valid_cards) > 1:
                return valid_cards[1]
            else:
                return valid_cards[0]