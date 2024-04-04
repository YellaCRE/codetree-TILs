def move_rudolph(t):
    global Rr, Rc
    graph[Rr][Rc] = 0

    # 가장 가까운 산타를 확인하고 돌진
    [target_row, target_col] = find_santa()

    # 이동
    movRow, movCol = where_to_move_rudolph(Rr, Rc, target_row, target_col)
    Rr, Rc = Rr + movRow, Rc + movCol

    targetNum = graph[target_row][target_col]
    if graph[Rr][Rc] > 0:
        bang("루돌프", targetNum, target_row, target_col, movRow, movCol, t)

    # 이동 완료
    graph[Rr][Rc] = -1


def find_santa():
    nearby_santa = {}
    min_distance = 2 * N
    for num in range(1, P + 1):
        target = santa_list[num]
        if target["탈락"]:
            continue

        distance = cal_distance(Rr, Rc, target["row"], target["col"])
        if not nearby_santa:
            nearby_santa = target
            min_distance = distance
        elif min_distance > distance:
            nearby_santa = target
            min_distance = distance
        elif min_distance == distance and nearby_santa["row"] < target["row"]:
            nearby_santa = target
            min_distance = distance

    return nearby_santa["row"], nearby_santa["col"]


def where_to_move_rudolph(startRow, startCol, endRow, endCol):
    movRow = 0
    if startRow < endRow:
        movRow = 1
    elif startRow > endRow:
        movRow = -1

    movCol = 0
    if startCol < endCol:
        movCol = 1
    elif startCol > endCol:
        movCol = -1

    return movRow, movCol


def cal_distance(ar, ac, br, bc):
    return (ar - br) ** 2 + (ac - bc) ** 2


def move_santa(t):
    for num in range(1, P + 1):
        # 만약 탈락이거나 스턴상태이면 continue
        if santa_list[num]["탈락"] or santa_list[num]["stun"] >= t:
            continue

        moveDir = where_to_move_santa(num)

        # 산타가 움직였을 때 액션
        if moveDir != -1:
            newRow = santa_list[num]["row"] + dr[moveDir]
            newCol = santa_list[num]["col"] + dc[moveDir]

            if graph[newRow][newCol] == -1 and D > 1:
                # 루돌프와 충돌했을 때 충돌 액션
                bang("산타", num, newRow, newCol, -dr[moveDir], -dc[moveDir], t)
            elif graph[newRow][newCol] == -1 and D == 1:
                # 충돌 거리가 1일 경우 제자리
                santa_list[num]["score"] += D
            else:
                # 충돌하지 않았을 경우
                graph[santa_list[num]["row"]][santa_list[num]["col"]] = 0
                santa_list[num]["row"], santa_list[num]["col"] = newRow, newCol
                graph[newRow][newCol] = num


def where_to_move_santa(num):
    global Rr, Rc

    min_distance = cal_distance(santa_list[num]["row"], santa_list[num]["col"], Rr, Rc)
    moveDir = -1

    # 움직일 수 있는 방향 확인
    for i in range(4):
        newRow = santa_list[num]["row"] + dr[i]
        newCol = santa_list[num]["col"] + dc[i]

        if not is_inRange(newRow, newCol) or graph[newRow][newCol] > 0:
            continue

        new_distance = cal_distance(newRow, newCol, Rr, Rc)
        if new_distance < min_distance:
            min_distance = new_distance
            moveDir = i

    return moveDir


def bang(who, targetNum, targetRow, targetCol, movRow, movCol, turn):
    # 루돌프의 충돌일 경우
    if who == "루돌프":
        # 루돌프의 충돌 방향으로 이동
        firstRow, firstCol = targetRow + movRow * C, targetCol + movCol * C
    else:
        firstRow, firstCol = targetRow + movRow * D, targetCol + movCol * D

    lastRow, lastCol = firstRow, firstCol

    # 해당 산타 스턴
    santa_list[targetNum]["stun"] = turn + 1

    # 만약 산타가 그 위치에 있다면 한칸 더 이동
    while is_inRange(lastRow, lastCol) and graph[firstRow][firstCol] > 0:
        lastRow += movRow
        lastCol += movCol

    # 충돌한 산타들을 이동
    while not (lastRow == firstRow and lastCol == firstCol):
        # 원래 있던 위치를 구함
        beforeRow = lastRow - movRow
        beforeCol = lastCol - movCol

        # 원래 장외였으면 종료
        if not is_inRange(beforeRow, beforeCol):
            break

        num = graph[beforeRow][beforeCol]
        # 장외가 된 거면 탈락
        if not is_inRange(lastRow, lastCol):
            santa_list[num]["탈락"] = True
        else:
            graph[lastRow][lastCol] = graph[beforeRow][beforeCol]
            santa_list[num]["row"], santa_list[num]["col"] = lastRow, lastCol

        lastRow, lastCol = beforeRow, beforeCol

    # 포인트 갱신
    if who == "루돌프":
        santa_list[targetNum]["score"] += C
    else:
        santa_list[targetNum]["score"] += D

    # 위치 갱신
    graph[santa_list[targetNum]["row"]][santa_list[targetNum]["col"]] = 0
    santa_list[targetNum]["row"], santa_list[targetNum]["col"] = firstRow, firstCol
    if is_inRange(firstRow, firstCol):
        graph[firstRow][firstCol] = targetNum
    else:
        santa_list[targetNum]["탈락"] = True


def is_inRange(x, y):
    return 0 < x <= N and 0 < y <= N


def live_santa():
    for num in range(1, P+1):
        if santa_list[num]["탈락"]:
            continue
        else:
            santa_list[num]["score"] += 1


N, M, P, C, D = map(int, input().split())
graph = [[0 for _ in range(N + 1)] for _ in range(N + 1)]

dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

# 루돌프의 위치
Rr, Rc = map(int, input().split())
graph[Rr][Rc] = -1

# 산타의 위치
santa_list = [{}]
for _ in range(P):
    # 산타 번호, row, col, 점수, 탈락 여부(True면 탈락)
    santa_num, santa_row, santa_col = map(int, input().split())
    graph[santa_row][santa_col] = santa_num
    santa_list.append({
        "num": santa_num,
        "row": santa_row,
        "col": santa_col,
        "score": 0,
        "stun": 0,
        "탈락": False,
    })

for turn in range(1, M+1):
    # 루돌프의 움직임
    move_rudolph(turn)
    # 산타의 움직임
    move_santa(turn)
    # 생존한 산타 점수 갱신
    live_santa()

answer = []
for num in range(1, P+1):
    answer.append(santa_list[num]["score"])
print(*answer)