def while_function(max, incrementor):
    i = 0
    numbers = []
    while i < max:
        print(f"At the top i is {i}")
        numbers.append(i)

        i += incrementor
        print("Numbers now: ", numbers)
        print(f"At the bottom i is {i}")

    print("The numbers: ")

    for num in numbers:
        print(num)

while_function(100, 10)
