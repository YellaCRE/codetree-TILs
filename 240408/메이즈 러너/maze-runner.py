dr = [1, -1, 0, 0]
dc = [0, 0, -1, 1]


def is_in_range(row, col):
    return 0 < row <= N and 0 < col <= N


def is_in_square(target_row, target_col, square_row, square_col, length):
    return square_row <= target_row < square_row + length and square_col <= target_col < square_col + length


def calculate_distance(a_row, a_col, b_row, b_col):
    return abs(a_row - b_row) + abs(a_col - b_col)


def player_turn():
    for i in range(1, M + 1):
        if player_list[i]["is_escape"]:
            continue

        move_direction = -1
        min_distance = calculate_distance(player_list[i]["row"], player_list[i]["col"], exit_row, exit_col)
        for d in range(4):
            # 상하좌우로 움직일 수 있으며
            new_row, new_col = player_list[i]["row"] + dr[d], player_list[i]["col"] + dc[d]
            if not is_in_range(new_row, new_col):
                continue
            # 벽이 없는 곳으로 이동할 수 있습니다.
            if maze[new_row][new_col] > 0:
                continue

            # 움직인 칸은 현재 머물러 있던 칸보다 출구까지의 최단 거리가 가까워야 합니다.
            new_distance = calculate_distance(new_row, new_col, exit_row, exit_col)
            # 움직일 수 있는 칸이 2개 이상이라면, 상하로 움직이는 것을 우선시합니다.
            if new_distance < min_distance:
                move_direction = d
                min_distance = new_distance

        # 참가가가 움직일 수 없는 상황이라면, 움직이지 않습니다.
        if move_direction == -1:
            continue
        # 위치 및 점수 갱신
        player_list[i]["row"], player_list[i]["col"] = (
            player_list[i]["row"] + dr[move_direction], player_list[i]["col"] + dc[move_direction])
        player_list[i]["score"] += 1
        # 참가자가 해당 칸에 도달하면, 즉시 탈출합니다.
        if player_list[i]["row"] == exit_row and player_list[i]["col"] == exit_col:
            player_list[i]["is_escape"] = True


def maze_turn():
    # 한 명 이상의 참가자와 출구를 포함한 가장 작은 정사각형을 잡습니다.
    square_row, square_col, square_size = find_square()

    # 선택된 정사각형은 시계방향으로 90도 회전하며, 회전된 벽은 내구도가 1씩 깎입니다.
    rotate_square(square_row, square_col, square_size)

    rotate_traveler_and_exit(square_row, square_col, square_size)


def find_square():
    # 가장 작은 정사각형부터 모든 정사각형을 만들어봅니다.
    for sz in range(2, N + 1):
        # 가장 좌상단 r 좌표가 작은 것부터 하나씩 만들어봅니다.
        for x1 in range(1, N - sz + 2):
            # 가장 좌상단 c 좌표가 작은 것부터 하나씩 만들어봅니다.
            for y1 in range(1, N - sz + 2):
                x2, y2 = x1 + sz - 1, y1 + sz - 1

                # 만약 출구가 해당 정사각형 안에 없다면 스킵합니다.
                if not (x1 <= exit_row <= x2 and y1 <= exit_col <= y2):
                    continue

                # 한 명 이상의 참가자가 해당 정사각형 안에 있는지 판단합니다.
                is_traveler_in = False
                for i in range(1, M + 1):
                    tx, ty = player_list[i]["row"], player_list[i]["col"]
                    if x1 <= tx <= x2 and y1 <= ty <= y2:
                        # 출구에 있는 참가자는 제외합니다.
                        if not (tx == exit_row and ty == exit_col):
                            is_traveler_in = True

                # 만약 한 명 이상의 참가자가 해당 정사각형 안에 있다면
                # sx, sy, square_size 정보를 갱신하고 종료합니다.
                if is_traveler_in:
                    return x1, y1, sz


