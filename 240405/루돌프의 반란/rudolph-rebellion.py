def is_inRange(row, col):
    return 0 < row <= N and 0 < col <= N


def calculate_distance(start_row, start_col, end_row, end_col):
    return (start_row - end_row) ** 2 + (start_col - end_col) ** 2


def rudolph_turn(t):
    global rudolph_row, rudolph_col
    closest_row, closest_col = find_closest_santa()
    move_row, move_col = find_direction(closest_row, closest_col)

    board[rudolph_row][rudolph_col] = 0
    rudolph_row, rudolph_col = rudolph_row + move_row, rudolph_col + move_col
    if board[rudolph_row][rudolph_col] > 0:
        target_santa_num = board[rudolph_row][rudolph_col]
        # 누가, 언제, 누구를, 어떻게
        bang("rudolph", t, target_santa_num, move_row, move_col, rudolph_row, rudolph_col)

    board[rudolph_row][rudolph_col] = -1


def find_closest_santa():
    min_distance = 2*N
    target_row, target_col = -1, -1
    for n in range(1, P+1):
        if not santa_list[n]["alive"]:
            continue

        distance = calculate_distance(santa_list[n]["row"], santa_list[n]["col"], rudolph_row, rudolph_col)
        if ((distance < min_distance) or (distance == min_distance and target_row < santa_list[n]["row"])
                or (distance == min_distance and target_row == santa_list[n]["row"] and target_col < santa_list[n]["col"])):
            target_row, target_col = santa_list[n]["row"], santa_list[n]["col"]
            min_distance = distance

    return target_row, target_col


def find_direction(target_row, target_col):
    move_row = 0
    if rudolph_row < target_row:
        move_row = 1
    elif rudolph_row > target_row:
        move_row = -1

    move_col = 0
    if rudolph_col < target_col:
        move_col = 1
    elif rudolph_col > target_col:
        move_col = -1

    return move_row, move_col


def santa_turn(t):
    # 산타는 1번부터 P번까지 순서대로 움직입니다.
    for n in range(1, P+1):
        # 기절했거나 이미 게임에서 탈락한 산타는 움직일 수 없습니다.
        if not santa_list[n]["alive"] or santa_list[n]["stun"] >= t:
            continue

        min_distance = calculate_distance(santa_list[n]["row"], santa_list[n]["col"], rudolph_row, rudolph_col)
        move_direction = -1
        for d in range(4):
            # 산타는 루돌프에게 거리가 가장 가까워지는 방향으로 1칸 이동합니다.
            row = santa_list[n]["row"] + dr[d]
            col = santa_list[n]["col"] + dc[d]

            # 산타는 다른 산타가 있는 칸이나 게임판 밖으로는 움직일 수 없습니다.
            if not is_inRange(row, col) or board[row][col] > 0:
                continue

            # 움직일 수 있는 칸이 있더라도 만약 루돌프로부터 가까워질 수 있는 방법이 없다면 산타는 움직이지 않습니다.
            distance = calculate_distance(row, col, rudolph_row, rudolph_col)
            if distance < min_distance:
                move_direction = d
                min_distance = distance

        if move_direction != -1:
            new_row, new_col = santa_list[n]["row"] + dr[move_direction], santa_list[n]["col"] + dc[move_direction]
            if board[new_row][new_col] == -1 and D > 1:
                bang("santa", t, n, -dr[move_direction], -dc[move_direction], new_row, new_col)
            elif board[new_row][new_col] == -1 and D == 1:
                # 기절
                santa_list[n]["stun"] = t + 1
                santa_list[n]["score"] += 1
            else:
                board[santa_list[n]["row"]][santa_list[n]["col"]] = 0
                santa_list[n]["row"], santa_list[n]["col"] = new_row, new_col
                board[new_row][new_col] = n


def bang(who, when, where, row_direction, col_direction, row, col):
    # 기절
    santa_list[where]["stun"] = when + 1

    # 점수 획득 후 밀려남
    if who == "rudolph":
        santa_list[where]["score"] += C
        first_row, first_col = row + C * row_direction, col + C * col_direction
    else:
        santa_list[where]["score"] += D
        first_row, first_col = row + D * row_direction, col + D * col_direction

    last_row, last_col = first_row, first_col

    # 상호작용
    while is_inRange(last_row, last_col) and board[last_row][last_col] > 0:
        last_row += row_direction
        last_col += col_direction

    while not (last_row == first_row and last_col == first_col):
        before_row, before_col = last_row - row_direction, last_col - col_direction
        target_santa = board[before_row][before_col]

        if not is_inRange(last_row, last_col):
            santa_list[target_santa]["alive"] = False
            board[before_row][before_col] = 0
        else:
            board[last_row][last_col], board[before_row][before_col] = board[before_row][before_col], 0

        santa_list[target_santa]["row"], santa_list[target_santa]["col"] = last_row, last_col
        last_row, last_col = before_row, before_col

    board[santa_list[where]["row"]][santa_list[where]["col"]] = 0
    if not is_inRange(last_row, last_col):
        santa_list[where]["alive"] = False
    else:
        board[last_row][last_col] = where
        santa_list[where]["row"], santa_list[where]["col"] = last_row, last_col


def turn_end_process():
    nobody_alive = True
    for n in range(1, P + 1):
        if santa_list[n]["alive"]:
            santa_list[n]["score"] += 1
            nobody_alive = False

    return nobody_alive


dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

N, M, P, C, D = map(int, input().split())
board = [[0 for _ in range(N+1)] for _ in range(N+1)]
rudolph_row, rudolph_col = map(int, input().split())
board[rudolph_row][rudolph_col] = -1

santa_list = [{} for _ in range(P+1)]
for _ in range(P):
    santa_num, santa_row, santa_col = map(int, input().split())
    board[santa_row][santa_col] = santa_num
    santa_list[santa_num] = {
        "number": santa_num,
        "row": santa_row,
        "col": santa_col,
        "stun": 0,
        "alive": True,
        "score": 0
    }

for turn in range(1, M + 1):
    rudolph_turn(turn)
    santa_turn(turn)
    if turn_end_process():
        break

answer = []
for num in range(1, P+1):
    answer.append(santa_list[num]["score"])
print(*answer)