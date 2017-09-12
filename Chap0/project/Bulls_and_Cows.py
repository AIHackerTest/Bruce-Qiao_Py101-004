from random import randint

target = randint(0, 20)

for i in range(10):
    try:
        answer = int(input(f"Please guess the number, you have {10 - i} chances: "))
        if answer == target:
            print("Bingo!")
            break
        elif answer > target:
            print("Greater!")
        else:
            print("Smaller!")
    except:
        print("You should input a number!")