# 정사각형 내부의 벽을 회전시킵니다.
def rotate_square(square_row, square_col, square_size):
    # 우선 정사각형 안에 있는 벽들을 1 감소시킵니다.
    for r in range(square_row, square_row + square_size):
        for c in range(square_col, square_col + square_size):
            if maze[r][c]:
                maze[r][c] -= 1

    # 정사각형을 시계방향으로 90' 회전합니다.
    for r in range(square_row, square_row + square_size):
        for c in range(square_col, square_col + square_size):
            # Step 1. (sx, sy)를 (0, 0)으로 옮겨주는 변환을 진행합니다.
            o_r, o_c = r - square_row, c - square_col
            # Step 2. 변환된 상태에서는 회전 이후의 좌표가 (x, y) . (y, square_n - x - 1)가 됩니다.
            r_r, r_c = o_c, square_size - o_r - 1
            # Step 3. 다시 (sx, sy)를 더해줍니다.
            next_maze[r_r + square_row][r_c + square_col] = maze[r][c]

    # next_board 값을 현재 board에 옮겨줍니다.
    for r in range(square_row, square_row + square_size):
        for c in range(square_col, square_col + square_size):
            maze[r][c] = next_maze[r][c]


# 모든 참가자들 및 출구를 회전시킵니다.
def rotate_traveler_and_exit(square_row, square_col, square_size):
    global exit_row, exit_col

    # m명의 참가자들을 모두 확인합니다.
    for i in range(1, M + 1):
        player_row, player_col = player_list[i]["row"], player_list[i]["col"]
        # 해당 참가자가 정사각형 안에 포함되어 있을 때에만 회전시킵니다.
        if (square_row <= player_row < square_row + square_size
                and square_col <= player_col < square_col + square_size):
            # Step 1. (sx, sy)를 (0, 0)으로 옮겨주는 변환을 진행합니다.
            ox, oy = player_row - square_row, player_col - square_col
            # Step 2. 변환된 상태에서는 회전 이후의 좌표가 (x, y) . (y, square_n - x - 1)가 됩니다.
            rx, ry = oy, square_size - ox - 1
            # Step 3. 다시 (sx, sy)를 더해줍니다.
            player_list[i]["row"], player_list[i]["col"] = (rx + square_row, ry + square_col)

    # 출구에도 회전을 진행합니다.
    ex, ey = exit_row, exit_col
    if square_row <= ex < square_row + square_size and square_col <= ey < square_col + square_size:
        # Step 1. (sx, sy)를 (0, 0)으로 옮겨주는 변환을 진행합니다.
        ox, oy = ex - square_row, ey - square_col
        # Step 2. 변환된 상태에서는 회전 이후의 좌표가 (x, y) . (y, square_n - x - 1)가 됩니다.
        rx, ry = oy, square_size - ox - 1
        # Step 3. 다시 (sx, sy)를 더해줍니다.
        exit_row, exit_col = rx + square_row, ry + square_col


N, M, K = map(int, input().split())
maze = [[-1 for _ in range(N + 1)]]
for _ in range(N):
    temp = list(map(int, input().split()))
    temp.insert(0, -1)
    maze.append(temp)
# print(maze)
next_maze = [[0] * (N + 1) for _ in range(N + 1)]

player_list = [{}]
for _ in range(M):
    input_row, input_col = map(int, input().split())
    player_list.append({
        "row": input_row,
        "col": input_col,
        "score": 0,
        "is_escape": False
    })
# print(player_list)
exit_row, exit_col = map(int, input().split())
# print(EXIT)

# K초 동안 위의 과정을 계속 반복됩니다.
for _ in range(K):
    player_turn()

    is_all_escaped = True
    for idx in range(1, M + 1):
        if not player_list[idx]["is_escape"]:
            is_all_escaped = False

    # 만약 모든 사람이 출구로 탈출했으면 바로 종료합니다.
    if is_all_escaped:
        break

    maze_turn()

total_moving_distance = 0
for idx in range(1, M + 1):
    total_moving_distance += player_list[idx]["score"]

print(total_moving_distance)
print(exit_row, exit_col)