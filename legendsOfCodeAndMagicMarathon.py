import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def debug(msg):
  print(msg, file=sys.stderr)



class Const:
  CREATURE = 0
  GREEN = 1
  RED = 2
  BLUE = 3



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
    self.hand.cards.sort(key=lambda card: card.value)
    self.field.cards.sort(key=lambda card: card.value)
    he.field.cards.sort(key=lambda card: card.value)

    actions = ''

    actions += self.hand.getActions()
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
  def getActions(self):
    mana = me.mana
    actions = ''


    for card in self.cards:

      if card.cost <= mana:
        if card.type == Const.CREATURE:
          actions += 'SUMMON ' + str(card.id) + '; '

          if 'C' in card.abilities:
            me.field.add(card)

          mana -= card.cost

        elif card.type == Const.GREEN:
          if me.field.cards == []:
            continue

          actions += 'USE %s %s;' % (card.id, me.field.cards[0].id)

        elif card.type == Const.RED:
          if he.field.cards == []:
            continue

          actions += 'USE %s %s;' % (card.id, he.field.cards[0].id)

        elif card.type == Const.BLUE:
          actions += 'USE %s %s;' % (card.id, '-1')

    return actions



class Field(Deck):
  def refresh(self):
    self.cards = []


  def getActions(self):
    res = ''

    guards = [c for c in he.field.cards if 'G' in c.abilities]

    for card in self.cards:
      if card.attack == 0:
        continue

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

    self.cardClass = int(card_number)
    self.id = int(instance_id)
    self.location = int(location)
    self.type = int(card_type)
    self.cost = int(cost)
    self.attack = int(attack)
    self.defense = int(defense)
    self.abilities = abilities
    self.myHealthChange = int(my_health_change)
    self.opponentHealthChange = int(opponent_health_change)
    self.draw = int(card_draw)

    """

    B, C, D - attack
    G - defense
    L - oposite attack
    W - oposite defense

    1/1 for 1

    base = a/cost + d/cost

    a + 2 for modifiers
    d + 2 for modifiers

      a/d - cost
    + d * 2 if G

    """


    if self.type == Const.CREATURE:
      self.value = (self.attack + 1 + sum([2 for x in abilities if x in ['B','C','D']])) / (self.cost + 1) \
                 + (self.defense + 1 + (4 if 'G' in abilities else 0)) / (self.cost + 1) \
                 + sum([2 for x in abilities if x in ['L', 'W']]) / 2

      # self.attack * (2 if 'B' in attributes else 1) - self.cost \
      #            + self.defense - self.cost \
    else:
      self.value = (self.attack + self.defense - self.cost * 2)


    # if self.type == Const.CREATURE:
    #   self.value +=  (1 if 'B' in abilities else 0) \
    #                + (1 if 'C' in abilities else 0) \
    #                + (1 if 'G' in abilities else 0) \
    #                + (1 if 'D' in abilities else 0) \
    #                + (1 if 'L' in abilities else 0) \
    #                + (1 if 'W' in abilities else 0)



class Draft:
  def __init__(self):
    self.cards = []

  def parse(self):
    for i in range(3):
      card = Card()
      card.place = i
      self.cards.append(card)

  def choose(self):
    self.cards.sort(key=lambda card: card.value)
    return self.cards[0].place

  def clean(self):
    self.cards = []




me = Player()
he = Player()

draft = Draft()

draftTurns = 30

# game loop
while True:

  stage = 'battle' if draftTurns == 0 else 'draft'

  me.parseInput()
  he.parseInput()

  opponent_hand = int(input())
  card_count = int(input())

  if stage == 'draft':
    draft.parse()
    print("PICK %s" % (draft.choose()))
    draftTurns -= 1
    continue


  for i in range(card_count):
    card = Card()

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

  # just in case
  print("PASS")

