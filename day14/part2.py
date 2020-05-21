from collections import deque

import fileinput
import math

class Ratio:
    def __init__(self, r, p):
        self.reactant = int(r)
        self.product = int(p)
    def reactant_for_product(self, product_quantity):
        # reactant => product              | reactant => product
        #   8 ORE  =>   3 B                |   7 ORE  =>   5 C
        # to produce 23 B, requires 64 ORE | to produce 37 C, requires 56 ORE
        #        with 1 B leftover         |        with 3 C leftover
        reactant_quantity = int(math.ceil(float(product_quantity) / self.product) * self.reactant)
        leftover = (reactant_quantity / self.reactant) * self.product - product_quantity
        return reactant_quantity, leftover

class Flask:
    def __init__(self):
        self.reactions = dict()

    def load(self, fh):
        for line in fh:
            reactants, product = line.split('=>')
            product_quantity, product = product.split()

            if product in self.reactions:
                raise RuntimeError

            self.reactions[product] = []
            for reactant in reactants.split(','):
                reactant_quantity, reactant = reactant.split()
                self.reactions[product].append((reactant, Ratio(reactant_quantity, product_quantity)))

    def synthesize(self, goal, base):
        priority = 0
        priorities = {goal: priority}
        products = deque([goal])
        while len(products) > 0:
            product = products.pop()
            for reactant, _ in self.reactions[product]:
                if reactant != base:
                    products.appendleft(reactant)
                priority += 1
                priorities[reactant] = priority

        base_amount = 0
        ingredients = {goal: 1}
        while len(ingredients) > 0:
            products = ingredients.keys()
            product = min(products, key=lambda p: priorities[p])
            product_amout = ingredients[product]
            del ingredients[product]
            for reactant, ratio in self.reactions[product]:
                reactant_amount, _ = ratio.reactant_for_product(product_amout)
                if reactant == base:
                    base_amount += reactant_amount
                elif reactant in ingredients:
                    ingredients[reactant] += reactant_amount
                else:
                    ingredients[reactant] = reactant_amount
        return base_amount
if __name__ == "__main__":
    flask = Flask()
    flask.load(fileinput.input())
    required = flask.synthesize('FUEL', 'ORE')
    print required