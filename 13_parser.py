from re import findall


def as_integers(xs):
    return list(map(int, xs))


def split_list(xs, n):
    return [as_integers(xs[i : i + n]) for i in range(0, len(xs), n)]


def parse(file):
    with open(file, "r") as file:
        text = file.read()

    return split_list(findall(r"[XY][+=](\d+)", text), 6)


if __name__ == "__main__":
    print(f"example: {parse('example')}")
