from random import randint

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
target = []

for i in range(4):
    if i == 0:
        target.append(numbers.pop(randint(1,9)))
    else:
        target.append(numbers.pop(randint(0,9 - i)))

for i in range(10):
    try:
        answer = input(f"Please input 4 digits, you have {10 - i} chances: ")
        is_answer_int = int(answer)
        A_numbers = 0
        B_numbers = 0
        for x in range(4):
            for y in range(4):
                if target[y] == int(list(answer)[x]):
                    if y == x:
                        A_numbers += 1
                    else:
                        B_numbers += 1
        if A_numbers == 4:
            print("Bingo!")
            break
        else:
            print(f"{A_numbers}A{B_numbers}B")
    except:
        print("You should input a number!")

# target_string = ''.join(map(str, target))
print(f"The answer is {''.join(map(str, target))}")
