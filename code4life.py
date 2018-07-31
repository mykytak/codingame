import sys
import math

# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!

def debug(msg):
  print(msg, file=sys.stderr)

def removeSample(samplesList, sample):
  for i, val in enumerate(samplesList):
    if val.id == sample.id:
      del samplesList[i]
      break

class ComparableMixin(object):
  def _compare(self, other, method):
    try:
      return method(self._cmpkey(), other._cmpkey())
    except (AttributeError, TypeError):
# _cmpkey not implemented, or return different type,
# so I can't compare with "other".
      return NotImplemented

  def __lt__(self, other):
    return self._compare(other, lambda s, o: s < o)

  def __le__(self, other):
    return self._compare(other, lambda s, o: s <= o)

  def __eq__(self, other):
    return self._compare(other, lambda s, o: s == o)

  def __ge__(self, other):
    return self._compare(other, lambda s, o: s >= o)

  def __gt__(self, other):
    return self._compare(other, lambda s, o: s > o)

  def __ne__(self, other):
    return self._compare(other, lambda s, o: s != o)

"""
  sampleId: unique id for the sample.
  carriedBy: 0 if the sample is carried by you, 1 by the other robot, -1 if the sample is in the cloud.
  rank: ignore for this league.
  gain: ignore for this league.
  health: number of health points you gain from this sample.
  costA, costB, costC, costD, costE: number of molecules of each type needed to research the sample
"""
class Sample(ComparableMixin):
  def __init__(self):
    sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e = input().split()
    self.id = int(sample_id)
    self.carried_by = int(carried_by)
    self.rank = int(rank)
    self.health = int(health)
    self.cost_a = int(cost_a)
    self.cost_b = int(cost_b)
    self.cost_c = int(cost_c)
    self.cost_d = int(cost_d)
    self.cost_e = int(cost_e)

    self.cost_total = self.cost_a + self.cost_b + self.cost_c + self.cost_d + self.cost_e
    self.cost_counter = (-1) * self.cost_total

    self.unknown = self.health == -1

    self._worthiness = self.worthiness()

  def worthiness(self):
    # 1 or 10    for 3,4,5
    # 10, 20, 30 for 5,6,7,8
    # 30, 40, 50 for 7,8,9,10,11,12,13,14
    #              - expertise
    #
    # t - int(ST.turn / 20)
    # h - self.health
    # c - self.cost_total
    # e - ctrl.generalExpertise
    #
    # h - c + e - t + 3

    return self.health - self.cost_total + self.expertise() + 3 # - int(ST.turn / 20) + 3

    # 1  3 0 0 => 0 - 3 + 0 - 0 + 3 = 0
    # 10 3 0 0 => 1 - 3 + 0 - 0 + 3 = 1
    # 1  5 0 0 => 0 - 5 + 0 - 0 + 3 = -2
    # 10 5 0 0 => 1   5           3 = -1
    #
    # 1  3 0 0 => 1  - 3 + 0 - 0 + 3 = 1
    # 10 3 0 0 => 10 - 3 + 0 - 0 + 3 = 10
    # 1  5 0 0 => 1  - 5 + 0 - 0 + 3 = -1
    # 10 5 0 0 => 10   5           3 = 8
    # 10 8 0 0 => 10   8           3 = 5
    # 20 5 0 0 => 20   5           3 = 18
    # 20 8 0 0 => 20   8           3 = 15
    #
    # 20 5 0 10 => 20   5        10 3 = 8
    # 20 8 0 10 => 20   8        10 3 = 5
    #
    # 400 => 20


  def canComplete(self):
    return (self.cost_a == 0 or self.cost_a - ctrl.amount('ma') - ctrl.expertise['a'] <= ctrl.storage['a']) \
       and (self.cost_b == 0 or self.cost_b - ctrl.amount('mb') - ctrl.expertise['b'] <= ctrl.storage['b']) \
       and (self.cost_c == 0 or self.cost_c - ctrl.amount('mc') - ctrl.expertise['c'] <= ctrl.storage['c']) \
       and (self.cost_d == 0 or self.cost_d - ctrl.amount('md') - ctrl.expertise['d'] <= ctrl.storage['d']) \
       and (self.cost_e == 0 or self.cost_e - ctrl.amount('me') - ctrl.expertise['e'] <= ctrl.storage['e']) \
       and (self.missing() <= 10 - ctrl.amount('m'))


  def canProgress(self):
    return self.cost_a > 0 and self.cost_a - ctrl.amount('ma') - ctrl.expertise['a'] < ctrl.storage['a'] \
        or self.cost_b > 0 and self.cost_b - ctrl.amount('mb') - ctrl.expertise['b'] < ctrl.storage['b'] \
        or self.cost_c > 0 and self.cost_c - ctrl.amount('mc') - ctrl.expertise['c'] < ctrl.storage['c'] \
        or self.cost_d > 0 and self.cost_d - ctrl.amount('md') - ctrl.expertise['d'] < ctrl.storage['d'] \
        or self.cost_e > 0 and self.cost_e - ctrl.amount('me') - ctrl.expertise['e'] < ctrl.storage['e']


  def missing(self):
    return max(self.cost_a, self.cost_a - ctrl.amount('ma') - ctrl.expertise['a']) \
         + max(self.cost_b, self.cost_b - ctrl.amount('mb') - ctrl.expertise['b']) \
         + max(self.cost_c, self.cost_c - ctrl.amount('mc') - ctrl.expertise['c']) \
         + max(self.cost_d, self.cost_d - ctrl.amount('md') - ctrl.expertise['d']) \
         + max(self.cost_e, self.cost_e - ctrl.amount('me') - ctrl.expertise['e'])


  def complete(self):
    print("CONNECT {}".format(self.id))

    # if self.cost_a > 0: ctrl.decAmount('ma', self.cost_a - ctrl.expertise['a'])
    # if self.cost_b > 0: ctrl.decAmount('mb', self.cost_b - ctrl.expertise['b'])
    # if self.cost_c > 0: ctrl.decAmount('mc', self.cost_c - ctrl.expertise['c'])
    # if self.cost_d > 0: ctrl.decAmount('md', self.cost_d - ctrl.expertise['d'])
    # if self.cost_e > 0: ctrl.decAmount('me', self.cost_e - ctrl.expertise['e'])

    ctrl.shouldUpdateStorage = True

    ctrl.decAmount('d' + str(self.rank))

    # some weird bug with remove
    # ST.carried.remove(self)

    # for i, val in enumerate(ST.carried):
    #   if val.id == self.id:
    #     del ST.carried[i]
    #     break

    removeSample(ST.carried, self)

    # del ST.carried[ST.carried.index(self)]

    if ctrl.focus_id == self.id:
      ctrl.focus_id = -1
      ctrl.amount('saved', 0)


  def cost(self):
    return self.cost_total + self.cost_counter


  def enough(self):
    return self.cost_a - ctrl.amount('ma') - ctrl.expertise['a'] <= 0 \
       and self.cost_b - ctrl.amount('mb') - ctrl.expertise['b'] <= 0 \
       and self.cost_c - ctrl.amount('mc') - ctrl.expertise['c'] <= 0 \
       and self.cost_d - ctrl.amount('md') - ctrl.expertise['d'] <= 0 \
       and self.cost_e - ctrl.amount('me') - ctrl.expertise['e'] <= 0 \

  def weight(self):
    return 1
    turnsLeft = (400 - ST.turn)
    completedIn = self.cost() - self.expertise()

    if completedIn > turnsLeft * 2:
      return 100

    # coef = 1
    coef = ranksCommon[self.rank] - completedIn

    # if 3 - total + ctrl.generalExpertise - ctrl.amount('d3') * 3 - ctrl.amount('d2') * 2 > 0:
    #   weight = 20
    #
    # if 3 - total + ctrl.generalExpertise - ctrl.amount('d3') * 3 - ctrl.amount('d2') * 2 > 4:
    #   weight = 40

    if ctrl.generalExpertise <= 2:
      coef -= 20

    if ctrl.generalExpertise <= 4:
      coef -= 20

    return self.health - coef


  def expertise(self):
    return sum([ctrl.expertise['a'] if self.cost_a > 0 else 0,
               ctrl.expertise['b'] if self.cost_b > 0 else 0,
               ctrl.expertise['c'] if self.cost_c > 0 else 0,
               ctrl.expertise['d'] if self.cost_d > 0 else 0,
               ctrl.expertise['e'] if self.cost_e > 0 else 0])

  def _cmpkey(self):
    # return (self.health, self.cost_counter)
    # return (self.cost_counter, self.health)
    return self._worthiness

  def __getitem__(self, key):
    return getattr(self, key)

  def __setitem__(self, key, value):
    setattr(self, key, value)

  def __repr__(self):
    return "id: {} carried: {}, health: {}, cost (a{} b{} c{} d{} e{})\n".format(self.id, self.carried_by, self.health, self.cost_a, self.cost_b, self.cost_c, self.cost_d, self.cost_e)


