import heapq
from typing import Dict, List, Optional, Tuple

import streamlit as st

State = Tuple[int, ...]  # ví dụ (2,8,3,1,6,4,7,0,5)


def parse_grid(text: str) -> State:
    """
    Parse text dạng:
        2 8 3
        1 6 4
        7 0 5
    thành tuple 9 phần tử.
    """
    nums: List[int] = []
    for line in text.strip().splitlines():
        for token in line.strip().split():
            if token:
                nums.append(int(token))

    if len(nums) != 9:
        raise ValueError("Cần đúng 9 số (3 dòng, mỗi dòng 3 số).")
    if sorted(nums) != list(range(9)):
        raise ValueError("Các số phải từ 0 đến 8, không trùng lặp.")
    return tuple(nums)


def is_solvable(state: State) -> bool:
    """
    Kiểm tra tính giải được của 3x3 8-puzzle.
    Đếm số inversion, nếu chẵn thì giải được.
    """
    arr = [x for x in state if x != 0]
    inv = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inv += 1

    return inv % 2 == 0


def manhattan_distance(state: State, goal: State) -> int:
    """
    Heuristic Manhattan distance.
    """
    pos_goal: Dict[int, Tuple[int, int]] = {}
    for idx, val in enumerate(goal):
        pos_goal[val] = (idx // 3, idx % 3)

    distance = 0
    for idx, val in enumerate(state):
        if val == 0:
            continue
        x, y = idx // 3, idx % 3
        goal_x, goal_y = pos_goal[val]
        distance += abs(x - goal_x) + abs(y - goal_y)
    return distance


def misplaced_titles(state: State, goal: State) -> int:
    """
    Heuristic: số ô sai vị trí (trừ ô 0).
    """
    return sum(1 for i in range(9) if state[i] != 0 and state[i] != goal[i])


def get_neighbors(state: State) -> List[State]:
    """
    Trả về các state có thể đi từ state hiện tại (move ô 0).
    """
    neighbors: List[State] = []
    zero_idx = state.index(0)
    x, y = zero_idx // 3, zero_idx % 3
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_idx = nx * 3 + ny
            new_state = list(state)
            new_state[zero_idx], new_state[new_idx] = (
                new_state[new_idx],
                new_state[zero_idx],
            )
            neighbors.append(tuple(new_state))

    return neighbors


def reconstruct_path(
    came_from: Dict[State, Optional[State]], current: State
) -> List[State]:
    """
    Tạo lại đường đi từ trạng thái bắt đầu đến trạng thái hiện tại.
    """
    path = [current]
    while current in came_from and came_from[current] is not None:
        prev = came_from[current]
        assert prev is not None
        current = prev
        path.append(current)
    path.reverse()
    return path


def astar(
    start: State, goal: State, heuristic_name: str = "manhattan"
) -> Optional[Tuple[List[State], int, bool]]:
    """
    Thực hiện tìm kiếm A* cho bài toán 8-puzzle.

    Args:
      start: Trạng thái xuất phát (tuple 9 phần tử).
      goal: Trạng thái đích.
      heuristic_name: 'manhattan' hoặc 'misplaced'.

    Heuristic:
      manhattan: Tổng khoảng cách Manhattan của các ô (bỏ qua 0).
      misplaced: Số ô sai vị trí (bỏ qua 0).

    Returns:
      Tuple gồm:
        - Danh sách các trạng thái từ start đến goal (nếu tìm thấy).
        - Số nút đã mở rộng.
        - True nếu tìm thấy lời giải, False nếu không tìm thấy.
      Hoặc None nếu heuristic_name không hợp lệ.
    """
    if heuristic_name == "manhattan":
        heuristic = manhattan_distance
    elif heuristic_name == "misplaced_tiles" or heuristic_name == "misplaced":
        heuristic = misplaced_titles
    else:
        # Fallback to manhattan if unknown
        heuristic = manhattan_distance

    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))

    came_from: Dict[State, Optional[State]] = {start: None}
    g_score: Dict[State, int] = {start: 0}

    closed_set = set()
    expanded_nodes = 0

    while open_set:
        _, _, current = heapq.heappop(open_set)

        if current in closed_set:
            continue

        closed_set.add(current)
        expanded_nodes += 1

        if current == goal:
            path = reconstruct_path(came_from, current)
            return path, expanded_nodes, True

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1

            if neighbor in closed_set and tentative_g_score >= g_score.get(
                neighbor, float("inf")
            ):
                continue

            if tentative_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, tentative_g_score, neighbor))

    return [], expanded_nodes, False


