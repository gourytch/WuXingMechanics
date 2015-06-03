#! /usr/bin/env python3
import random

WATER='WATER'
WOOD='WOOD'
FIRE='FIRE'
EARTH='EARTH'
METAL='METAL'

xings = (WATER, WOOD, FIRE, EARTH, METAL)

generation = {
    WATER: WOOD,
    WOOD: FIRE,
    FIRE: EARTH,
    EARTH: METAL,
    METAL: WATER
}

suppression = {
    WATER: FIRE,
    FIRE: METAL,
    METAL: WOOD,
    WOOD: EARTH,
    EARTH: WATER
}


def action(defense, offense, amount):
    if suppression[offense] == defense:
        return -2 * amount # double impact
    if generation[offense] == defense:
        return amount # healing
    if suppression[defense] == offense:
        return 0 # absorb
    if generation[defense] == offense:
        return -2 * amount # double impact
    return -amount # ordinal damage


class Player(object):
    def __init__(self, name, seed):
        super(Player, self).__init__()
        self.rng = random.Random(seed)
        self.name = name
        self.hp = 100
        self.defense = None
        self.offense = None
        self.amount  = None
        print("player {} with seed {} created.".format(self.name, seed))
        return

    def apply(self, offense, amount):
        delta = action(self.defense, offense, amount)
        if delta > 0:
            print("    player {} healed by {}; hp: {} + {} = {}".format(
                self.name, delta, self.hp, delta, self.hp + delta))
        elif delta == 0:
            print("    player {} absrorbed damage; hp: {}".format(
            self.name, self.hp))
        else:
            print("    player {} {} by {}; hp: {} - {} = {}".format(
                self.name, "DAMAGED" if amount < -delta else "damaged",
                -delta, self.hp, -delta, self.hp + delta))
        self.hp = self.hp + delta
        return

    def choose(self):
        self.defense = self.rng.choice(xings)
        self.offense = self.rng.choice(xings)
        self.amount  = self.rng.randrange(self.hp//2 - 1) if 7 < self.hp else 1
        print("  player {} choosed defense: {}, offense: {} x {}; hp left: {}"
            .format(self.name, self.defense,
                    self.offense, self.amount,
                    self.hp - self.amount))
        return

    def is_alive(self):
        if 0 < self.hp:
            print("  player {} is alive and has {} hp".format(
                self.name, self.hp))
            return True
        print("  player {} is dead".format(self.name))
        return False


class Battle(object):

    def __init__(self, player1, player2):
        super(Battle, self).__init__()
        self.player1 = player1
        self.player2 = player2
        return

    def round(self):
        self.player1.choose()
        self.player2.choose()
        self.player1.hp = self.player1.hp - self.player1.amount
        self.player2.hp = self.player2.hp - self.player2.amount
        self.player1.apply(self.player2.offense, self.player2.amount)
        self.player2.apply(self.player1.offense, self.player1.amount)
        alive1 = self.player1.is_alive()
        alive2 = self.player2.is_alive()
        if not alive1:
            if not alive2:
                print("DRAW")
                return False
            else:
                print("WINNER: {}".format(self.player2.name))
                return False
        elif not alive2:
            print("WINNER: {}".format(self.player1.name))
            return False
        return True

    def game(self):
        print("*** let the battle begin! ***")
        do_next_round = True
        round_no = 0
        while do_next_round:
            round_no = round_no + 1
            print("\nround {} started. total hp={}".format(
                round_no, self.player1.hp + self.player2.hp))
            do_next_round = self.round()
        print("\n*** game finished at round {}. total hp={} ***".format(
            round_no, self.player1.hp + self.player2.hp))
        return


if __name__ == '__main__':
    rng = random.Random()
    rng.seed()
    while True:
        seed1 = rng.randrange(1000)
        seed2 = rng.randrange(1000)
        if seed1 != seed2:
            break
    alice = Player('Alice', seed1)
    bob = Player('Bob', seed2)
    battle = Battle(alice, bob)
    battle.game()
