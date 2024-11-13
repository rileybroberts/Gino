#!/usr/bin/ruby
#
# If you want to understand how this script works, I'd recommend starting to read it
# at the "entry point" where it starts validating and parsing the arguments---just
# look for the lines interacting with ARGV to get the initial list of cards.  From
# there you can follow how it generates the full set of candidate melds (which may
# overlap) and then how it builds a "tree" where each path to a leaf node defines a
# non-overlapping set of melds.

usage = "deadwood.rb:
This program takes 10 command line args - the cards in a gin hand, and prints
a list of optimal melds and deadwood cards to stdout.

Example:

    $ ruby deadwood.rb ac ad as 4c 5c 6c 7c qd 10h 4h

    Optimal melds:
      4C 5C 6C 7C
      AC AD AS
    Deadwood: 4H 10H QD (value: 24)"

$full_deck = ['AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC',
              'AD', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD',
              'AH', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH',
              'AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS']

def card_value(card)
  s = ($full_deck.index(card) % 13) + 1
  (s > 10) ? 10 : s
end

def count_deadwood(cards)
  d = 0
  cards.each {|c| d += card_value(c)}
  d
end

def card_number_value(card)
  c = card[/^[^CDHS]*/]
  c = (c == 'A') ? '1' : c
  c = (c == 'J') ? '11' : c
  c = (c == 'Q') ? '12' : c
  c = (c == 'K') ? '13' : c
  c.to_i
end

def is_number_meld(cards)
  return false if ((cards.size != 3) && (cards.size != 4))
  num = card_number_value(cards[0])
  cards.each {|c| return false if (card_number_value(c) != num)}
  true
end

def is_suit_meld(cards)
  suit = cards[0][/.$/]
  current_value = card_number_value(cards[0]) + 1
  cards.each {|c| return false if (c[/.$/] != suit)}
  cards[1..(cards.size)].each do |c|
    return false if (card_number_value(c) != current_value)
    current_value += 1
  end
  true
end

def valid_card(card)
  (card =~ /[2-9AKQJ][CDHS]/i) || (card =~ /10[CDHS]/i)
end

def hand_string(arr)
  s = ""
  arr.each {|card| s << "#{card.to_s} "}
  return "" if (s.size == 0)
  return s[0..(s.size - 2)]
end

# Returns cards sorted first by number value, then by suit
def sort_by_value(hand)
  return hand.sort do |a, b|
    a_val = card_number_value(a)
    b_val = card_number_value(b)
    c = a_val <=> b_val
    if (c == 0)
      c = a[/.$/] <=> b[/.$/]
    end
    c
  end
end

# Returns cards sorted first by suit, then by number value
def sort_by_suit(hand)
  return hand.sort do |a, b|
    a_val = card_number_value(a)
    b_val = card_number_value(b)
    c = a[/.$/] <=> b[/.$/]
    if (c == 0)
      c = a_val <=> b_val
    end
    c
  end
end

class MeldNode
  attr_accessor :cards, :deadwood, :parent
  def initialize(cards, parent)
    @parent = parent
    @cards = cards
    @deadwood = count_deadwood(cards)
    if (parent != nil)
      @deadwood = @parent.deadwood + @deadwood
    end
  end
end

# Returns a new array of melds, containing all melds from the initial group,
# except for ones that contain cards from the given meld.
def clean_meld_group(melds, meld)
  to_return = []
  melds.each {|m| to_return << m}
  meld.each do |c|
    to_return.delete_if {|m| (m.index(c) != nil)}
  end
  to_return
end

# Returns the leaf node for which parent pointers can be followed to obtain the
# best possible meld combinations.
# This could be a O(n!) algorithm, where n is the number of melds. But in
# normal use, it shouldn't ever approach something too infeasible, because any
# large set of melds should include an enourmous amount of overlapping melds,
# which will be eliminated from recursive calls. The max recursion depth will
# be equal to the largest number of non-overlapping melds.
def build_meld_tree(melds, root_meld)
  best = root_meld
  melds.each do |m|
    n = MeldNode.new(m, root_meld)
    new_tree = build_meld_tree(clean_meld_group(melds, m), n)
    best = new_tree if (best == nil) || (new_tree.deadwood > best.deadwood)
  end
  best
end

# Follows a path up to the root, and gets an array of melds
def get_meld_set(leaf_node)
  arr = []
  n = leaf_node
  while (n != nil)
    arr << n.cards
    n = n.parent
  end
  arr
end

# Returns an array containing the best score and best melds
def get_best_combination(melds)
  best_score = 0
  best_melds = []
  best_leaf = build_meld_tree(melds, nil)
  best_score = best_leaf.deadwood
  best_melds = get_meld_set(best_leaf)
  [best_score, best_melds]
end

if (ARGV.size != 10)
  puts usage
  exit 1
end

ARGV.each do |c|
  if (!valid_card(c))
    puts usage
    exit 2
  end
end

hand = []
ARGV.each {|c| hand << c.upcase}
all_melds = []
# First, check for 4 card melds of the same-numbered card
hand = sort_by_value(hand)
(hand.size - 3).times do |i|
  poss_meld = hand[i..(i + 3)]
  if is_number_meld(poss_meld)
    all_melds << poss_meld
    # When a 4-card meld is found, also add all the possible 3-card melds which
    # won't be picked up by the subsequent 3-card scan.
    all_melds << [poss_meld[0], poss_meld[1], poss_meld[3]]
    all_melds << [poss_meld[0], poss_meld[2], poss_meld[3]]
  end
end
# Next, check for 3 card melds of the same-numbered card
(hand.size - 2).times do |i|
  poss_meld = hand[i..(i + 2)]
  all_melds << poss_meld if is_number_meld(poss_meld)
end
# Next, check for 3 card melds in the same suit
hand = sort_by_suit(hand)
(hand.size - 2).times do |i|
  poss_meld = hand[i..(i + 2)]
  all_melds << poss_meld if is_suit_meld(poss_meld)
end
# Next, 4 card melds
(hand.size - 3).times do |i|
  poss_meld = hand[i..(i + 3)]
  all_melds << poss_meld if is_suit_meld(poss_meld)
end
# Finally, 5 card melds
(hand.size - 4).times do |i|
  poss_meld = hand[i..(i + 4)]
  all_melds << poss_meld if is_suit_meld(poss_meld)
end
# 6 or more card melds are equivalent to multiple smaller melds.

# All possible melds have been found. Now, find the optimal set of melds.
all_melds.sort! {|a, b| count_deadwood(a) <=> count_deadwood(b)}
a = get_best_combination(all_melds)
deadwood = count_deadwood(hand) - a[0]
puts "Optimal melds:"
best_melds = a[1]
best_melds.each do |m|
  puts "  " + hand_string(m)
  m.each {|c| hand.delete(c)}
end
puts "Deadwood: #{hand_string(sort_by_value(hand))} (#{deadwood.to_s})"

# puts "All possible melds:"
# all_melds.each {|m| puts hand_string(m)}