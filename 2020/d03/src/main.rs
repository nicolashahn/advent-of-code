fn p1(lines: &Vec<&str>, right: usize) -> usize {
    let mut idx = 0;

    lines
        .iter()
        .map(|line| {
            let chars = line.chars().collect::<Vec<_>>();
            let ans = if chars[idx] == '#' { 1 } else { 0 };
            idx += right;
            idx %= chars.len();
            ans
        })
        .sum()
}

fn p2(lines: &Vec<&str>) -> usize {
    p1(lines, 1)
        * p1(lines, 3)
        * p1(lines, 5)
        * p1(lines, 7)
        * p1(&lines.iter().step_by(2).cloned().collect(), 1)
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let lines = input.split("\n").filter(|&n| n != "").collect::<Vec<_>>();

    println!("p1: {}", p1(&lines, 3));
    println!("p2: {}", p2(&lines));
}
