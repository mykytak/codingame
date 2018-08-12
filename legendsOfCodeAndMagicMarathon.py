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
    self.health = 0
    self.mana = 0
    self.deck = 0
    self.rune = 0
    self.deck = Deck()
    self.hand = Hand()
    self.field = Field()


  def parseInput(self):
    self.health, self.mana, self.deck, self.rune = [int(j) for j in input().split()]
    self.hand = Hand()
    self.field = Field()


  def action(self):
    self.hand.cards.sort(key=lambda card: card.value, reverse=True)

    self.field.prepare()
    he.field.prepare(True)

    actions = ''

    actions += self.hand.getActions()
    actions += self.field.cleanBoard()
    actions += self.field.attackPlayer()

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


  def hit(self, enemy):
    actions = ''
    while self.cards != []:
      self.cards.sort(key=lambda card: card.killingPower(enemy), reverse=True)
      # nothing with I can continue attack
      if self.cards[0].killingPower(enemy) == -99:
        return actions

      attacker = self.cards.pop(0)
      if attacker.attack == 0:
        continue
      actions += 'ATTACK %s %s; ' % (attacker.id, enemy.id)
      attacker.hit(enemy)
      self.offense -= attacker.attack

      if enemy.defense <= 0:
        break
    else:
      he.field.cards.remove(enemy)
      he.field.offense -= enemy.attack

    return actions

    # if enemy.defense <= 0:
    #   he.field.cards.remove(enemy)
    #   he.field.offense -= enemy.attack


  def cleanBoard(self):
    actions = ''
    guards = [c for c in he.field.cards if 'G' in c.abilities]

    if guards == [] and self.offense > he.field.defense:
      return actions

    if guards != []:
      for g in guards:
        actions += self.hit(g)

    if self.offense >= he.health or he.field.cards == []:
      return actions

    targets = iter(he.field.cards)
    while self.offense <= he.field.offense or he.field.cards != []:
      try:
        target = next(targets)
      except StopIteration:
        break
      actions += self.hit(target)

    return actions


  def attackPlayer(self):
    res = ''

    for card in self.cards:
      if card.attack == 0:
        continue

      res += 'ATTACK %s -1;' % (card.id)

    return res


  def prepare(self, enemy=False):
    # if not enemy: func = lambda card: card.value
    # else:         func = lambda card: card.threat

    if not enemy: self.cards.sort(key=lambda card: card.value, reverse=True)
    else:         self.cards.sort(key=lambda card: card.threat, reverse=True)

    self.offense = 0
    self.defense = 0

    for card in self.cards:
      self.offense += card.attack
      self.defense += card.defense




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

    self.B = 'B' in abilities
    self.C = 'C' in abilities
    self.G = 'G' in abilities
    self.D = 'D' in abilities
    self.L = 'L' in abilities
    self.W = 'W' in abilities

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
                 + (self.defense + 1 + (4 if self.G else 0)) / (self.cost + 1) \
                 + sum([2 for x in abilities if x in ['L', 'W']]) / 2

      self.threat = self.attack + (self.attack - self.defense) + sum([2 for x in abilities if x in ['B', 'D']]) + (10 if self.L else 0)

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


  def killingPower(self, enemy):
    if self.attack == 0:
      return -99

    if self.L and not enemy.W:
      return 99

    if enemy.W:
      if self.L: return -99
      return -self.attack - self.defense

    if enemy.L and self.attack < enemy.defense:
      return -99

    if self.G and self.attack < enemy.defense:
      return -99

    if enemy.L:
      return -math.pow(self.attack - enemy.defense, 2)

    return -math.pow(self.attack - enemy.defense, 2)


  def hit(self, enemy):
    if self.L and not enemy.W:
      enemy.defense = 0
      return

    if enemy.W:
      enemy.W = False
      return

    enemy.defense -= self.attack

  def __repr__(self):
    return "%s: %s/%s %s w%s t%s" % (self.id, self.attack, self.defense, self.abilities, self.value, self.threat)




class Draft:
  def __init__(self):
    self.cards = []
    self.low  = 0
    self.mid  = 0
    self.high = 0

    self.targetLow  = 9
    self.targetMid  = 11
    self.targetHigh = 10

  def parse(self):
    for i in range(3):
      card = Card()
      card.place = i
      self.cards.append(card)

  def choose(self):
    self.cards.sort(key=lambda card: card.value + \
                    (self.targetLow - self.low if card.cost in [0,1,2] else \
                    (self.targetMid - self.mid if card.cost in [3,4,5] else \
                     self.targetHigh - self.high )), reverse=True)

    res = self.cards[0]
    if res.cost < 3: self.low += 1
    elif res.cost < 6: self.mid += 1
    else: self.high += 1

    return res.place

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

