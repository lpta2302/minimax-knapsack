from enum import Enum
from typing import List
from item import Item

class Problem(Enum):
    OPTIMIZE_VALUE = 'OPTIMIZE_VALUE'
    OPTIMIZE_VALUE_BOTH = 'OPTIMIZE_VALUE_BOTH'

class State:
    def __init__(self, remaining_items: List[Item], selected_items: List[Item], selected_items_opponent: List[Item],
                 accumulate: int, accumulate_opponent: int, capacity: int):
        self.remaining_items = remaining_items  # Danh sách các vật phẩm còn lại chưa chọn
        self.selected_items = selected_items  # Danh sách các vật phẩm đã chọn
        self.selected_items_opponent = selected_items_opponent  # Danh sách vật phẩm của đối thủ
        self.accumulate = accumulate  # Tổng giá trị của các vật phẩm đã chọn
        self.accumulate_opponent = accumulate_opponent  # Tổng giá trị của vật phẩm đối thủ
        self.capacity = capacity  # Dung lượng ba lô còn lại


class KnapsackSolver:
    def __init__(self, items: List[Item], capacity: int, problem=Problem.OPTIMIZE_VALUE) -> None:
        self.items = items
        self.items.sort(key=lambda item: item.weight, reverse=True)
        self.capacity = capacity
        self.problem = problem
        self.max_value: int = 0  # Giá trị tối đa tìm được
        self.selected_items: List[Item] = []  # Danh sách các vật phẩm được chọn
        self.is_enable_minimizer: bool = True  # Cờ để kích hoạt lượt của Minimizer

    def minimax(self, state: State, is_max_turn: bool, alpha: int, beta: int) -> tuple[int, List[Item]]:
        # Điều kiện kết thúc: không còn vật phẩm hoặc dung lượng ba lô đã đầy/hết
        if self.terminal(state):
            return self.evaluate(state)

        if is_max_turn:
            max_value: int = float('-inf')  # Giá trị lớn nhất khởi tạo cho Max
            selected_items: List[Item] = []  # Danh sách tạm thời các vật phẩm được chọn

            for i in range(len(state.remaining_items)):
                # Thử chọn một vật phẩm (chỉ số i)
                if state.remaining_items[i].weight <= state.capacity:
                    new_state = State(
                        remaining_items=state.remaining_items[i + 1:],
                        selected_items=state.selected_items + [state.remaining_items[i]],
                        selected_items_opponent=state.selected_items_opponent,
                        accumulate=state.accumulate + state.remaining_items[i].value,
                        accumulate_opponent=state.accumulate_opponent,
                        capacity=state.capacity - state.remaining_items[i].weight
                    )

                    # Gọi đệ quy cho minimax với alpha-beta pruning
                    result, selected_items_result = self.minimax(new_state, False, alpha, beta)
                    # max_value = max(max_value, result)
                    if(result > max_value):
                        max_value = result
                        selected_items = selected_items_result

                    # Cập nhật max_value và selected_items nếu tìm được giá trị lớn hơn
                    if max_value > self.max_value:
                        self.max_value = max_value
                        self.selected_items = selected_items

                    # Alpha-beta pruning: Cập nhật alpha và kiểm tra điều kiện cắt tỉa
                    alpha = max(alpha, max_value)
                    if beta <= alpha:
                        break  # Cắt tỉa nhánh còn lại nếu không cần thiết phải duyệt tiếp
            return max_value, selected_items
        else:
            min_value: int = float('inf')  # Giá trị nhỏ nhất khởi tạo cho Min
            selected_items:List[Item] = []

            if self.problem == Problem.OPTIMIZE_VALUE:
                if self.is_enable_minimizer:
                    # Tính toán danh sách vật phẩm dự kiến để Minimizer có thể chọn
                    expected_selected_items: List[Item] = state.remaining_items[:]
                    expected_capacity: int = state.capacity
                    i: int = len(expected_selected_items) - 1
                    while  i >= 0 and expected_capacity > 0:
                        if expected_selected_items[i].weight <= expected_capacity:
                            expected_capacity -= expected_selected_items[i].weight
                            expected_selected_items.pop()
                        i -= 1

                    self.is_enable_minimizer = expected_selected_items  # Cập nhật cờ minimizer

            for i in range(len(state.remaining_items)):
                # Nếu có thể, minimizer sẽ chọn một vật phẩm khác
                new_state = State(
                    remaining_items=state.remaining_items[:i] + state.remaining_items[i + 1:] 
                        if self.is_enable_minimizer else state.remaining_items,
                    selected_items=state.selected_items,
                    selected_items_opponent=state.selected_items_opponent + [state.remaining_items[i]],
                    accumulate=state.accumulate,
                    accumulate_opponent=state.accumulate_opponent + state.remaining_items[i].value,
                    capacity=state.capacity
                )

                result, selected_items_result = self.minimax(new_state, True, alpha, beta)
                # min_value = min(min_value, result)  # Cập nhật giá trị nhỏ nhất
                if(result < min_value):
                    min_value = result
                    selected_items = selected_items_result

                # Alpha-beta pruning: Cập nhật beta và kiểm tra điều kiện cắt tỉa
                beta = min(beta, min_value)
                if beta <= alpha:
                    break  # Cắt tỉa nhánh còn lại nếu không cần thiết phải duyệt tiếp
            return min_value, selected_items

    def terminal(self, state: State) -> bool:
        return not state.remaining_items or state.capacity <= 0

    def evaluate(self, state: State) -> tuple[int, List[Item]]:
        if self.problem == Problem.OPTIMIZE_VALUE:
            return state.accumulate, state.selected_items
        elif self.problem == Problem.OPTIMIZE_VALUE_BOTH:
            return state.accumulate - state.accumulate_opponent, state.selected_items
    def solve(self) -> tuple[int, List[Item]]:
        # Hàm bắt đầu giải bài toán
        initial_state = State(
            remaining_items=self.items,
            selected_items=[],
            selected_items_opponent=[],
            accumulate=0,
            accumulate_opponent=0,
            capacity=self.capacity
        )
        
        # Gọi hàm minimax với alpha = -∞ và beta = ∞ để bắt đầu tìm kiếm
        # if self.problem == Problem.OPTIMIZE_VALUE_BOTH:
        #     max_value, selected = self.minimax(initial_state, True, float('-inf'), float('inf'))
        #     return max_value, selected
        
        self.minimax(initial_state, True, float('-inf'), float('inf'))
        return self.max_value, self.selected_items
