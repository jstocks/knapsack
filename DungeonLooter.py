import random
import numpy as np


class Adventurer:
    """
    The adventurer has a finite carry capacity.  They cannot carry more than their
    carry_weight.  They also contain a coin_purse to keep all of their different
    coins that sum up to a total value.
    """

    def __init__(self, carry_weight):
        self.carry_weight = carry_weight  # backpack capacity
        self.coin_purse = {}
        self.inventory = []
        self.backpack_weight = 0
        self.carry_value = 0

    def bkpk_weight(self):  # update the backpack weight
        tot_weight = 0
        for w in self.inventory:
            tot_weight += w.weight
        self.backpack_weight = tot_weight

    def car_value(self):  # update the carry value
        car_value = 0
        for i in self.inventory:
            car_value += i.value
        self.carry_value = car_value

    def purse_val(self):  # update the purse value
        purse_val = sum(k*v for k, v in self.coin_purse.items())
        return purse_val

    def show_inventory(self):
        """
        Shows Inventory
        :return: A String representation of the players inventory.
        """

        """
        === SAMPLE SHOW INVENTORY ===
        Adventurer (Total Carry Capacity: 100)
        Total Carry Weight: 70
        Total Carry Value: 537
        Total Coin Purse Value: 89

        == COINS ==
        bronze (1): 0
        copper (2): 0
        nickel (5): 1
        silver (13): 0
        gold (20): 1
        diamond (32): 2
        lunastone (100): 0

        == INVENTORY ==
        dagger: Wgt=4, V=90
        armor: Wgt=52, V=118
        herbs: Wgt=1, V=19
        herbs: Wgt=2, V=17
        clothing: Wgt=5, V=43
        dagger: Wgt=4, V=60
        jewels: Wgt=2, V=190
        """

        print("Adventurer (Total Carry Capacity: " + str(self.carry_weight) + ")\n" +
              "Total Carry Weight: " + str(self.backpack_weight) +"\n" +
              "Total Carry Value: " + str(self.carry_value) + "\n" +
              "Total Coin Purse Value: " + str(self.purse_val()) + "\n\n" +
              "== COINS ==")
        for key in Game.COINS:
            if key in self.coin_purse:
                print(Game.COINS[key] + ": " + "(" + str(key) + "): " + str(self.coin_purse[key]))
            else:
                print(Game.COINS[key] + ": " + "(" + str(key) + "): " + "0")
        print("\r")

        print("== INVENTORY ==")
        if not self.inventory:
            print("   --EMPTY-- \n")
        else:
            for i in self.inventory:
                print(i)
            print("\r")


class Chest:
    """
    A chest is a container of Items that can be randomly populated.
    """

    def __init__(self, n=10):
        self.contents = []
        self.total_value = 0
        for i in range(n):
            self.contents.append(Item.generate_random_item())
        self.tot_value()

    def tot_value(self):
        tot_val = 0
        for i in self.contents:
            tot_val += i.value
        self.total_value = tot_val

    def __str__(self):
        ret_str = ""
        x = 1
        tot_wgt = 0
        # tot_val = 0
        for i in self.contents:
            ret_str += f'{x}: {i} \n'
            tot_wgt += i.weight
            # tot_val += i.value
            x += 1
        return f"Chest: Item Count={x - 1}, Total Value={self.total_value}, " \
               f"Total Weight={tot_wgt}\n{ret_str}"

    def __repr__(self):
        ret_str = ""
        x = 1
        tot_wgt = 0
        tot_val = 0
        for i in self.contents:
            ret_str += f'{x}: {i} \n'
            tot_wgt += i.weight
            tot_val += i.value
            x += 1
        return f"Chest: Item Count={x -1}, Total Value={tot_val}, " \
               f"Total Weight={tot_wgt}\n{ret_str}"

    def remove(self, item):
        """
        Removes the provided item from the chest.
        :param item: The item object that should be remove from the list.
        :return: True if item was found/removed, False otherwise
        """
        try:
            self.contents.remove(item)
            return True
        except ValueError as e:
            return False