st.set_page_config(page_title="8-Puzzle Solver", layout="centered")
st.title("8-Puzzle Solver with A* Algorithm")
st.markdown(
    """
  Nhập trạng thái **bắt đầu** và **mục tiêu** dưới dạng 3 dòng, mỗi dòng 3 số từ 0 đến 8 (0 là ô trống). \n
  Chọn heuristic ("Manhattan" hoặc "Misplaced") và nhấn "Solve" để tìm lời giải.
  
  **Lưu ý:** Bài toán chỉ giải được nếu số inversion chẵn.
  """
)

col1, col2 = st.columns(2)

with col1:
    start_text = st.text_area(
        "Start State:",
        value="2 8 3\n1 6 4\n7 0 5",
        height=150,
    )

with col2:
    goal_text = st.text_area(
        "Goal State:",
        value="1 2 3\n8 0 4\n7 6 5",
        height=150,
    )

heuristic_choice = st.selectbox(
    "Heuristic:",
    ["manhattan", "misplaced_tiles"],
    format_func=lambda x: "Manhattan" if x == "manhattan" else "Misplaced Tiles",
)

run_button = st.button("Run A*")


def show_state(state: State, title: str = ""):
    if title:
        st.subheader(title)
    grid = [[state[r * 3 + c] for c in range(3)] for r in range(3)]
    # convert 0 thành khoảng trống cho dễ nhìn
    display_grid = [[str(num) if num != 0 else " " for num in row] for row in grid]
    st.table(display_grid)


if "result_path" not in st.session_state:
    st.session_state.result_path = None
    st.session_state.expanded_nodes = 0
    st.session_state.heuristic = heuristic_choice

if run_button or st.session_state.result_path is not None:
    try:
        start_state = parse_grid(start_text)
        goal_state = parse_grid(goal_text)

        # Kiểm tra cả hai state phải cùng parity (cùng chẵn hoặc cùng lẻ)
        start_solvable = is_solvable(start_state)
        goal_solvable = is_solvable(goal_state)

        if start_solvable != goal_solvable:
            st.error(
                "Hai trạng thái **không cùng parity** nên không thể chuyển đổi được cho nhau!"
            )
        else:
            with st.spinner("Đang tìm lời giải..."):
                result = astar(
                    start_state,
                    goal_state,
                    heuristic_name=heuristic_choice,
                )
                if result is None:
                    st.error("Heuristic không hợp lệ.")
                else:
                    path, expanded_nodes, found = result

                if not found:
                    st.error("Không tìm thấy lời giải.")
                else:
                    st.success("Tìm thấy lời giải!")
                    st.session_state.result_path = path
                    st.session_state.expanded_nodes = expanded_nodes
                    st.session_state.heuristic = heuristic_choice

    except Exception as e:
        st.error(f"Lỗi input: {e}")

if st.session_state.result_path:
    path: List[State] = st.session_state.result_path
    expanded_nodes: int = st.session_state.expanded_nodes

    st.markdown("---")
    st.subheader("Kết quả:")

    st.write(f"- Số bước di chuyển: **{len(path) - 1}**")
    st.write(f"- Số node đã mở rộng: **{expanded_nodes}**")
    st.write(f"- Heuristic sử dụng: **{st.session_state.heuristic.title()}**")

    st.markdown("### Điều khiển các bước:")

    col_prev, col_next, col_reset = st.columns([1, 1, 1])

    if "current_step" not in st.session_state:
        st.session_state.current_step = 0

    with col_prev:
        if st.button("⬅️ Bước trước", use_container_width=True):
            if st.session_state.current_step > 0:
                st.session_state.current_step -= 1

    with col_next:
        if st.button("Bước tiếp ➡️", use_container_width=True):
            if st.session_state.current_step < len(path) - 1:
                st.session_state.current_step += 1

    with col_reset:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.current_step = 0

    step = st.session_state.current_step
    st.write(f"**Bước hiện tại: {step} / {len(path) - 1}**")

    show_state(path[0], title="Start state")
    show_state(path[-1], title="Goal state")
    show_state(path[step], title=f"Bước {step} / {len(path) - 1}")

    if step > 0:
        st.markdown(f"### Chuỗi các trạng thái từ bước 0 đến bước {step}")
        for i in range(step + 1):
            st.write(f"**Bước {i}:**")
            show_state(path[i])
