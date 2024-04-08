SPACE = 0
TRAP = 1
WALL = 2
D = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def knight_turn(order_idx, direct):
    if not knight_list[order_idx]["alive"]:
        return

    if not can_move(order_idx, direct):
        return

    for i in moving_knight:
        knight_move(i, direct)


def knight_move(moving_idx, direct):
    knight_board_clear(moving_idx)

    for r in range(knight_list[moving_idx]["row"],
                   knight_list[moving_idx]["row"] + knight_list[moving_idx]["height"]):
        for c in range(knight_list[moving_idx]["col"],
                       knight_list[moving_idx]["col"] + knight_list[moving_idx]["width"]):
            new_row, new_col = r + D[direct][0], c + D[direct][1]
            knight_board[new_row][new_col] = moving_idx

    knight_list[moving_idx]["row"], knight_list[moving_idx]["col"] = (
        knight_list[moving_idx]["row"] + D[direct][0], knight_list[moving_idx]["col"] + D[direct][1])


def can_move(moving_idx, direct):
    # 위쪽
    if direct == 0:
        for c in range(knight_list[moving_idx]["col"], knight_list[moving_idx]["col"] + knight_list[moving_idx]["width"]):
            if board[knight_list[moving_idx]["row"] - 1][c] == WALL:
                return False

            if knight_board[knight_list[moving_idx]["row"] - 1][c] > 0:
                target_idx = knight_board[knight_list[moving_idx]["row"] - 1][c]
                if not can_move(target_idx, direct):
                    return False
    # 오른쪽
    elif direct == 1:
        for r in range(knight_list[moving_idx]["row"], knight_list[moving_idx]["row"] + knight_list[moving_idx]["height"]):
            if board[r][knight_list[moving_idx]["col"] + knight_list[moving_idx]["width"]] == WALL:
                return False

            if knight_board[r][knight_list[moving_idx]["col"] + knight_list[moving_idx]["width"]] > 0:
                target_idx = knight_board[r][knight_list[moving_idx]["col"] + knight_list[moving_idx]["width"]]
                if not can_move(target_idx, direct):
                    return False
    # 아랫쪽
    elif direct == 2:
        for c in range(knight_list[moving_idx]["col"], knight_list[moving_idx]["col"] + knight_list[moving_idx]["width"]):
            if board[knight_list[moving_idx]["row"] + knight_list[moving_idx]["height"]][c] == WALL:
                return False

            if knight_board[knight_list[moving_idx]["row"] + knight_list[moving_idx]["height"]][c] > 0:
                target_idx = knight_board[knight_list[moving_idx]["row"] + knight_list[moving_idx]["height"]][c]
                if not can_move(target_idx, direct):
                    return False
    # 왼쪽
    else:
        for r in range(knight_list[moving_idx]["row"], knight_list[moving_idx]["row"] + knight_list[moving_idx]["height"]):
            if board[r][knight_list[moving_idx]["col"] - 1] == WALL:
                return False

            if knight_board[r][knight_list[moving_idx]["col"] - 1] > 0:
                target_idx = knight_board[r][knight_list[moving_idx]["col"] - 1]
                if not can_move(target_idx, direct):
                    return False

    moving_knight.append(moving_idx)
    return True


def damage_phase(attacker):
    for moving_idx in moving_knight:
        if moving_idx == attacker:
            continue

        for r in range(knight_list[moving_idx]["row"],
                       knight_list[moving_idx]["row"] + knight_list[moving_idx]["height"]):
            for c in range(knight_list[moving_idx]["col"],
                           knight_list[moving_idx]["col"] + knight_list[moving_idx]["width"]):
                if board[r][c] == TRAP:
                    knight_list[moving_idx]["damage"] += 1
                    knight_list[moving_idx]["hp"] -= 1

        if knight_list[moving_idx]["hp"] <= 0:
            knight_list[moving_idx]["alive"] = False
            knight_board_clear(moving_idx)


def knight_board_clear(moving_idx):
    for r in range(knight_list[moving_idx]["row"],
                   knight_list[moving_idx]["row"] + knight_list[moving_idx]["height"]):
        for c in range(knight_list[moving_idx]["col"],
                       knight_list[moving_idx]["col"] + knight_list[moving_idx]["width"]):
            knight_board[r][c] = 0


L, N, Q = map(int, input().split())
# print(L, N, Q)
board = [[WALL for _ in range(L + 2)]]
for _ in range(L):
    temp_list = list(map(int, input().split()))
    temp_list.insert(0, WALL)
    temp_list.append(WALL)
    board.append(temp_list)
board.append([WALL for _ in range(L + 2)])
# print(board)
knight_board = [[0 for _ in range(L + 2)] for _ in range(L + 2)]
knight_list = [{}]
for n in range(1, N + 1):
    R, C, H, W, K = map(int, input().split())
    knight_list.append({
        "number": n,
        "row": R,
        "col": C,
        "height": H,
        "width": W,
        "hp": K,
        "damage": 0,
        "alive": True,
    })
    for row in range(R, R + H):
        for col in range(C, C + W):
            knight_board[row][col] = n
# print(knight_list)
# print(knight_board)
orders = []
for _ in range(Q):
    orders.append(list(map(int, input().split())))
# print(orders)

moving_knight = []
for idx, direction in orders:
    knight_turn(idx, direction)
    damage_phase(idx)
    moving_knight = []

total_damage = 0
for n in range(1, N + 1):
    if knight_list[n]["alive"]:
        total_damage += knight_list[n]["damage"]
print(total_damage)