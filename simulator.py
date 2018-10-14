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
from myloger import flog
import matplotlib.pyplot as plt

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
                flog.info("spin: %s" % res[index])
                return res[index]

    def little_knapsack(self, amount):
        """denominations: 1000, 500, 250, 100, 50, 25"""
        stake = (amount // 25) * 25
        if stake == 0:
            raise Exception("Broke")
        return stake

    def arb(self, args):
        """define the arb amounts, to determine the stake for each bet"""
        amount = int(self.capital / 2)
        res = {}
        valid = ['x2','x4','x5','x10','x20','x40']
        try:
            if amount >  self.capital:
                raise ValueError("In these case you would need to recharg your account")
            elif amount > 20000:
                raise ValueError("Guys at betin do not allow bets with stakes over 20000, sorry")
        except ValueError as err:
            if err.args[0] == "Guys at betin do not allow bets with stakes over 20000, sorry":
                amount = 20000
            else:
                raise err
        if len(args) == 1:
            res[args[0]] = amount
            self.capital = self.capital - amount
            return res
        elif len(args) > 1:
            temp = [int(i.strip('x')) for i in args]
            temp_tot = sum([1 / num for num in temp])
            if temp_tot >= 1:
                raise Exception("Cannot arbitrage on this combination")
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
    flog.debug("start Single_simulation on %s with %s" % (str(arbs), repr(wheel)))
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
    flog.debug("End of Simulation round; stats: capital_change: %d; current wheel capital: %d"
               % (capital_change, wheel.capital))
    return capital_change

def simulation(howmany):
    LOADED_CAPITAL = 1000
    # we are running a (1000)how many simulations for each respective combination
    for arg in pick_bets():  # decide what of the 62 combinations you will be usitng
        flog.info("Beginning new run for %s, this combination" % str(arg))
        yaxis = [LOADED_CAPITAL] # hold the arg value for each simulation, pending plotting
        wheel = SpinWheel(LOADED_CAPITAL)
        # pass it to wheel.arb, to know how much to stake on each
        try:
            for i in range(howmany):
                arbs = wheel.arb(arg)
                wheel.capital = wheel.capital + single_simulation(wheel, arbs)
                yaxis.append(wheel.capital)
                # tracking this data via plot graph -> for each arg we can create a plot that follows the
                # the arb and takes all the said "howmany" nuimber of simulations as one data point
                # for respective arb
        except Exception as err:
            if err.args[0] == "Broke" or err.args[0] == "In these case you would need to recharge your account":
                # print('message: ', err ,' :on :%s' % str(arg))
                pass
            elif err.args[0] == "Cannot arbitrage on this combination":
                break
            else:
                raise err
        finally:
            flog.info("!MPORTANT: %s starter bet: %d : ending stake: %d" % (arg, LOADED_CAPITAL, wheel.capital))
            print("!MPORTANT: %s starter bet: %d : ending stake: %d" % (arg, LOADED_CAPITAL, wheel.capital))
            plt.ylabel('Cost for each 62 combinations')
            plt.xlabel('Number of simulations')
            if wheel.capital > LOADED_CAPITAL:
                plt.plot(yaxis, label = '%s' % str(arg))
    leg  = leg = plt.legend(loc='best', ncol=1, fontsize='x-small', mode="expand", shadow=True, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    plt.title('Betin Spin and Win Simulation(%d)' % howmany)
    plt.show()

if __name__ == "__main__":
    simulation(50)

#Write some damn fucking Tests:
