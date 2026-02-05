import sys
sys.setrecursionlimit(10**7)

def determinant(mat, n):

    if n == 1:
        return mat[0][0]

    if n == 2:
        return mat[0][0]*mat[1][1] - mat[0][1]*mat[1][0]

    res = 0

    #Khai triển theo hàng 0
    for j in range(n):

        #Tạo ma trận con
        sub = []

        for i in range(1, n):
            row = []
            for k in range(n):
                if k != j:
                    row.append(mat[i][k])
            sub.append(row)

        sign = 1 if j % 2 == 0 else -1
        res += sign * mat[0][j] * determinant(sub, n-1)

    return res

n = int(input())

A = []

for _ in range(n):
    A.append(list(map(int, input().split())))

print(determinant(A, n))
