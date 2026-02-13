import math

def reverse_num(n):
    if n < 10:
        return n
    
    k = int(math.log10(n))
    last = n % 10
    rest = n // 10
    return last * (10 ** k) + reverse_num(rest)


n = int(input("Nhập n: "))
print("Số đảo:", reverse_num(n))
