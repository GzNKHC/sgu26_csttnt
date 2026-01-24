from collections import deque

GOAL = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)

MOVES = [(-1,0),(1,0),(0,-1),(0,1)]

def read_input(filename):
    state = []
    with open(filename, 'r') as f:
        for line in f:
            state.extend(map(int, line.split()))
    return tuple(state)

def get_neighbors(state):
    neighbors = []
    zero = state.index(0)
    r, c = zero // 3, zero % 3

    for dr, dc in MOVES:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nz = nr * 3 + nc
            new_state = list(state)
            new_state[zero], new_state[nz] = new_state[nz], new_state[zero]
            neighbors.append(tuple(new_state))
    return neighbors

def bfs(start):
    queue = deque([(start, [])])
    visited = set()

    while queue:
        state, path = queue.popleft()

        if state == GOAL:
            return path + [state]

        if state in visited:
            continue

        visited.add(state)
        for n in get_neighbors(state):
            if n not in visited:
                queue.append((n, path + [state]))

    return None

def write_output(solution, filename):
    with open(filename, 'w') as f:
        f.write(f"So buoc: {len(solution) - 1}\n\n")
        for s in solution:
            for i in range(0, 9, 3):
                f.write(" ".join(map(str, s[i:i+3])) + "\n")
            f.write("-----\n")

if __name__ == "__main__":
    start = read_input("input.txt")
    solution = bfs(start)

    if solution:
        write_output(solution, "Tuan03/8_Puzzle/output.txt")
        print("Da ghi ket qua vao output.txt")
    else:
        print("Khong tim duoc loi giai")