project_count = int(input())
for i in range(project_count):
    a, b, c, d, e = [int(j) for j in input().split()]



class ST:
  state = "SAMPLES"
  samples = []

  carried = []
  turn = 0

  def updateCarried(sample):
    el = next( (el for el in ST.carried if el.id == sample.id), None)
    if el is None:
      return

    index = ST.carried.index(el)
    ST.carried[index] = sample


class Samples:
  name = "SAMPLES"


  def getRank(self):
    total = ctrl.amount(['s', 'd3', 'd2', 'd1'])

    rank = 1

    if 3 - total + self.coef + int(ST.turn / 20) - ctrl.amount('d3') * 3 - ctrl.amount('d2') * 2 > 0:
      rank = 2

    if self.coef >= 4 \
      and 3 - total + self.coef + int(ST.turn / 20) - ctrl.amount('d3') * 3 - ctrl.amount('d2') * 2 > 0:
      rank = 3

    if ST.turn >= 200 and ctrl.generalExpertise > 4:
      rank = 3

    return rank


  def action(self):
    if ctrl.amount(['s', 'd3', 'd2', 'd1']) == 3:
      ctrl.next('d')
      return

    rank = self.getRank()
    print("CONNECT {}".format(rank))
    ctrl.incAmount('s')

    self.coef -= rank * 2


  def moveTo(self):
    self.coef = ctrl.generalExpertise
    ST.samples = []
    ctrl.shouldLoadSamples = True
    print("GOTO SAMPLES")


