def find_max(arr, n):
    if n == 1:
        return arr[0]

    max_prev = find_max(arr, n - 1)
    if arr[n - 1] > max_prev:
        return arr[n - 1]
    else:
        return max_prev

n = int(input("Nhập số phần tử: "))
arr = list(map(int, input("Nhập dãy số: ").split()))

print("Giá trị lớn nhất:", find_max(arr, n))
