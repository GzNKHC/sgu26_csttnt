from collections import deque

#Đọc file
def read_maze(filename):
    with open(filename, 'r') as f:
        n, m = map(int, f.readline().split())
        maze = []
        start = goal = None

        for i in range(n):
            row = f.readline().split()
            for j in range(m):
                if row[j] == 'S':
                    start = (i, j)
                    row[j] = '0'
                elif row[j] == 'A':
                    goal = (i, j)
                    row[j] = '0'
            maze.append(row)

    return maze, start, goal


#Truy vết
def reconstruct_path(parent, start, goal):
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


#BFS
def bfs(maze, start, goal):
    n, m = len(maze), len(maze[0])
    queue = deque([start])
    visited = set([start])
    parent = {}

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    while queue:
        x, y = queue.popleft()

        if (x, y) == goal:
            return reconstruct_path(parent, start, goal)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m:
                if maze[nx][ny] == '0' and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

    return None


#DFS
def dfs(maze, start, goal):
    n, m = len(maze), len(maze[0])
    stack = [start]
    visited = set([start])
    parent = {}

    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    while stack:
        x, y = stack.pop()

        if (x, y) == goal:
            return reconstruct_path(parent, start, goal)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m:
                if maze[nx][ny] == '0' and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    stack.append((nx, ny))

    return None

#Main
if __name__ == "__main__":
    maze, start, goal = read_maze("Tuan03//MeCung//maze.txt")


    path = bfs(maze, start, goal)   # DÙNG BFS
    # path = dfs(maze, start, goal) # DÙNG DFS (comment BFS, mở dòng này)


    if path:
        print("Tìm thấy đường đi")
        print("Số bước:", len(path) - 1)
        print("Đường đi:")
        for step in path:
            print(step)
    else:
        print("Không tìm thấy đường đi")