class Diagnosis:
  """
  should calculate approx benefit from doing current samples
  should drop sample if full and cannot complete any right now
    and took another one that can be completed (calculate by current molecules)
  """
  name = "DIAGNOSIS"

  def reset(self):
    self.key = 0
    self.wasStuck = False
    self.dir = 'm'


  def removeSamples(self):
    if len(ctrl.samplesForRemove) > 0:
      sample = ctrl.samplesForRemove.pop()
      print("CONNECT {}".format(sample.id))
      ctrl.decAmount('d' + str(sample.rank))
      ctrl.cloud.add(sample)
      return True

    return False


  def getFromCloud(self):
    if ctrl.amount(['s', 'd']) == 3:
      return False

    samples = ctrl.checkCloud()
    if len(samples) > 0:
      sample = None
      for s in samples:
        if s.canComplete():
          sample = s
          break
      else:
        return False

      ctrl.cloud.remove(sample)
      print("CONNECT {}".format(sample.id))
      ctrl.incAmount('d' + str(sample.rank))
      ST.carried.append(sample)
      return True

    return False


  def action(self):

    if self.getFromCloud():
      return

    if self.shouldMove():
      ctrl.next(self.dir)
      return

    if self.removeSamples():
      return

    sample = ST.samples[0]

    print("CONNECT {}".format(sample.id))
    ctrl.incAmount('d' + str(sample.rank))
    ctrl.decAmount('s')

    ctrl.samplesForUpdate.append(sample.id)

    ST.samples = ST.samples[1:]


  def shouldMove(self):
    if len(ctrl.samplesForRemove) > 0:
      return False

    if ctrl.amount('s') == 0:
      if ctrl.amount('d') == 0:
        self.dir = 's'
        return True

      canComplete = False
      for s in ST.carried:
        canComplete = canComplete or s.enough() or s.canComplete() # or s.canProgress()
        if canComplete:
          break
      else:
        self.dir = 's'
        ctrl.samplesForRemove += ST.carried
        ST.carried = []
        return False

      return True

    return False


  def moveTo(self):
    print("GOTO DIAGNOSIS")
    self.reset()


