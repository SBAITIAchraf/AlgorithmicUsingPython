while True:
    try:
        from module import square_root

        numb = int(input("Type a number: "))
        numb_sqrt = square_root(numb)
        print(f"the square root of that number is: {numb_sqrt}")

    except ValueError:
        continue
