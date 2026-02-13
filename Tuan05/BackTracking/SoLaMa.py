def roman_to_int(s, i=0):
    value = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    if i == len(s):
        return 0
    if i == len(s) - 1:
        return value[s[i]]
    if value[s[i]] < value[s[i+1]]:
        return -value[s[i]] + roman_to_int(s, i + 1)
    else:
        return value[s[i]] + roman_to_int(s, i + 1)

s = input("Nhập số La Mã: ").strip().upper()
print("Giá trị:", roman_to_int(s))
