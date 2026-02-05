def tong1(n):

    if n == 1:
        return 1

    return tong1(n-1) + 1/n


# Test
n = int(input())
print(tong1(n))
