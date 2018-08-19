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
        'x2': 20,'x4': 10,'x5': 8,'x10': 4,'x20': 2,'x40': 1,'1free': 2,'2free': 1,'4free': 1
    }

    def __init__(self, capital):
        self.capital = capital

    def __repr__(self):
        return "Wheel %d" % self.capital

    def spin(self):
        res = ['x2', 'x4', 'x5', 'x10', 'x20', 'x40', '1free', '2free', '4free']
        cdf = [(0, 40.82),(40.83, 61.23),(61.24, 77.56),(77.57, 85.72),(85.73, 89.80),(89.81, 91.84),(91.84, 95.92),
               (95.92, 97.96),(97.97, 100)]
        rand = random.random() * 100
        for index, value in enumerate(cdf):
            if value[0] <= rand <= value[1]:
                print(res[index])
                return res[index]

    def little_knapsack(self, amount):
        """denominations: 1000, 500, 250, 100, 50, 25"""
        stake = (amount // 25) * 25
        if stake == 0:
            raise Exception("Broke")
        return stake

    def arb(self, args):
        """define the arb amounts, to determine the stake for each bet"""
        amount = self.capital // 2
        res = {}
        valid = ['x2','x4','x5','x10','x20','x40']
        if amount >  self.capital:
            raise ValueError("In these case you would need to recharg your account")
        elif amount > 20000:
            raise ValueError("Guys at betin do not allow bets with stakes over 20000, sorry")
        if len(args) == 1:
            res[args[0]] = amount
            self.capital = self.capital - amount
            return res
        elif len(args) > 1:
            temp = [int(i.strip('x')) for i in args]
            temp_tot = sum([1 / num for num in temp])
            # validate
            for i in args:
                if i not in valid:
                    raise ValueError("%s not in spinning wheel" % i)
                else:
                    res[i] = self.little_knapsack(int((1 / int(i.strip('x'))) / temp_tot * amount))
                    self.capital = self.capital - res[i]
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
    valid = ['x2','x4','x5','x10','x20','x40']
    for i in range(len(valid)):
        res = choose(valid, i)
        for i in res:
            yield i

def single_simulation(wheel, arbs):
    chance_pick = wheel.spin()
    # call wheel.spin, to simulate the actual spin wheel
    capital_change = 0
    if chance_pick in arbs.keys():
        capital_change += arbs[chance_pick] * int(chance_pick.strip('x'))
    elif chance_pick == '1free':
        capital_change += single_simulation(wheel, arbs)
    elif chance_pick == '2free':
        for i in range(2):
            capital_change += single_simulation(wheel, arbs)
    elif chance_pick == '4free':
        for i in range(4):
            capital_change += single_simulation(wheel, arbs)
    else:
        capital_change += 0
        # check if pick and spin result correlate and hence update the wheel capital
    print('cac', capital_change, wheel.capital)
    return capital_change

def simulation(howmany):
    LOADED_CAPITAL = 20000
    # we are running a 1000 simulations for each respective combination
    for arg in [('x2', 'x4')]:  # decide what of the 62 combinations you will be usitng
        if len(arg) == 3:
            # import pdb; pdb.set_trace()
            pass
        wheel = SpinWheel(LOADED_CAPITAL)
        # pass it to wheel.arb, to know how much to stake on each
        try:
            arbs = wheel.arb(arg)
            for i in range(howmany):
                wheel.capital = wheel.capital + single_simulation(wheel, arbs)
        except Exception as err:
            if err.args[0] == "Broke" or err.args[0] == "In these case you would need to recharg your account":
                print(err)
            else:
                raise err
        finally:
            print("%s starter bet: %d : ending stake: %d" % (arg, LOADED_CAPITAL, wheel.capital))

if __name__ == "__main__":
    simulation(3)

#Write some damn fucking Tests: