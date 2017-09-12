import random

# generate 4 digits target random
def Num():  # Why Num() but not num()
    num = random.sample(range(0, 10), 4)
    while num[0] == 0:
        num = random.sample(range(0, 10), 4)
    return num

def guess():
    guesses = input("Please input 4 digits: ")

    if guesses.isdigit() and len(guesses) == 4:
        get_num = []
        for x in guesses:
            get_num.append(int(x))
        return get_num
    else:
        print("You should input 4 digits!")

def comp(number, answer):
    a = c = 0
    for x in range(4):
        if number[x] == answer[x]:
            a += 1
    for y in answer:
        if y in number:
            c += 1
    b = c - a
    return a, b

def play():
    try:
        print("Game begin!")
        number = Num()
        times = 9

        while times >= 0:
            answer = guess()
            print(f"You have {times} chances.")
            times -= 1
            A, B = comp(number, answer)
            print(f"{A}A{B}B")
            if A == 4:
                print("You are right!")
                break
        if times < 0:
            print(f"Sorry! You lose! The answer is {str(number)}")

    except:
        print("Zzz...")

play()
