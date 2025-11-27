# 8-Puzzle Solver với Thuật toán A*

Ứng dụng web giải bài toán 8-puzzle sử dụng thuật toán tìm kiếm A* với hai heuristic khác nhau.

## Mô tả bài toán

8-puzzle là một trò chơi trượt số gồm 8 ô đánh số từ 1-8 và 1 ô trống (ký hiệu là 0) trên lưới 3×3. Mục tiêu là di chuyển các ô để đạt được trạng thái đích từ trạng thái ban đầu.

**Ví dụ:**

```
Trạng thái bắt đầu:       Trạng thái đích:
2 8 3                     1 2 3
1 6 4          →          8 0 4
7 0 5                     7 6 5
```

## Tính chất giải được

Không phải mọi cấu hình 8-puzzle đều có lời giải. Một trạng thái chỉ giải được nếu:
- **Hai trạng thái (start và goal) phải cùng parity**
- Parity được xác định bởi số **inversions** (số cặp số nghịch thế khi bỏ qua ô 0)
- Nếu cả hai state có số inversions cùng chẵn hoặc cùng lẻ → giải được ✅
- Nếu một state có inversions chẵn, state kia lẻ → không giải được ❌

## Thuật toán A*

A* là thuật toán tìm kiếm có thông tin, sử dụng hàm đánh giá:

```
f(n) = g(n) + h(n)
```

Trong đó:
- `g(n)`: chi phí thực tế từ trạng thái ban đầu đến trạng thái n
- `h(n)`: ước lượng chi phí từ trạng thái n đến trạng thái đích (heuristic)

### Heuristic được hỗ trợ

1. **Manhattan Distance**: Tổng khoảng cách Manhattan của tất cả các ô so với vị trí đích
   - Tính bằng: `|x1 - x2| + |y1 - y2|` cho mỗi ô
   - Heuristic **admissible** (không bao giờ overestimate)
   - Hiệu quả cao, mở rộng ít node hơn

2. **Misplaced Tiles**: Đếm số ô sai vị trí (trừ ô 0)
   - Đơn giản nhưng kém hiệu quả hơn Manhattan
   - Vẫn là heuristic admissible

## Cài đặt và Chạy

### Yêu cầu hệ thống

- Python 3.8 trở lên
- pip (Python package manager)

### Hướng dẫn cài đặt

1. **Clone hoặc tải về repository**
   ```bash
   git clone https://github.com/nphuoctho/8-puzzle-astar
   cd ./8-puzzle-astar
   ```

2. **Cài đặt dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Chạy ứng dụng**
   ```bash
   streamlit run app.py
   ```

4. Ứng dụng sẽ tự động mở tại `http://localhost:8501`

### Troubleshooting

- **Lỗi "streamlit command not found"**:
  - Chạy: `python -m streamlit run app.py`

- **Lỗi "Address already in use"**:
  - Thay đổi port: `streamlit run app.py --server.port 8502`

- **Ứng dụng không tự động mở trình duyệt**:
  - Mở thủ công: `http://localhost:8501`

## Cách sử dụng

1. **Nhập trạng thái bắt đầu**: 3 dòng, mỗi dòng 3 số (0-8)
2. **Nhập trạng thái đích**: 3 dòng, mỗi dòng 3 số (0-8)
3. **Chọn heuristic**: Manhattan hoặc Misplaced Tiles
4. **Nhấn "Run A*"**: Xem kết quả

## Kết quả hiển thị

- ✅ Số bước di chuyển tối ưu
- 📊 Số node đã mở rộng (để so sánh hiệu quả heuristic)
- 🎯 Heuristic đã sử dụng
- 🔄 Slider để xem từng bước di chuyển chi tiết

## Ví dụ test case

### Test case 1: Giải được (cùng parity lẻ)
```
Start:          Goal:
2 8 3           1 2 3
1 6 4           8 0 4
7 0 5           7 6 5

Kết quả: 5 bước
```

### Test case 2: Không giải được (khác parity)
```
Start:          Goal:
1 2 3           8 1 3
4 5 6           0 4 2
7 8 0           7 6 5

Kết quả: Lỗi - không cùng parity
```

## Cấu trúc code

- `parse_grid()`: Parse input text thành tuple
- `is_solvable()`: Kiểm tra tính giải được (đếm inversions)
- `manhattan_distance()`: Tính heuristic Manhattan
- `misplaced_titles()`: Tính heuristic Misplaced Tiles
- `get_neighbors()`: Tạo các trạng thái kế tiếp
- `astar()`: Thuật toán A* chính
- `reconstruct_path()`: Tái tạo đường đi từ start đến goal

## Độ phức tạp

- **Không gian trạng thái**: 9!/2 = 181,440 trạng thái có thể giải được
- **Độ phức tạp thời gian**: O(b^d) với b là branching factor (~2-4), d là độ sâu
- **Manhattan heuristic** giảm đáng kể số node cần mở rộng so với Misplaced Tiles

## Môn học

Bài tập môn Trí Tuệ Nhân Tạo - CITD

## Tham khảo

- [8-Puzzle Problem - Wikipedia](https://en.wikipedia.org/wiki/15_puzzle)
- [A* Search Algorithm](https://en.wikipedia.org/wiki/A*_search_algorithm)
