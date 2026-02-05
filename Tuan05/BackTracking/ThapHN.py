def hanoi(n, A, C, B):
    #Đk
    if n == 1:
        print(f"Chuyển đĩa 1 từ {A} → {C}")
        return

    #Chuyển n-1 từ A sang B
    hanoi(n-1, A, B, C)

    #Chuyển đĩa lớn nhất
    print(f"Chuyển đĩa {n} từ {A} → {C}")

    #Chuyển n-1 từ B sang C
    hanoi(n-1, B, C, A)


#Test
n = 3
hanoi(n, "A", "C", "B")
