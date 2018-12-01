with open('in.txt', 'r') as f:
    digits = f.read()
    digits = digits + digits[0]
    s = 0
    for i in range(1, len(digits)):
        if digits[i] == digits[i-1]:
            s += int(digits[i-1])
    print(s)
