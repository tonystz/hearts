"""This module containts the abstract class Player and some implementations."""
from random import shuffle

from card import Suit, Rank, Card, Deck
from rules import is_card_valid


class Player:

    """
    Abstract class defining the interface of a Computer Player.
    """

    def pass_cards(self, hand):
        """Must return a list of three cards from the given hand."""
        return NotImplemented

    def play_card(self, hand, trick, trick_nr, are_hearts_broken):
        """
        Must return a card from the given hand.
        trick is a list of cards played so far.
        trick can thus have 0, 1, 2, or 3 elements.
        are_hearts_broken is a boolean indicating whether the hearts are broken yet.
        trick_nr is an integer indicating the current trick number, starting with 0.
        """
        return NotImplemented

    def see_played_trick(self, trick, trick_nr):
        """
        Allows the player to have a look at all four cards in the trick being played.
        """
        pass



class StupidPlayer(Player):

    """
    Most simple player you can think of.
    It just plays random valid cards.
    """

    def pass_cards(self, hand):
        return hand[:3]

    def play_card(self, hand, trick, trick_nr, are_hearts_broken):
        # Play first card that is valid
        for card in hand:
            if is_card_valid(hand, trick, card, trick_nr, are_hearts_broken):
                return card
        raise AssertionError(
            'Apparently there is no valid card that can be played. This should not happen.'
        )


class SimplePlayer(Player):

    """
    This player has a notion of a card being undesirable.
    It will try to get rid of the most undesirable cards while trying not to win a trick.
    """

    def __init__(self, verbose=True):
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
                    
    def play_card(self, hand, trick, trick_nr, are_hearts_broken):
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


class ExpertPlayer(Player):

    """
    This player has a notion of a card being undesirable.
    It will try to get rid of the most undesirable cards while trying not to win a trick.
    """

    def __init__(self, verbose=True):
        self.verbose = verbose

    def say(self, message, *formatargs):
        if self.verbose:
            print(message.format(*formatargs))

    def undesirability(self, card):
        return (
            card.rank.value
            + (10 if card.suit == Suit.spades and card.rank >= Rank.queen else 0)
        )

    def pass_cards(self, hand):
        self.say('Hand before passing: {}', hand)
        hand_copy = hand.copy()
        cards_to_pass = []
        for _ in range(0, 3):
            spades_in_hand = [card for card in hand_copy if card.suit == Suit.spades]
            if len(spades_in_hand) < 6 and any(card.rank == Rank.queen for card in spades_in_hand):
                card_to_pass = Card(Suit.spades, Rank.queen)
            elif len(spades_in_hand) < 6 and any(card.rank == Rank.ace for card in spades_in_hand):
                card_to_pass = Card(Suit.spades, Rank.ace)            
            elif len(spades_in_hand) < 6 and any(card.rank == Rank.king for card in spades_in_hand):
                card_to_pass = Card(Suit.spades, Rank.king)
            else:
                other_suits_in_hand = [self._cards_with_suit(Suit.clubs, hand_copy), self._cards_with_suit(Suit.diamonds, hand_copy), self._cards_with_suit(Suit.hearts, hand_copy)]
                suits_array = [x for x in other_suits_in_hand if len(x) != 0]
                min_suit_array = min(suits_array, key=len)
                card_to_pass = min_suit_array[-1]
            cards_to_pass.append(card_to_pass)
            hand_copy.remove(card_to_pass)
        self.say('Cards to pass: {}', cards_to_pass)
        return cards_to_pass
                    
    def play_card(self, hand, trick, trick_nr, are_hearts_broken):
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

    def _cards_with_suit(self, suit, cards):
        return [card for card in cards if card.suit == suit]