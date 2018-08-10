import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def debug(msg):
  print(msg, file=sys.stderr)


class Player:
  def __init__(self):
    self.hp = 0
    self.mana = 0
    self.deck = 0
    self.rune = 0
    self.deck = Deck()
    self.hand = Hand()
    self.field = Field()


  def parseInput(self):
    self.hp, self.mana, self.deck, self.rune = [int(j) for j in input().split()]
    self.hand = Hand()
    self.field = Field()


  def action(self):
    actions = ''
    for a in self.hand.getAvailable():
      actions += 'SUMMON ' + str(a.id) + '; '

    actions += self.field.getActions()

    if actions == '':
      actions = 'PASS'

    return actions



class Deck:
  def __init__(self):
    self.cards = []


  def add(self, card):
    self.cards.append(card)


  def remove(self, card):
    for c, i in enumerate(self.cards):
      if c.id == card.id:
        del self.cards[i]
        return True

    return False



class Hand(Deck):
  def getAvailable(self):
    mana = me.mana
    cards = []


    for card in self.cards:
      if card.cost <= mana:
        cards.append(card)
        mana -= card.cost

    return cards



class Field(Deck):
  def refresh(self):
    self.cards = []


  def getActions(self):
    res = ''

    guards = [c for c in he.field.cards if 'G' in c.abilities]

    for card in self.cards:
      res += 'ATTACK ' + str(card.id)

      if guards != []:
        g = guards[-1]
        res += ' ' + str(g.id) + '; '
        g.defense -= card.attack
        if g.defense <= 0:
          guards.pop()

      else:
        res += ' -1;'

    return res




class Card:
  def __init__(self):
    card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw = input().split()

    self.type = int(card_number)
    self.id = int(instance_id)
    self.location = int(location)
    self.cardType = int(card_type)
    self.cost = int(cost)
    self.attack = int(attack)
    self.defense = int(defense)
    self.abilities = abilities
    self.myHealthChange = int(my_health_change)
    self.opponentHealthChange = int(opponent_health_change)
    self.draw = int(card_draw)




me = Player()
he = Player()

draftTurns = 30

# game loop
while True:

  stage = 'battle' if draftTurns == 0 else 'draft'

  me.parseInput()
  he.parseInput()

  opponent_hand = int(input())
  card_count = int(input())

  for i in range(card_count):
    card = Card()

    if stage == 'draft':
      me.field.add(card)
      continue



    if card.location == 0:
      me.hand.add(card)
    elif card.location == 1:
      me.field.add(card)
    else:
      he.field.add(card)


    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)



  if stage == 'battle':
    print(me.action())
    # battle
    continue

  # draft
  print("PASS")
  draftTurns -= 1