class Molecules():
  name = "MOLECULES"

  def reset(self):
    self.key = 0
    self.dir = 's'
    ctrl.shouldLoadSamples = True
    ST.carried.sort(reverse=True)


  def checkAvailability(self, sample):
    return sample.cost_a - ctrl.amount('ma') <= ctrl.storage['a'] \
       and sample.cost_b - ctrl.amount('mb') <= ctrl.storage['b'] \
       and sample.cost_c - ctrl.amount('mc') <= ctrl.storage['c'] \
       and sample.cost_d - ctrl.amount('md') <= ctrl.storage['d'] \
       and sample.cost_e - ctrl.amount('me') <= ctrl.storage['e']


  def getSampleKey(self, sample):
    if sample.cost_a - ctrl.amount('ma') - ctrl.expertise['a'] > 0 and ctrl.storage['a'] > 0: return ('cost_a', 'a')
    if sample.cost_b - ctrl.amount('mb') - ctrl.expertise['b'] > 0 and ctrl.storage['b'] > 0: return ('cost_b', 'b')
    if sample.cost_c - ctrl.amount('mc') - ctrl.expertise['c'] > 0 and ctrl.storage['c'] > 0: return ('cost_c', 'c')
    if sample.cost_d - ctrl.amount('md') - ctrl.expertise['d'] > 0 and ctrl.storage['d'] > 0: return ('cost_d', 'd')
    if sample.cost_e - ctrl.amount('me') - ctrl.expertise['e'] > 0 and ctrl.storage['e'] > 0: return ('cost_e', 'e')

    return (None, None)


  def moveFrom(self):
      enough = False
      for s in ST.carried:
        enough = enough or s.enough()

      if enough:
        ctrl.next('l')
      else:
        ctrl.next('s')
      # analyse other player and probably get rid of samples

      # ctrl.next(self.dir)


  def action(self):
    try:
      sample = ST.carried[self.key]
    except:
      sample = None

    if self.shouldMove(sample):
      self.moveFrom()
      return

    if sample.enough():
      self.key += 1
      self.action()
      ctrl.focus_id = -1
      ctrl.amount('saved', 0)
      return

    if ctrl.focus_id < 0:
      ctrl.focus_id = sample.id
      ctrl.amount('saved', sample.cost_total)

    (key, mol) = self.getSampleKey(sample)

    if key is None:
      self.key += 1
      self.action()
      return

    sample.cost_counter += 1

    if ctrl.focus_id == sample.id:
      ctrl.decAmount('saved')

    print("CONNECT {}".format(mol))
    ctrl.incAmount('m' + mol)

  def shouldMove(self, sample):
    if ctrl.amount('m') == 10 or self.key >= ctrl.amount('d'):
      return True

    if sample is None:
      return True

    if ctrl.focus_id != sample.id and ctrl.focus_id != -1 and ctrl.amount('saved') + ctrl.amount('m') == 10:
      for s in ST.carried:
        if s.canComplete():
          ctrl.focus_id = s.id
          ctrl.amount('saved', sample.missing())
          return False

      return True

    return False


  def moveTo(self):
    self.reset()
    print("GOTO MOLECULES")



class Laboratory():
  name = "LABORATORY"

  """
  should calculate approx benefit from returning to fill other samples
  """

  def reset(self):
    self.key = 0
    self.dir = 's'


  def action(self):
    if self.shouldMove():
      ctrl.next(self.dir)
      return

    sample = ST.carried[self.key]

    if sample.enough():
      sample.complete()
      return

    self.key += 1
    self.action()

  def checkCloud(self):
    totalCurr = ctrl.amount('d')
    if len(ctrl.checkCloud()) >= 3 - totalCurr:
      self.dir = 'd'

  def shouldMove(self):
    currItemsCount = ctrl.amount('d')
    if currItemsCount == 0:
      self.checkCloud()
      return True

    elif self.key >= ctrl.amount('d'):

      canComplete = False
      for s in ST.carried:
        canComplete = canComplete or s.canComplete()

      if not canComplete:
        self.checkCloud()
        return True

      self.dir = 'm'
      return True

    return False

  def moveTo(self):
    self.reset()
    print("GOTO LABORATORY")


class Router:

  def __init__(self):
    self.lastMoves = []
    self.decision  = 's'

  """
  decide if robot should move from module.
  Side effect = self.decision will contain next module to move to
  """
  def shouldMove(self, curr):
    if curr.name == 'SAMPLES':
      pass
    elif curr.name == 'DIAGNOSIS':
      pass
    elif curr.name == 'MOLECULES':
      pass
    elif curr.name == 'LABORATORY':
      pass


