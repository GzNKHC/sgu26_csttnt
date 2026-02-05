import sys
sys.setrecursionlimit(10**7)

def dfs(cur):
    if cur in visited:
        return

    visited.add(cur)

    #Duyệt ước
    x = 1
    while x * x <= cur:
        if cur % x == 0:
            y = cur // x

            if x <= y:
                new_num = (x - 1) * (y + 1)

                if new_num >= 0:
                    dfs(new_num)

        x += 1

N = int(input().strip())

visited = set()

dfs(N)

#KQ
ans = sorted(visited)
print(*ans)
