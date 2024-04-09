from collections import deque


# 우/하/좌/상의 우선순위대로 먼저 움직인 경로가 선택됩니다.
dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]


def select_attacker(t):
    attacker_damage = 5001
    atk_row, atk_col = -1, -1
    for r in range(1, N+1):
        for c in range(1, M+1):
            # 부서지지 않은 포탑 중 가장 약한 포탑이 공격자로 선정됩니다
            if board[r][c] == 0:
                continue
            # 공격력이 가장 낮은 포탑이 가장 약한 포탑입니다.
            if board[r][c] < attacker_damage:
                attacker_damage = board[r][c]
                atk_row, atk_col = r, c
                continue
            elif board[r][c] > attacker_damage:
                continue
            # 가장 최근에 공격한 포탑이 가장 약한 포탑입니다.
            if attack_history[r][c] > attack_history[atk_row][atk_col]:
                attacker_damage = board[atk_row][atk_col]
                atk_row, atk_col = r, c
                continue
            elif attack_history[r][c] < attack_history[atk_row][atk_col]:
                continue
            # 각 포탑 위치의 행과 열의 합이 가장 큰 포탑이 가장 약한 포탑입니다.
            if r+c > atk_row+atk_col:
                attacker_damage = board[atk_row][atk_col]
                atk_row, atk_col = r, c
                continue
            elif r+c < atk_row+atk_col:
                continue
            # 각 포탑 위치의 열 값이 가장 큰 포탑이 가장 약한 포탑입니다.
            if r > atk_row:
                attacker_damage = board[atk_row][atk_col]
                atk_row, atk_col = r, c

    # 공격자로 선정되면 가장 약한 포탑이므로, 핸디캡이 적용되어 N+M만큼의 공격력이 증가
    board[atk_row][atk_col] += N+M
    attack_history[atk_row][atk_col] = t
    # 공격과 무관하다는 뜻은 공격자도 아니고
    atk = (atk_row, atk_col)
    repair_exception_list.add(atk)
    return atk


def find_target(atk):
    target_damage = -1
    tar_row, tar_col = -1, -1
    for r in range(1, N+1):
        for c in range(1, M+1):
            # 자신을 제외한 포탑
            if r == atk[0] and c == atk[1]:
                continue
            # 공격력이 가장 높은 포탑이 가장 강한 포탑입니다.
            if board[r][c] > target_damage:
                target_damage = board[r][c]
                tar_row, tar_col = r, c
                continue
            elif board[r][c] < target_damage:
                continue
            # 공격한지 가장 오래된 포탑이 가장 강한 포탑입니다.
            if attack_history[r][c] < attack_history[tar_row][tar_col]:
                target_damage = board[r][c]
                tar_row, tar_col = r, c
                continue
            elif attack_history[r][c] > attack_history[tar_row][tar_col]:
                continue
            # 각 포탑 위치의 행과 열의 합이 가장 작은 포탑이 가장 강한 포탑입니다.
            if r+c < tar_row+tar_col:
                target_damage = board[tar_row][tar_col]
                tar_row, tar_col = r, c
                continue
            elif r+c > tar_row+tar_col:
                continue
            # 각 포탑 위치의 열 값이 가장 작은 포탑이 가장 강한 포탑입니다.
            if r < tar_row:
                target_damage = board[tar_row][tar_col]
                tar_row, tar_col = r, c

    # 공격과 무관하다는 뜻은 공격에 피해를 입은 포탑도 아니라는 뜻입니다.
    tar = (tar_row, tar_col)
    repair_exception_list.add(tar)
    return tar


def laser_attack(atk, tar):
    can_attack = False
    q = deque()
    q.append([atk[0], atk[1]])
    visited = [[False for _ in range(M+1)] for _ in range(N+1)]
    back_visited = [[[-1, -1] for _ in range(M+1)] for _ in range(N+1)]

    while q:
        r, c = q.popleft()
        if r == tar[0] and c == tar[1]:
            can_attack = True
            break

        for d in range(4):
            new_row, new_col = (N + r - 1 + dr[d]) % N + 1, (N + c - 1 + dc[d]) % N + 1

            if board[new_row][new_col] == 0:
                continue

            if visited[new_row][new_col]:
                continue

            visited[new_row][new_col] = True
            back_visited[new_row][new_col] = [r, c]
            q.append([new_row, new_col])

    if can_attack:
        damage = board[atk[0]][atk[1]]
        board[tar[0]][tar[1]] = max(0, board[tar[0]][tar[1]] - damage)

        cr, cc = back_visited[tar[0]][tar[1]]
        while not (cr == atk[0] and cc == atk[1]):
            board[cr][cc] = max(0, board[cr][cc] - damage // 2)
            repair_exception_list.add((cr, cc))
            cr, cc = back_visited[cr][cc]

    return can_attack


def cannon_attack(atk, tar):
    damage = board[atk[0]][atk[1]]
    half_damage = damage // 2
    for r in range(-1, 2):
        for c in range(-1, 2):
            new_row, new_col = (N + tar[0] - 1 + r) % N + 1, (N + tar[1] - 1 + c) % N + 1
            if new_row == tar[0] and new_col == tar[1]:
                board[new_row][new_col] = max(0, board[new_row][new_col] - damage)
            else:
                board[new_row][new_col] = max(0, board[new_row][new_col] - half_damage)
                repair_exception_list.add((new_row, new_col))


def repair_phase():
    for r in range(1, N+1):
        for c in range(1, M+1):
            if board[r][c] == 0:
                continue
            if (r, c) in repair_exception_list:
                continue
            board[r][c] += 1


N, M, K = map(int, input().split())
board = [[0 for _ in range(M+1)]]
for _ in range(N):
    temp = list(map(int, input().split()))
    temp.insert(0, 0)
    board.append(temp)
# print(board)

attack_history = [[0 for _ in range(M+1)] for _ in range(N+1)]
for turn in range(1, K+1):
    # 초기화
    repair_exception_list = set()

    attacker = select_attacker(turn)
    target = find_target(attacker)

    if not laser_attack(attacker, target):
        cannon_attack(attacker, target)

    repair_phase()

answer = 0
for row in range(1, N+1):
    for col in range(1, M+1):
        answer = max(answer, board[row][col])

print(answer)