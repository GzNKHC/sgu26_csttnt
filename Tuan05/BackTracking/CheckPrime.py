import math

def is_prime(n, k=2):
    if n < 2:
        return False
    if k > int(math.sqrt(n)):
        return True
    if n % k == 0:
        return False
    return is_prime(n, k + 1)


n = int(input("Nhập n: "))

if is_prime(n):
    print("Là số nguyên tố")
else:
    print("Không phải số nguyên tố")
