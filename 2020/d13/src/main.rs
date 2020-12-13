fn p1(ts: i64, buses: Vec<i64>) -> i64 {
    let mut nts = ts;
    loop {
        for b in buses.iter().filter(|&&b| b != -1) {
            if nts % b == 0 {
                return (nts - ts) * b;
            }
        }
        nts += 1;
    }
}

fn egcd(a: i64, b: i64) -> (i64, i64, i64) {
    if a == 0 {
        (b, 0, 1)
    } else {
        let (g, x, y) = egcd(b % a, a);
        (g, y - (b / a) * x, x)
    }
}

fn mod_inv(x: i64, n: i64) -> i64 {
    let (_, x, _) = egcd(x, n);
    (x % n + n) % n
}

fn chi_rem(pairs: &[(i64, i64)]) -> i64 {
    let product = pairs.iter().map(|(r, _)| r).product::<i64>();

    pairs.iter().fold(0, |acc, (i, j)| {
        let p = product / i;
        acc + j * mod_inv(p, *i) * p
    }) % product
}

fn p2(buses: Vec<i64>) -> i64 {
    chi_rem(
        &buses
            .iter()
            .enumerate()
            .filter(|&(_, &b)| b != -1)
            .map(|(i, &b)| (b, b - i as i64))
            .collect::<Vec<_>>(),
    )
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let input_lines: Vec<_> = input.lines().collect();
    let ts = input_lines[0].parse::<i64>().unwrap();
    let buses: Vec<_> = input_lines[1]
        .split(",")
        .map(|b| b.parse::<i64>().unwrap_or(-1))
        .collect();
    println!("p1: {}", p1(ts, buses.clone()));
    println!("p2: {}", p2(buses));
}
