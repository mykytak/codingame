import sys
import math



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
    self.hand.cards.sort(key=lambda card: card.value)

    self.field.prepare()
    he.field.prepare(True)

    actions = ''

    actions += self.hand.getActions()
    actions += self.field.forSureKills()
    actions += self.field.cleanBoard()
    actions += self.field.attackPlayer()

    actions += self.hand.getActions()
    actions += self.field.forSureKills()
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
    for i, c in enumerate(self.cards):
      if c.id == card.id:
        del self.cards[i]
        return True

    return False



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
      actions += 'ATTACK %s %s; ' % (attacker.id, enemy.id)
      attacker.hit(enemy)
      self.offense -= attacker.attack

      if enemy.defense <= 0:
        break
    else:
      he.field.cards.remove(enemy)
      he.field.offense -= enemy.attack

    return actions


  def forSureKills(self):
    actions = ''

    guards = [card for card in he.field.cards if card.G]
    guardsTotal = len(guards)

    for enemy in guards:
      for card in self.cards:
        if card.killingPower(enemy) == 0:
          actions += 'ATTACK %s %s;' % (card.id, enemy.id)
          self.remove(card)
          he.field.remove(enemy)
          guardsTotal -= 1

    if guardsTotal != 0:
      return actions

    for card in self.cards:
      for enemy in he.field.cards:
        if card.killingPower(enemy) == 0:
          actions += 'ATTACK %s %s;' % (card.id, enemy.id)
          self.remove(card)
          he.field.remove(enemy)

    return actions


  def cleanBoard(self):
    actions = ''
    guards = [c for c in he.field.cards if 'G' in c.abilities]

    if guards == [] and self.offense > he.field.defense:
      return actions

    if guards != []:
      for g in guards:
        actions += self.hit(g)

    if he.field.cards == []:
      return actions

    # disabled till 'guaranteed kills' function will be implemented
    # meTurnsToKill = he.health / self.offense if self.offense > 0 else 99
    # heTurnsToKill = me.health / he.field.offense if he.field.offense > 0 else 99
    # if meTurnsToKill < heTurnsToKill:
    #   return actions

    targets = iter(he.field.cards)
    while he.field.cards != [] or self.cards != []:
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
    if not enemy: self.cards.sort(key=lambda card: card.value,  reverse=True)
    else:         self.cards.sort(key=lambda card: card.threat, reverse=True)

    self.offense = sum([card.attack  for card in self.cards])
    self.defense = sum([card.defense for card in self.cards])



class Card:
  @classmethod
  def parse(cls):
    card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw = input().split()

    args = {
      'cardClass':  int(card_number),
      'id':         int(instance_id),
      'location':   int(location),
      'type':       int(card_type),
      'cost':       int(cost),
      'attack':     int(attack),
      'defense':    int(defense),
      'abilities':  abilities
    }

    if args['type'] == Const.CREATURE: return Creature(args)
    elif args['type'] == Const.GREEN:  return ItemGreen(args)
    elif args['type'] == Const.RED:    return ItemRed(args)
    elif args['type'] == Const.BLUE:   return ItemBlue(args)
    else: raise Exception('Card type not found')


  def __init__(self, args = []):
    for key in args:
      setattr(self, key, args[key])

    self.B = 'B' in self.abilities
    self.C = 'C' in self.abilities
    self.G = 'G' in self.abilities
    self.D = 'D' in self.abilities
    self.L = 'L' in self.abilities
    self.W = 'W' in self.abilities

    self.draftValue = 0
    self.threat = 0

    self.value = (self.attack + self.defense) / max(self.cost, 0.5)


  def __repr__(self):
    return "%s: %s/%s %s v%.3f t%s; dw:%.3f\n" % (self.id, self.attack, self.defense, self.abilities, self.value, self.threat, self.draftValue)



class Creature(Card):
  def __init__(self, args):
    super().__init__(args)

    self.value = (self.attack + self.defense) / max(self.cost, 0.5)

    if self.B: self.value += 2 / max(self.cost, 0.5)
    if self.C: self.value += 2 / max(self.cost, 0.5)
    if self.D: self.value += 2 / max(self.cost, 0.5)

    if self.G: self.value += 6 / max(self.cost, 0.5)

    if self.L: self.value += 2 / max(self.cost, 0.5)
    if self.W: self.value += 2 / max(self.cost, 0.5)


    self.threat = self.attack + (self.attack - self.defense) + sum([2 for x in self.abilities if x in ['B', 'D']]) + (10 if self.L else 0)


  # used only while in hand right now
  def action(self):
    if self.cost > me.mana:
      return None

    if self.C:
      me.field.add(self)

    me.mana -= self.cost

    return 'SUMMON %s' % (self.id)


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
      return -math.pow(self.attack - enemy.defense, 2) - self.defense

    # + min because min always will be negative
    return -math.pow(self.attack - enemy.defense, 2) + min(0, self.defense - enemy.attack) * (enemy.attack - self.attack)


  def hit(self, enemy):
    if self.L and not enemy.W:
      enemy.defense = 0
      return

    if enemy.W:
      enemy.W = False
      return

    enemy.defense -= self.attack




class ItemGreen(Card):
  def action(self):
    if me.field.cards == []:
      return None

    return 'USE %s %s;' % (self.id, me.field.cards[0].id)



class ItemRed(Card):
  def action(self):
    if he.field.cards == []:
      return None

    return 'USE %s %s;' % (self.id, he.field.cards[0].id)



class ItemBlue(Card):
  def action(self):
    return 'USE %s %s;' % (self.id, '-1')




class Hand(Deck):
  def getActions(self):
    actions = "; ".join(filter(None, [card.action() for card in self.cards])) + "; "
    return actions




class Draft:
  def __init__(self):
    self.cards = []
    self.low  = 0
    self.mid  = 0
    self.high = 0

    self.left = 30

    self.targetLow  = 5
    self.targetMid  = 0
    self.targetHigh = 3


  def parse(self):
    self.cards = []
    for i in range(3):
      card = Card.parse()
      card.place = i
      self.cards.append(card)


  def choose(self):
    for card in self.cards:
      # last line: the more powerful card, the less attack/defense to cost matter
      card.draftValue = card.value + \
                        max(((self.targetLow - self.low) * self.left / 10 if card.cost in [0,1,2] else \
                        ((self.targetMid - self.mid) * self.left / 10 if card.cost in [3,4,5,6] else \
                        (self.targetHigh - self.high) * self.left / 10 )), 0)
                        # + card.cost * 0.5 * card.value
                        # + math.pow(card.cost - 6, 2) * 0.2 * card.value * 0.1

    self.cards.sort(key=lambda card: card.draftValue, reverse=True)

    res = self.cards[0]
    if res.cost < 3: self.low += 1
    elif res.cost < 6: self.mid += 1
    else: self.high += 1

    self.left -= 1

    return res.place


  def clean(self):
    self.cards = []




me = Player()
he = Player()

draft = Draft()

draftTurns = 30

# game loop
while True:

  me.parseInput()
  he.parseInput()

  opponent_hand = int(input())
  card_count = int(input())

  if draftTurns > 0:
    draft.parse()
    print("PICK %s" % (draft.choose()))
    draftTurns -= 1
    continue


  for i in range(card_count):
    card = Card.parse()

    if card.location == 0:
      me.hand.add(card)
    elif card.location == 1:
      me.field.add(card)
    else:
      he.field.add(card)


  print(me.action())

