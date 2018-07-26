import sys
import math

# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!

def debug(msg):
  print(msg, file=sys.stderr)

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

  def canComplete(self):
    return self.cost_a - ctrl.expertise['a'] < 5 \
       and self.cost_b - ctrl.expertise['b'] < 5 \
       and self.cost_c - ctrl.expertise['c'] < 5 \
       and self.cost_d - ctrl.expertise['d'] < 5 \
       and self.cost_e - ctrl.expertise['e'] < 5

  def cost(self):
    return self.cost_total + self.cost_counter

  def enough(self):
    return self.cost_a - ctrl.expertise['a'] <= 0 \
       and self.cost_b - ctrl.expertise['b'] <= 0 \
       and self.cost_c - ctrl.expertise['c'] <= 0 \
       and self.cost_d - ctrl.expertise['d'] <= 0 \
       and self.cost_e - ctrl.expertise['e'] <= 0 \

  def expertise(self):
    return sum([ctrl.expertise['a'] if self.cost_a > 0 else 0,
               ctrl.expertise['b'] if self.cost_b > 0 else 0,
               ctrl.expertise['c'] if self.cost_c > 0 else 0,
               ctrl.expertise['d'] if self.cost_d > 0 else 0,
               ctrl.expertise['e'] if self.cost_e > 0 else 0])

  def _cmpkey(self):
    # return (self.health, self.cost_counter)
    return (self.cost_counter, self.health)

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

  def updateCarried(sample):
    el = next( (el for el in ST.carried if el.id == sample.id), None)
    if el is None:
      return

    index = ST.carried.index(el)
    ST.carried[index] = sample


class Samples:
  name = "SAMPLES"

  def __init__(self):
    self.coef = 0

  def action(self):
    total = ctrl.amount(['s', 'd3', 'd2', 'd1'])
    if total == 3:
      ctrl.next()
      return

    # try:
    #   sample = ST.samples[0]
    # except IndexError:
    #   self.states = 0

    # rank = 2 if ctrl.amount('d2') == 0 else 1

    rank = 1

    if 3 - total + self.coef - ctrl.amount('d3') * 3 - ctrl.amount('d2') * 2 > 0:
      rank = 2

    if 3 - total + self.coef - ctrl.amount('d3') * 3 - ctrl.amount('d2') * 2 > 4:
      rank = 3

    print("CONNECT {}".format(rank))
    ctrl.incAmount('s')

    self.coef -= rank


  def moveTo(self):
    self.coef = ctrl.generalExpertise
    print("GOTO SAMPLES")


class Diagnosis:
  name = "DIAGNOSIS"

  def __init__(self):
    self.key = 0

  def action(self):
    if len(ctrl.samplesForRemove) > 0:
      sample = ctrl.samplesForRemove.pop()
      print("CONNECT {}".format(sample.id))
      ctrl.decAmount('d' + str(sample.rank))
      if sample in ST.carried:
        ST.carried.remove(sample)
      return

    if ctrl.amount('s') == 0:
      ctrl.next()
      return

    sample = ST.samples[0]

    print("CONNECT {}".format(sample.id))
    ctrl.incAmount('d' + str(sample.rank))
    ctrl.decAmount('s')

    if sample.canComplete():
      ctrl.samplesForUpdate.append(sample.id)
    else:
      ctrl.samplesForRemove.append(sample)

    ST.samples = ST.samples[1:]

  def moveTo(self):
    print("GOTO DIAGNOSIS")
    self.key = 0
    ctrl.shouldLoadSamples = True



