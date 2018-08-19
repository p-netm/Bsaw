"""
DETAILS
bet     Occurences    pdf(Actual odds)  Bookmakers_odds         cdf
x2       20             40.82                 50              0--40.82
x4       10             20.41                 25              40.83--61.23
x5        8             16.33                 20              61.24--77.56
x10       4             8.16                  10              77.57--85.72
x20       2             4.08                  5               85.73--89.80
x40       1             2.04                  2.5             89.81--91.84
1free     2             4.08                  -               91.84--95.92
2free     1             2.04                  -               95.92--97.96
4free     1             2.04                  -               97.97--100

TOTAL     49            100.00                112.5

Holy shit the house advantage on this is 12.5%, that is very greedy
"""

import random


class SpinWheel(object):
    choicedict = {
        'x2': 20,
        'x4': 10,
        'x5': 8,
        'x10': 4,
        'x20': 2,
        'x40': 1,
        '1free': 2,
        '2free': 1,
        '4free': 1
    }

    def __init__(self, capital):
        self.capital = capital

    def spin(self):
        res = ['x2',
               'x4',
               'x5',
               'x10',
               'x20',
               'x40',
               '1free',
               '2free',
               '4free']
        cdf = [
            (0, 40.82),
            (40.83, 61.23),
            (61.24, 77.56),
            (77.57, 85.72),
            (85.73, 89.80),
            (89.81, 91.84),
            (91.84, 95.92),
            (95.92, 97.96),
            (97.97, 100)]
        rand = random.random() * 100
        for index, value in cdf:
            if value[0] <= rand <= value[1]:
                return res[index]

    def little_knapsack(self, amount):
        """denominations: 1000, 500, 250, 100, 50, 25"""
        return (amount // 25) * 25

    def arb(self, args, amount):
        """define the arb amounts, to determine the stake for each bet"""
        res = {}
        valid = ['x2',
               'x4',
               'x5',
               'x10',
               'x20',
               'x40']
        if amount >  self.capital:
            raise ValueError("In these case you would need to recharg your account")
        elif amount > 20000:
            raise ValueError("Guys at betin do not allo bets with stakes over 20000, sorry")
        if len(args) == 1:
            res[args[0]] = amount
            self.capital =- amount
            return res
        elif len(args) > 1:
            temp = [int(i.strip('x')) for i in range(len(args))]
            temp_tot = sum([1 / num for num in temp])
            # validate
            for i in args:
                if i not in valid:
                    raise ValueError("%s not in spinning wheel" % i)
                else:
                    res[i] = self.little_knapsack(int(int(i.strip('x')) / temp_tot * amount))
                    self.capital =- res[i]
        return res


def choose_iter(elements, length):
    for i in range(len(elements)):
        if length == 1:
            yield (elements[i],)
        else:
            for next in choose_iter(elements[i + 1:len(elements)], length - 1):
                yield (elements[i],) + next


def choose(l, k):
    return list(choose_iter(l, k))


def pick_bets():
    """62 combinations and we start with the first and end with the last"""
    valid = ['x2',
             'x4',
             'x5',
             'x10',
             'x20',
             'x40']
    for i in range(len(valid)):
        res = choose(valid, i)
        for i in res:
            yield i

