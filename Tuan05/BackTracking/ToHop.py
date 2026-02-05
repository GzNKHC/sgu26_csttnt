def C(n, r):

    #Trường hợp cơ bản
    if r == 0 or r == n:
        return 1

    #Đệ quy Pascal
    return C(n-1, r) + C(n-1, r-1)


#Test
n, r = map(int, input().split())

print(C(n, r))
