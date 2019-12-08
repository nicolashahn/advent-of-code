from collections import Counter

H = 6
W = 25


def p1(img):
    layers = []
    for i in range(0, len(img), H * W):
        layers.append(img[i : i + H * W])
    minl = min(layers, key=lambda l: Counter(l)["0"])
    c = Counter(minl)
    return c["1"] * c["2"]


def p2(img):
    layers = []
    for i in range(0, len(img), H * W):
        layers.append(img[i : i + H * W])
    final = list(layers[-1])
    for l in layers[::-1]:
        for i in range(H * W):
            if l[i] != "2":
                final[i] = l[i]
    i = 0
    for y in range(H):
        row = ""
        for x in range(W):
            row += final[i]
            i += 1
        print(row.replace("0", " "))


def main():
    with open("in.txt", "r") as f:
        img = f.read().strip()
        # print(p1(img))
        p2(img)


if __name__ == "__main__":
    main()
