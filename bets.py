class Odds:

    def __init__(self, odds, web=""):
        if type(odds) != list:
            raise Exception("Must be list of len 2")
        if len(odds) != 2:
            raise Exception("Must be list of len 2")

        self.odds = odds
        self.web = [web, web]

    def update(self, other):
        if other.odds[0] > self.odds[0]:
            self.odds[0] = other.odds[0]
            self.web[0]  = other.web[0]
        if other.odds[1] > self.odds[1]:
            self.odds[1] = other.odds[1]
            self.web[1] = other.web[1]

    def __str__(self):
        fstring = ["{0:^"+str(len(i))+"}" for i in self.web]

        return " ".join([str(o) for o in self.web]) + "\n" + \
               " ".join([f.format(str(o)) for f, o in zip(fstring, self.odds)])

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.odds)

    def get_probability(self):
        return sum([1/o for o in self.odds])

    def sure_bet(self, amount=100):
        if self.get_probability() < 1:
            if len(self.odds) == 2:
                amount = [amount*i/sum(self.odds) for i in self.odds[::-1]]
                return amount

    def sure_bet5(self, amount=100):
        if self.get_probability() < 1:
            if len(self.odds) == 2:
                stake = [5*round(amount*i/sum(self.odds)/5) for i in self.odds[::-1]]
                check = sum([a*f >= amount for a, f in zip(stake, self.odds)]) == len(self.odds)
                return stake*check


class Matches:

    def __init__(self):
        self.matches = {}
        self.sure_bets = {}

    def __str__(self):
        if not self.matches:
            return ""
        return "\n".join([m + "\n" + str(o) for m, o in self.matches.items()])

    def __repr__(self):
        return self.__str__()

    def __contains__(self, key):
        return key in self.matches

    def append(self, match, odds):
        if match not in self.matches:
            self.matches[match] = odds
        else:
            self.matches[match].update(odds)

    def get_surebets(self):
        for key in self.matches:
            odds = self.matches[key]
            sb = odds.sure_bet5()
            if sb:
                self.sure_bets[key] = [sb, odds]


    def print_surebets(self):
        if self.sure_bets:
            print("\n".join([m + "\n" + "Bet {} {}\n".format(*o[0]) + str(o[1]) for m, o in self.sure_bets.items()]))
        else:
            print("No sure bets found")



