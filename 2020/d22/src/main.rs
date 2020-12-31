use std::collections::{HashSet, VecDeque};

fn p1(mut d1: VecDeque<usize>, mut d2: VecDeque<usize>) -> usize {
    while !d1.is_empty() && !d2.is_empty() {
        let top1 = d1.pop_front().unwrap();
        let top2 = d2.pop_front().unwrap();
        if top1 > top2 {
            d1.push_back(top1);
            d1.push_back(top2);
        } else {
            d2.push_back(top2);
            d2.push_back(top1);
        }
    }
    let winner = if d1.is_empty() { d2 } else { d1 };

    winner
        .iter()
        .rev()
        .enumerate()
        .map(|(i, c)| (i + 1) * c)
        .sum()
}

fn rec(
    mut d1: VecDeque<usize>,
    mut d2: VecDeque<usize>,
) -> (bool, VecDeque<usize>, VecDeque<usize>) {
    let mut cache: HashSet<(VecDeque<usize>, VecDeque<usize>)> = HashSet::new();
    #[allow(unused_assignments)]
    let mut p1_won = None;
    loop {
        let cache_key = (d1.clone(), d2.clone());
        if cache.contains(&cache_key) {
            p1_won = Some(true);
            break;
        }
        cache.insert(cache_key);
        let top1 = d1.pop_front().unwrap();
        let top2 = d2.pop_front().unwrap();
        if top1 <= d1.len() && top2 <= d2.len() {
            let nd1 = d1.iter().take(top1).cloned().collect::<VecDeque<_>>();
            let nd2 = d2.iter().take(top2).cloned().collect::<VecDeque<_>>();
            let (p1_won_sub, _, _) = rec(nd1, nd2);
            if p1_won_sub {
                d1.push_back(top1);
                d1.push_back(top2);
            } else {
                d2.push_back(top2);
                d2.push_back(top1);
            }
        } else {
            if top1 > top2 {
                d1.push_back(top1);
                d1.push_back(top2);
            } else {
                d2.push_back(top2);
                d2.push_back(top1);
            }
        }
        if d1.is_empty() {
            p1_won = Some(false);
            break;
        } else if d2.is_empty() {
            p1_won = Some(true);
            break;
        }
    }

    (p1_won.unwrap(), d1, d2)
}

fn p2(d1: VecDeque<usize>, d2: VecDeque<usize>) -> usize {
    let (p1_won, final_d1, final_d2) = rec(d1, d2);
    let winner = if p1_won { final_d1 } else { final_d2 };

    winner
        .iter()
        .rev()
        .enumerate()
        .map(|(i, c)| (i + 1) * c)
        .sum()
}
fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let decks = input
        .split("\n\n")
        .map(|deck| {
            let mut lines = deck.lines();
            let _ = lines.next();
            lines
                .map(|card| card.parse::<usize>().unwrap())
                .collect::<VecDeque<_>>()
        })
        .collect::<Vec<_>>();

    println!("p1: {}", p1(decks[0].clone(), decks[1].clone()));
    println!("p2: {}", p2(decks[0].clone(), decks[1].clone()));
}
