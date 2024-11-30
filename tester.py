import time
from typing import List, Dict, Tuple

from item import Item
from knapsack_solver import KnapsackSolver  # Assuming your KnapsackSolver is in this file

class KnapsackTestRunner:
    def __init__(self):
        self.test_cases: List[Dict] = [
            {
                'name': 'Basic Test Case',
                'items': [
                    Item(5, 4),  # Value: 5, Weight: 4
                    Item(4, 3),  # Value: 4, Weight: 3
                    Item(3, 2),  # Value: 3, Weight: 2
                    Item(1, 6)   # Value: 1, Weight: 6
                ],
                'capacity': 8,
                'expected_value': 9,
                'expected_items': [
                    (5, 4),  # Item 1
                    (4, 3)   # Item 2
                ]
            },
            {
                'name': 'No Items Fit',
                'items': [
                    Item(5, 10),  # Value: 5, Weight: 10
                    Item(3, 8),   # Value: 3, Weight: 8
                    Item(2, 7)    # Value: 2, Weight: 7
                ],
                'capacity': 5,
                'expected_value': 0,
                'expected_items': []
            },
            {
                'name': 'Exact Fit',
                'items': [
                    Item(5, 4),  # Value: 5, Weight: 4
                    Item(4, 3),  # Value: 4, Weight: 3
                    Item(3, 2),  # Value: 3, Weight: 2
                    Item(2, 1)   # Value: 2, Weight: 1
                ],
                'capacity': 5,
                'expected_value': 7,
                'expected_items': [
                    (5, 4),  # Item 1
                    (2, 1)   # Item 3
                ]
            },
            {
                'name': 'Multiple Optimal Solutions',
                'items': [
                    Item(6, 4),  # Value: 6, Weight: 4
                    Item(5, 3),  # Value: 5, Weight: 3
                    Item(3, 2),  # Value: 3, Weight: 2
                    Item(4, 5)   # Value: 4, Weight: 5
                ],
                'capacity': 7,
                'expected_value': 11,
                'expected_items': [
                    (6, 4),   # Item 2
                    (5, 3),  # Item 1
                ]
            },
            {
                'name': 'All Items Fit',
                'items': [
                    Item(5, 2),  # Value: 5, Weight: 2
                    Item(4, 3),  # Value: 4, Weight: 3
                    Item(3, 1),  # Value: 3, Weight: 1
                    Item(2, 4),  # Value: 2, Weight: 4
                ],
                'capacity': 10,
                'expected_value': 14,
                'expected_items': [
                    (2, 4),   # Item 4
                    (4, 3),  # Item 2
                    (5, 2),  # Item 1
                    (3, 1),  # Item 3
                ]
            },
            {
                'name': 'Single Item',
                'items': [
                    Item(7, 4),  # Value: 7, Weight: 4
                ],
                'capacity': 5,
                'expected_value': 7,
                'expected_items': [
                    (7, 4)  # Item 1
                ]
            },
            {
                'name': 'k1',
                'items': [
                    Item(18, 8),  # {value, weight}
                    Item(7, 2),   # {value, weight}
                    Item(15, 5),  # {value, weight}
                    Item(5, 2),   # {value, weight}
                    Item(10, 3),  # {value, weight}
                    Item(9, 4),   # {value, weight}
                    Item(8, 4),   # {value, weight}
                    Item(14, 7),  # {value, weight}
                    Item(12, 6),  # {value, weight}
                    Item(6, 3)    # {value, weight}
                ],
                'capacity': 20,
                'expected_value': 55,
                'expected_items': [
                    (18, 8), 
                    (15, 5), 
                    (10, 3), 
                    (7, 2), 
                    (5, 2)
                ]
            }
        ]

    def run_test(self, test_case: Dict) -> None:
        start_time = time.time()
        solver = KnapsackSolver(test_case['items'], test_case['capacity'])
        result_value, selected_items = solver.solve()
        end_time = time.time()  # Kết thúc đếm thời gian

        print(f"Thời gian chạy: {end_time - start_time:.4f} giây")
        # Check if the result value matches the expected value
        assert result_value == test_case['expected_value'], (
            f"Failed: {test_case['name']} - Expected value: {test_case['expected_value']}, "
            f"got: {result_value}"
        )
        
        # Check if the selected items match the expected selected items
        selected_items_values: List[Tuple[int, int]] = [
            (item.value, item.weight) for item in selected_items
        ]
        assert selected_items_values == test_case['expected_items'], (
            f"Failed: {test_case['name']} - Expected items: {test_case['expected_items']}, "
            f"got: {selected_items_values}"
        )
        
        print(f"Passed: {test_case['name']}")

    def run_all_tests(self) -> None:
        for test_case in self.test_cases:
            self.run_test(test_case)


# Example usage:
if __name__ == '__main__':
    test_runner = KnapsackTestRunner()
    test_runner.run_all_tests()
