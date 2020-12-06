use std::collections::HashSet;

fn p1(gs: Vec<&str>) -> usize {
    gs.iter()
        .map(|&g| {
            g.chars()
                .filter(|&c| c != '\n')
                .collect::<HashSet<_>>()
                .len()
        })
        .sum()
}

fn p2(gs: Vec<&str>) -> usize {
    gs.iter()
        .map(|&g| {
            g.lines()
                .map(|l| l.chars().filter(|&c| c != '\n').collect::<HashSet<_>>())
                .fold(('a'..='z').collect::<HashSet<_>>(), |acc, s| {
                    acc.intersection(&s).cloned().collect()
                })
                .len()
        })
        .sum()
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let groups = input.split("\n\n").collect::<Vec<_>>();
    println!("p1 {:?}", p1(groups.clone()));
    println!("p2 {:?}", p2(groups));
}
