#!/usr/bin/env python3
import re
from typing import List, Tuple

full_deck = [
    'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC',
    'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD',
    'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH',
    'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS'
]

def card_value(card: str) -> int:
    s = (full_deck.index(card) % 13) + 1
    return 10 if s > 10 else s

def count_deadwood(cards: List[str]) -> int:
    return sum(card_value(c) for c in cards)

def card_number_value(card: str) -> int:
    c = re.match(r'^[^CDHS]*', card).group()
    c = '1' if c == 'A' else c
    c = '11' if c == 'J' else c
    c = '12' if c == 'Q' else c
    c = '13' if c == 'K' else c
    return int(c)

def is_number_meld(cards: List[str]) -> bool:
    if len(cards) not in [3, 4]:
        return False
    num = card_number_value(cards[0])
    return all(card_number_value(c) == num for c in cards)

def is_suit_meld(cards: List[str]) -> bool:
    suit = cards[0][-1]
    current_value = card_number_value(cards[0]) + 1
    for c in cards[1:]:
        if c[-1] != suit or card_number_value(c) != current_value:
            return False
        current_value += 1
    return True

def valid_card(card: str) -> bool:
    return bool(re.match(r'^(10|[2-9AKQJ])[CDHS]$', card, re.I))

def hand_string(arr: List[str]) -> str:
    return ' '.join(arr) if arr else ''

def sort_by_value(hand: List[str]) -> List[str]:
    return sorted(hand, key=lambda a: (card_number_value(a), a[-1]))

def sort_by_suit(hand: List[str]) -> List[str]:
    return sorted(hand, key=lambda a: (a[-1], card_number_value(a)))

class MeldNode:
    def __init__(self, cards: List[str], parent):
        self.cards = cards
        self.parent = parent
        self.deadwood = count_deadwood(cards) + (parent.deadwood if parent else 0)

def clean_meld_group(melds: List[List[str]], meld: List[str]) -> List[List[str]]:
    return [m for m in melds if not any(c in m for c in meld)]

def build_meld_tree(melds: List[List[str]], root_meld) -> MeldNode:
    best = root_meld
    for m in melds:
        n = MeldNode(m, root_meld)
        new_tree = build_meld_tree(clean_meld_group(melds, m), n)
        if best is None or (new_tree and new_tree.deadwood > best.deadwood):
            best = new_tree
    return best

def get_meld_set(leaf_node: MeldNode) -> List[List[str]]:
    arr = []
    n = leaf_node
    while n:
        arr.append(n.cards)
        n = n.parent
    return arr

def get_best_combination(melds: List[List[str]]) -> Tuple[int, List[List[str]]]:
    best_leaf = build_meld_tree(melds, None)
    if best_leaf is None:
        return 0, []
    best_melds = get_meld_set(best_leaf)
    return best_leaf.deadwood, best_melds

def compute_deadwood(cards: List[str]) -> Tuple[List[List[str]], List[str], int]:
    if len(cards) != 10:
        raise ValueError("Exactly 10 cards are required.")
    
    for c in cards:
        if not valid_card(c):
            raise ValueError(f"Invalid card detected: {c}")
    
    hand = [c.upper() for c in cards]
    all_melds = []

    # First, check for 4 card melds of the same-numbered card
    hand = sort_by_value(hand)
    for i in range(len(hand) - 3):
        poss_meld = hand[i:i + 4]
        if is_number_meld(poss_meld):
            all_melds.append(poss_meld)
            all_melds.append([poss_meld[0], poss_meld[1], poss_meld[3]])
            all_melds.append([poss_meld[0], poss_meld[2], poss_meld[3]])

    # Next, check for 3 card melds of the same-numbered card
    for i in range(len(hand) - 2):
        poss_meld = hand[i:i + 3]
        if is_number_meld(poss_meld):
            all_melds.append(poss_meld)

    # Next, check for 3 card melds in the same suit
    hand = sort_by_suit(hand)
    for i in range(len(hand) - 2):
        poss_meld = hand[i:i + 3]
        if is_suit_meld(poss_meld):
            all_melds.append(poss_meld)

    # Next, 4 card melds
    for i in range(len(hand) - 3):
        poss_meld = hand[i:i + 4]
        if is_suit_meld(poss_meld):
            all_melds.append(poss_meld)

    # Finally, 5 card melds
    for i in range(len(hand) - 4):
        poss_meld = hand[i:i + 5]
        if is_suit_meld(poss_meld):
            all_melds.append(poss_meld)

    # All possible melds have been found. Now, find the optimal set of melds.
    all_melds.sort(key=lambda a: count_deadwood(a))
    best_score, best_melds = get_best_combination(all_melds)
    deadwood = count_deadwood(hand) - best_score
    deadwood_cards = sort_by_value([c for c in hand if c not in [card for meld in best_melds for card in meld]])

    return best_melds, deadwood_cards, deadwood

# Optional: Example usage
if __name__ == "__main__":
    sample_hand = ['1C', 'AD', 'AS', '4C', '5C', '6C', '7C', 'QD', '10H', '4H']
    try:
        melds, deadwood, value = compute_deadwood(sample_hand)
        print("Optimal melds:")
        for m in melds:
            print(f"  {' '.join(m)}")
        print(f"Deadwood: {' '.join(deadwood)} (value: {value})")
    except ValueError as e:
        print(e)