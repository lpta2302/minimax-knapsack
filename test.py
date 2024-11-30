import time
import random 
from random import randint
from item import Item  # Giả định bạn có file item.py định nghĩa class Item
from knapsack_solver import KnapsackSolver, Problem

def test_complexity(max_items):
    """Kiểm tra độ phức tạp thời gian khi tăng số lượng vật phẩm."""

    results = []
    for i in range(1, 20, 2):  # Tăng số lượng vật phẩm
        capacity = 50 # Điều chỉnh sức chứa túi sao cho phù hợp
        
        # Tạo danh sách vật phẩm ngẫu nhiên
        # items = [Item(random.randint(1, 30), random.randint(10, 30)) for _ in range(max_items)]
        items = [Item(i * j,randint(1,capacity)) for j in range(max_items)]

        # Khởi tạo và giải bài toán
        solver = KnapsackSolver(items, capacity, Problem.OPTIMIZE_VALUE_BOTH)
        start_time = time.time()
        solver.solve()
        end_time = time.time()

        elapsed_time = end_time - start_time
        results.append((i, elapsed_time))
        print(f"Bội số: {i}, Thời gian chạy: {elapsed_time:.6f} giây")

    return results

# Ví dụ sử dụng:
max_items = 10  # Thay đổi giá trị này để kiểm tra với số lượng vật phẩm lớn hơn
# items = [Item(i*randint(1,30), randint(1,30)) for i in range(max_items)]

results = test_complexity(max_items)

# Vẽ biểu đồ (tùy chọn)
import matplotlib.pyplot as plt
i, times = zip(*results)
plt.plot(i, times)
plt.xlabel("Bội số của vật phẩm")
plt.ylabel("Thời gian chạy (giây)")
plt.title("Độ phức tạp thời gian của thuật toán Minimax Knapsack")
plt.show()