class Item:
    """
    An Item can be of multiple types and those types have a min and max value and weight.
    When an item of a specific type is generated, it should contain a value that
    is within that range.  To add different types to the game, simply add them to the
    static field Item.TYPES as shown.  This is used by the generator to create a random item.
    """
    TYPES = {
        'dagger':
            {
                'weight': (1, 5),
                'value': (10, 100)
            },
        'jewels':
            {
                'weight': (1, 5),
                'value': (50, 500)
            },
        'clothing':
            {
                'weight': (5, 10),
                'value': (1, 50)
            },
        'herbs':
            {
                'weight': (1, 2),
                'value': (3, 20)
            },
        'gems':
            {
                'weight': (1, 5),
                'value': (25, 250)
            },
        'armor':
            {
                'weight': (25, 75),
                'value': (50, 1000)
            }
    }

    def __init__(self, name, weight, value):
        """
        Creates an item with the provided type (name), weight and value.
        :param name: The name of the item.  Usually just the 'type' of item it is.
        :param weight: The weight of the item.  (numeric)
        :param value: The value of the item (int).
        """
        self.name = name
        self.weight = weight
        self.value = value

    def __str__(self):
        return f"{self.name}: Wgt={self.weight}, V={self.value}"

    @staticmethod
    def generate_random_item(of_type=None):
        """
        Will generate a random item of any type or of a specific type when provided.
        :param of_type: The TYPE of item to generate.  If omitted, the method will
        generate an item of random Type.
        :return: An instantiated Item.
        """
        if of_type is None:
            of_type = random.choice(list(Item.TYPES))

        w_min, w_max = Item.TYPES[of_type]['weight']
        v_min, v_max = Item.TYPES[of_type]['value']
        w = random.randint(w_min, w_max)
        v = random.randint(v_min, v_max)
        return Item(of_type, w, v)