class Controller:
  def __init__(self):
    self.routes = [Samples(), Diagnosis(), Molecules(), Laboratory()]
    self.key = -1
    self.current = None
    self.dontReturn = False
    self.lastMoves = []
    self.hash = {
      's': 0,
      'd': 1,
      'm': 2,
      'l': 3
    }

    self.carrying = {
      's': 0,
      'd1': 0,
      'd2': 0,
      'd3': 0,

      'ma': 0,
      'mb': 0,
      'mc': 0,
      'md': 0,
      'me': 0,

      'l': 0,

      'saved': 0,
    }
    # ranksCommon = {
    #   1: {
    #     steps: 8 + 5  - ctrl.generalExpertise,
    #     health: 5,
    #   },
    #   2: {
    #     steps: 8 + 8  - ctrl.generalExpertise,
    #     health: 20,
    #     },
    #   3: {
    #     steps: 8 + 14 - ctrl.generalExpertise,
    #     health: 40
    #     }
    # }

    self.generalExpertise = 0

    self.ranksCommon = {
      1: 8 + 5  - self.generalExpertise + 5,
      2: 8 + 8  - self.generalExpertise + 20,
      3: 8 + 14 - self.generalExpertise + 40,
    }

    self.shouldLoadSamples = True
    self.shouldUpdateStorage = True
    self.samplesForUpdate = []
    self.samplesForRemove = []
    self.storage = {
      'a': 0,
      'b': 0,
      'c': 0,
      'd': 0,
      'e': 0,
    }

    self.expertise = {
      'a': 0,
      'b': 0,
      'c': 0,
      'd': 0,
      'e': 0
    }

    self.focus_id = -1

    self.cloud = Cloud()

  def checkCloud(self, amount = 0):
    if amount == 0:
      return self.cloud.getBest(len(self.cloud.samples))

    return self.cloud.getBest(amount)

  def amount(self, key, value = None):
    if value is not None:
      self.carrying[key] = value
      return

    if key == 'd':
      key = ['d3', 'd2', 'd1']
    elif key == 'm':
      key = ['ma', 'mb', 'mc', 'md', 'me']


    if isinstance(key, list):
      return sum([self.amount(x) for x in key])

    return self.carrying[key]

  def incAmount(self, key):
    self.carrying[key] += 1

  def decAmount(self, key, amount = 1):
    self.carrying[key] -= amount

  def get(self, key):
    ikey = self.hash[key]
    return self.routes[ikey]

  def action(self):

    # first turn
    if self.current is None:
      self.next('s')
      return

    if self.current.name == "DIAGNOSIS" or self.current.name == "MOLECULES":
      self.shouldLoadSamples = False

    self.current.action()

  def next(self, hKey):
    self.key = self.hash[hKey]

    self.lastMoves.append(hKey)
    self.lastMoves = self.lastMoves[-5:]

    el = self.routes[self.key]
    el.moveTo()
    self.current = el

class Cloud:
  samples = []

  def add(self, sample):
    self.samples.append(sample)
    self.samples.sort()

  def getBest(self, count = 1):
    filtered = [s for s in self.samples if s.canComplete()]
    total = len(filtered)

    if total < count:
      return filtered

    return filtered[:a]

  def remove(self, sample):
    # self.samples.remove(sample)
    removeSample(self.samples, sample)

ctrl = Controller()

# game loop
while True:
    # for i in range(2):
    target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e = input().split()
    eta = int(eta)
    score = int(score)
    storage_a = int(storage_a)
    storage_b = int(storage_b)
    storage_c = int(storage_c)
    storage_d = int(storage_d)
    storage_e = int(storage_e)

    if ctrl.shouldUpdateStorage:
      ctrl.amount('ma', storage_a)
      ctrl.amount('mb', storage_b)
      ctrl.amount('mc', storage_c)
      ctrl.amount('md', storage_d)
      ctrl.amount('me', storage_e)
      ctrl.shouldUpdateStorage = False


    expertise_a = int(expertise_a)
    expertise_b = int(expertise_b)
    expertise_c = int(expertise_c)
    expertise_d = int(expertise_d)
    expertise_e = int(expertise_e)

    ctrl.generalExpertise = sum([expertise_a, expertise_b, expertise_c, expertise_d, expertise_e])
    ctrl.expertise = {
        'a': expertise_a,
        'b': expertise_b,
        'c': expertise_c,
        'd': expertise_d,
        'e': expertise_e
    }

    # rival details
    input()

    available_a, available_b, available_c, available_d, available_e = [int(i) for i in input().split()]
    ctrl.storage = {
        'a': available_a,
        'b': available_b,
        'c': available_c,
        'd': available_d,
        'e': available_e
    }
    sample_count = int(input())

    for i in range(sample_count):
      # if ST.state == "SAMPLES":
      #   ST.samples.append(Sample())

      if len(ctrl.samplesForUpdate) > 0:
        sample = Sample()

        if sample.id in ctrl.samplesForUpdate:
          if sample.canComplete() and sample.worthiness() > 0:
            ST.carried.append(sample)
          else:
            ctrl.samplesForRemove.append(sample)
          ctrl.samplesForUpdate.remove(sample.id)
          continue

      elif ctrl.shouldLoadSamples:
        # update carrying samples if any
        sample = Sample()

        if sample.carried_by != 0:
          # other bot samples OR samples in the cloud
          continue

        if ctrl.current.name == "DIAGNOSIS" and sample.unknown:
          ST.samples.append(sample)

        #sample = Sample()
        #ST.updateCarried(sample)
      else:
        input()

    ST.turn += 2

    if eta > 0:
      print("WAIT")
      # print("GOTO {}".format(ctrl.current.name))
      continue

    # ST.samples = sorted([sample for sample in ST.samples if sample.carried_by == -1])

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    ctrl.action()

