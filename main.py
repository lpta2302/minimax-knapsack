from typing import List
from item import Item
from knapsack_gui import KnapsackGUI
from knapsack_solver import KnapsackSolver

gui = KnapsackGUI()
gui.run()


# items = [
#     Item(18, 8),  # {value, weight}
#     Item(7, 2),   # {value, weight}
#     Item(15, 5),  # {value, weight}
#     Item(5, 2),   # {value, weight}
#     Item(10, 3),  # {value, weight}
#     Item(9, 4),   # {value, weight}
#     Item(8, 4),   # {value, weight}
#     Item(14, 7),  # {value, weight}
#     Item(12, 6),  # {value, weight}
#     Item(6, 3)    # {value, weight}
# ]
# print("---------classic----------")
# best, selected_items= KnapsackSolver(items, 10).solve()
# print(best)
# for item in selected_items:
#     print(item)
# print("---------amount---------")

# best, selected_items = KnapsackSolver(items, 10, False).solve()
# print(best)
# for item in selected_items:
#     print(item)