class Game:
    """
    The controlller for the game controlling the different Coin Denominations and
    maintaining the states of chests and acting as the "shop" that can also sell
    the items for the Adventurer.
    """
    COINS = {
        1: 'bronze',
        2: 'copper',
        5: 'nickel',
        13: 'silver',
        20: 'gold',
        32: 'diamond',
        100: 'lunastone'
    }

    def __init__(self, player):
        self.player = player
        self.chests = []

    def show_player_inventory(self):
        return player.show_inventory()

    def add_chest(self, chest):
        """
        Adds a chest to the game.
        :param chest: The Chest to add to the game.
        :return: None
        """
        self.chests.append(chest)

    def show_chests(self):
        """
        Prints a list of the chest contents to the screen.
        :return: None
        """

        """
        === SAMPLE SHOW CHESTS === 
        Chest 0:
        = CONTENTS =
        dagger: Wgt=4, V=90
        armor: Wgt=52, V=118
        herbs: Wgt=1, V=19
        herbs: Wgt=2, V=17
        clothing: Wgt=5, V=43
        dagger: Wgt=4, V=60
        jewels: Wgt=2, V=190

        Chest 1:
        = CONTENTS = 
        clothing: Wgt=5, V=43
        dagger: Wgt=4, V=60
        """
        x = 0
        for i in self.chests:
            print("Chest " + str(x) + ":\n= CONTENTS =\n" + str(i))
            x += 1

    def loot_chests(self):
        """
        For each chest in the game, determine the optimal content to remove [0-1]
        knapsack and add the item to the adventurers inventory. Chests may still
        have contents remaining after looting.

        Note after looting each chest, the remaining carry weight of the adventurer
        will be reduced.  The adventurer does NOT have to select the optional ORDER
        of looting chests if there are more than one.  For example if the first chest
        contains 100 lbs of clothes and the second contains 100 lbs of jewels, if
        the adventurer loots the clothing chest first, then the opportunity to loot
        the jewels will be missed.

        :return: None
        """
        # OPTIONAL sort chests based on chest value, highest to lowest; loot highest value first!!!
        # self.chests.sort(key=lambda chest: chest.total_value, reverse=True)

        # iterate through chest[s] until no more player capacity
        for c in range(len(self.chests)):
            capacity = self.player.carry_weight - self.player.backpack_weight
            if capacity <= 0:  # cannot carry anymore
                return

            # assign weights and values to arrays
            weights = [w.weight for w in self.chests[c].contents]
            values = [v.value for v in self.chests[c].contents]

            # ignore the current chest if it is empty
            if len(weights) == 0:
                continue  # now check the next chest

            # create row, column array of zeroes
            solution = np.zeros((len(weights), capacity + 1))
            # initialize the first item; add value if item weight is >= than capacity
            for j in range(capacity + 1):
                solution[0, j] = values[0] if j >= weights[0] else 0

            # iterate over each item (rows)
            for i in range(1, len(weights)):
                for j in range(capacity + 1):
                    if j - weights[i] >= 0:  # IF THIS ITEM CAN FIT
                        # go up one row, left value of item to determine value with item
                        with_item = solution[i - 1, j - weights[i]] + values[i]
                    else:
                        # if it can't fit, determine value of -1
                        with_item = -1

                    # compare up one row, current value
                    without_item = solution[i - 1, j]
                    # optimal value placed in cell
                    solution[i, j] = max(without_item, with_item)

            # [solution] returns array of optimal knapsack

            rows, cols = solution.shape

            # start at bottom right cell
            curr_row = rows - 1
            curr_col = cols - 1

            loot_items = []
            # append value in last cell
            curr_val = solution[curr_row, curr_col]
            while curr_val > 0:
                # compare value in cell above current; if it's the same, just go up and try again
                if curr_row == 0:
                    loot_items.append(curr_row)
                    break
                elif curr_val != solution[curr_row - 1, curr_col]:
                    loot_items.append(curr_row)
                    curr_val = curr_val - values[curr_row]
                    curr_col = curr_col - weights[curr_row]
                    curr_row -= 1
                else:
                    curr_row -= 1

            # add item to player inventory and remove from chest
            for x in loot_items:
                self.player.inventory.append(self.chests[c].contents[x])
                self.chests[c].contents.pop(x)

            # update chest value & player's backpack weight and carry value
            self.chests[c].tot_value()
            self.player.bkpk_weight()
            self.player.car_value()

    def sell_items(self):
        """
        Sell items will take the entirety of the adventurers inventory, calculate its total
        value and "sell it." This will remove it all items from inventory and in return "payment"
        matching that total value will be added to the adventurer's coin_purse, consisting of the
        optimal set of denominations.  For example, if the total inventory is valued at 124, the
        coin_purse will have the following denominations added:
            1 Diamond (100 value)
            1 Gold (20 value)
            2 Nickel (2x2 = 4 value)

        :return: None
        """

        target = self.player.carry_value
        denominations = Game.COINS

        data = [[]] * (target + 1)
        for i in range(1, target + 1):
            curr_min = None
            for denom in denominations:
                back_val = i - denom
                if back_val >= 0:  # able to subtract the current denom from curr value
                    if data[back_val] is None:  # base case for 0
                        continue  # previous calculation is invalid & can't be used
                    curr = data[back_val].copy()
                    curr.append(denom)
                    if curr_min is None or len(curr) < len(curr_min):
                        curr_min = curr
            data[i] = curr_min
        change = data[target]
        # create dictionary of change made
        change_dict = {}
        for c in range(len(change)):
            change_dict[change[c]] = change.count(change[c])
        # add change to player's coin purse
        for key in change_dict:
            if key in self.player.coin_purse:
                self.player.coin_purse[key] = self.player.coin_purse[key] + change_dict[key]
            else:
                self.player.coin_purse[key] = change_dict[key]

        # clear player inventory
        self.player.inventory.clear()
        self.player.backpack_weight = 0
        self.player.carry_value = 0


if __name__ == "__main__":
    # CREATE A PLAYER WITH FINITE CARRY CAPACITY
    player = Adventurer(carry_weight=100)
    game = Game(player)

    # INDICATE THERE IS NO INVENTORY AND NO MONEY
    game.show_player_inventory()

    # CREATE CHESTS WITH RANDOM CONTENT AND ADD IT TO THE GAME
    game.add_chest(Chest())

    # SHOW THE CONTENT OF ANY CHESTS IN THE GAME
    game.show_chests()

    # THE GAME SHOULD HAVE A METHOD THAT WILL OPTIMALLY LOOT THE ITEMS
    # IN THE CHEST [0-1 KNAPSACK] AND ADD IT TO THE PLAYER'S INVENTORY
    # ANY ITEMS NOT IN THE CHEST SHOULD REMAIN
    game.loot_chests()

    game.show_chests()
    game.show_player_inventory()

    # THE GAME SHOULD HAVE A METHOD TO TAKE INVENTORY FROM THE PLAYER
    # CONVERT IT INTO PROPER DENOMINATIONS, AND PLACE THAT DATA INTO THE COIN PURSE
    game.sell_items()

    game.show_player_inventory()
