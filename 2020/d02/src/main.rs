use std::fs;

fn p1(lines: &Vec<(i64, i64, char, &str)>) -> i64 {
    let mut ans = 0;

    for (low, hi, letter, password) in lines {
        let mut count = 0;
        for c in password.chars() {
            if c == *letter {
                count += 1;
            }
        }

        ans += if *low <= count && count <= *hi { 1 } else { 0 }
    }

    ans
}

fn p2(lines: &Vec<(i64, i64, char, &str)>) -> i64 {
    let mut ans = 0;

    for (low, hi, letter, password) in lines {
        let lowc = password.chars().collect::<Vec<_>>()[*low as usize - 1];
        let hic = password.chars().collect::<Vec<_>>()[*hi as usize - 1];

        ans += if (lowc == *letter && hic != *letter) || (lowc != *letter && hic == *letter) {
            1
        } else {
            0
        }
    }

    ans
}

fn main() {
    let input = fs::read_to_string("./input").unwrap();
    let lines = input
        .split("\n")
        .filter(|&n| n != "")
        .map(|line| {
            let split = line.split(":").collect::<Vec<_>>();
            let range_letter = split[0].split(" ").collect::<Vec<_>>();
            let range = range_letter[0];
            let low_hi = range
                .split("-")
                .map(|n| n.parse::<i64>().unwrap())
                .collect::<Vec<_>>();
            let low = low_hi[0];
            let hi = low_hi[1];
            let letter = range_letter[1].chars().next().unwrap();
            let password = split[1].trim();
            (low, hi, letter, password)
        })
        .collect::<Vec<_>>();

    println!("p1: {}", p1(&lines));
    println!("p2: {}", p2(&lines));
}
