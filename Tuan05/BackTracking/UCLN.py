def UCLN(m, n):

    if n == 0:
        return m

    return UCLN(n, m % n)


# Test
m, n = map(int, input().split())
print(UCLN(m, n))
