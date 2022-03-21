
import csv
from itertools import combinations
from typing import List


MAX_COST = 500

CSV_FILE = './data/init.csv'

class Action:
    list_action: List = []

    def __init__(self, name, price, profit) -> None:
        self.price = price
        self.name = name
        self.profit = profit
        self.gain_in_euro = (price*profit)/100
        self.list_action.append(self)

    def __repr__(self) -> str:
        return self.name + " |  prix : " + str(self.price) + " € | profit en euro : " + str(self.gain_in_euro) + "€"


def all_combination(array, number):
    """Run all combinations

    Args:
        array (list): Extract all possible combinations
        number (int): number of element per combination

    Returns:
        list: list of possible combinations
    """
    return list(combinations(array, number))


def read_file(file):
    """Open csv file 

    Args:
        file (string): path to csv file
    """
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            Action(row['name'], float(row['price']), float(row['profit']))


def search_all_combinations(max_cost):
    """Extract all combinaisons under max_price

    Args:
        max_cost (int): combinaison's cost must be lower than max_cost

    Returns:
        list: list of combinaison with max_cost
    """
    all_combination_possible = []
    for l in range(len(Action.list_action)+1):
        combinations = all_combination(Action.list_action, l)
        for combinaison in combinations:
            base_price = 0
            for action in combinaison:
                base_price += action.price
            if base_price <= max_cost:
                all_combination_possible.append(combinaison)
    return all_combination_possible


def search_maximum_profit(all_combination_possible):
    """Extract max profit from possible combinaison

    Args:
        combi_actions_possible (list): list of tuple, each tuple is a possible combinaison of stocks

    Returns:
        tutple: max_benefit => higthest benefit in list, benefit_array => list of all benefit for all combinaisons
    """
    benefit_array = []
    for combinaison in all_combination_possible:
        base_benifit = 0
        for action in combinaison:
            base_benifit += (action.profit * action.price)/100
        benefit_array.append(base_benifit)
    maximum_benefit = max(benefit_array)
    return (maximum_benefit, benefit_array)


def search_profitable_combinaison(all_combination_possible, benefit_array, maximum_benefit):
    """extract the best combinaison with the max benefit

    Args:
        all_combination_possible (list): list of all possible combinaisons
        benefit_array (list): list of benefit per combinaison
        maximum_benefit (float): heightest benefit in benefit_array

    Returns:
        tutple: best_combinaison, price of this best combinaison
    """
    for i in range(len(benefit_array)):
        if benefit_array[i] == maximum_benefit:
            price = 0
            for action in all_combination_possible[i]:
                price += action.price

            return (all_combination_possible[i], price)


def display_result(most_profitable_combinaison, price, max_benefit):
    """Print result : Actions, total cost and total benefit

    Args:
        most_profitable_combinaison (list): list of stocks to buy
        price (float): total cost
        max_benefit (float): total return
    """
    for action in most_profitable_combinaison:
        print(action)
    print("Coût total : ", round(price, 2),"€")
    print("Profit total : ", round(max_benefit, 2),"€")


def main(file):
    """Main function

    Args:
        file (string): Path to csv file
    """

    read_file(file)
    all_combination_possible = search_all_combinations(MAX_COST)
    max_benefit, benefit_array = search_maximum_profit(all_combination_possible)
    most_profitable_combinaison, price = search_profitable_combinaison(all_combination_possible, benefit_array, max_benefit)

    display_result(most_profitable_combinaison, price, max_benefit)



if __name__ == "__main__":
    main(CSV_FILE)