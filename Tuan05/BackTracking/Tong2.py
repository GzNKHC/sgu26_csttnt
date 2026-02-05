def tong2(x, n):

    if n == 1:
        return 1

    term = ((-1)**(n+1)) * (x**n)

    return tong2(x, n-1) + term


# Test
x, n = map(float, input().split())
n = int(n)

print(tong2(x, n))