class Molecules():
  name = "MOLECULES"

  def __init__(self):
    self.states = 10
    self.key = 0

  def checkAvailability(self, sample):
    return sample.cost_a <= ctrl.storage['a'] \
       and sample.cost_b <= ctrl.storage['b'] \
       and sample.cost_c <= ctrl.storage['c'] \
       and sample.cost_d <= ctrl.storage['d'] \
       and sample.cost_e <= ctrl.storage['e']

  def getSampleKey(self, sample):
    if sample.cost_a - ctrl.expertise['a'] > 0 and ctrl.storage['a'] > 0: return ('cost_a', 'a')
    if sample.cost_b - ctrl.expertise['b'] > 0 and ctrl.storage['b'] > 0: return ('cost_b', 'b')
    if sample.cost_c - ctrl.expertise['c'] > 0 and ctrl.storage['c'] > 0: return ('cost_c', 'c')
    if sample.cost_d - ctrl.expertise['d'] > 0 and ctrl.storage['d'] > 0: return ('cost_d', 'd')
    if sample.cost_e - ctrl.expertise['e'] > 0 and ctrl.storage['e'] > 0: return ('cost_e', 'e')

    return (None, None)

  def action(self):
    if ctrl.amount('m') == 10 or self.key >= ctrl.amount(['d3', 'd2', 'd1']):
      ctrl.next()
      return

    try:
      sample = ST.carried[self.key]

      if not sample.canComplete():
        ctrl.samplesForRemove.append(sample)
        # ST.carried.remove(sample)
        self.key += 1
        self.action()
        return

      # if not self.checkAvailability(sample):
      #   self.key += 1
      #   self.action()
      #   return

    except IndexError:
      pass

    if sample.enough():
      self.key += 1
      self.action()
      ctrl.focus_id = -1
      ctrl.amount('saved', 0)
      return

    if ctrl.focus_id < 0:
      ctrl.focus_id = sample.id
      ctrl.amount('saved', sample.cost_total)

    if ctrl.focus_id != sample.id and ctrl.amount('saved') + ctrl.amount('m') == 10:
      ctrl.next()
      return

    (key, mol) = self.getSampleKey(sample)

    if key is None:
      self.key += 1
      self.action()
      return

    if ctrl.storage[mol] == 0:
      self.action()
      return

    sample[key] -= 1
    sample.cost_counter += 1

    print("CONNECT {}".format(mol))
    ctrl.incAmount('m')


  def moveTo(self):
    print("GOTO MOLECULES")
    self.key = 0
    ctrl.shouldLoadSamples = True
    # ST.carried.sort()



class Laboratory():
  name = "LABORATORY"

  def __init__(self):
    self.name = "LABORATORY"
    self.key = 0

  def action(self):
    if ctrl.amount(['d3', 'd2', 'd1']) == 0 or ctrl.amount('m') == 0 or self.key >= ctrl.amount(['d3', 'd2', 'd1']):
      ctrl.next()
      return

    try:
      sample = ST.carried[self.key]
    except IndexError:
      debug("no samples for laboratory")
      return


    if sample.enough():
      print("CONNECT {}".format(sample.id))
      ctrl.decAmount('m', sample.cost())
      ctrl.decAmount('d' + str(sample.rank))
      ST.carried.remove(sample)

      if ctrl.focus_id == sample.id:
        ctrl.focus_id = -1
        ctrl.amount('saved', 0)
      return

    self.key += 1
    self.action()

  def moveTo(self):
    ST.samples = []
    self.key = 0
    print("GOTO LABORATORY")


class Controller:
  def __init__(self):
    self.routes = [Samples(), Diagnosis(), Molecules(), Laboratory()]
    self.key = -1
    self.current = None
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
      'm': 0,
      'l': 0,

      'saved': 0,
    }

    self.shouldLoadSamples = True
    self.samplesForUpdate = []
    self.samplesForRemove = []
    self.storage = {
      'a': 0,
      'b': 0,
      'c': 0,
      'd': 0,
      'e': 0,
    }

    self.generalExpertise = 0
    self.expertise = {
      'a': 0,
      'b': 0,
      'c': 0,
      'd': 0,
      'e': 0
    }

    self.focus_id = -1

  def amount(self, key, value = None):
    if value is not None:
      self.carrying[key] = value
      return

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
      self.next()
      return

    if self.current.name == "DIAGNOSIS" or self.current.name == "MOLECULES":
      self.shouldLoadSamples = False

    self.current.action()

  def next(self):
    self.key = (self.key + 1) % 4
    el = self.routes[self.key]
    el.moveTo()
    self.current = el

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

    if ctrl.current and ctrl.current.name == "SAMPLES":
      ctrl.amount('m', storage_a + storage_b + storage_c + storage_d + storage_e)


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

      if ctrl.shouldLoadSamples:
        # update carrying samples if any
        sample = Sample()

        if sample.carried_by != 0:
          # other bot samples OR samples in the cloud
          continue

        if sample.id in ctrl.samplesForUpdate:
          ST.carried.append(sample)
          ctrl.samplesForUpdate.remove(sample.id)
          continue

        if ctrl.current.name == "DIAGNOSIS" and sample.unknown:
          ST.samples.append(sample)

        #sample = Sample()
        #ST.updateCarried(sample)
      else:
        input()

    if eta > 0:
      print("GOTO {}".format(ctrl.current.name))
      continue

    # ST.samples = sorted([sample for sample in ST.samples if sample.carried_by == -1])

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    ctrl.action()

