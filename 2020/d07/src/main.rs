/// this is garbage, please close the file
use std::collections::HashMap;

fn dfs<'a>(
    rev_map: &'a HashMap<(&str, &str), Vec<(&str, &str)>>,
    start: (&str, &str),
    end: (&str, &str),
) -> bool {
    if start == end {
        return true;
    }
    for &b in rev_map.get(&start).unwrap_or(&vec![]) {
        if dfs(rev_map, b, end) {
            return true;
        }
    }

    false
}

fn p1(map: HashMap<(&str, &str), Vec<(usize, (&str, &str))>>) -> usize {
    let mut rev_map: HashMap<(&str, &str), Vec<(&str, &str)>> = HashMap::new();

    for (c_desc_color, val) in map.iter() {
        for (_num, desc_color) in val.iter() {
            rev_map
                .entry(*desc_color)
                .and_modify(|v| v.push(*c_desc_color))
                .or_insert_with(Vec::new);
            rev_map.entry(*c_desc_color).or_insert_with(Vec::new);
        }
    }

    let no_num_map = map
        .iter()
        .map(|(k, v)| (*k, v.iter().map(|(_, b)| *b).collect::<Vec<_>>()))
        .collect();

    map.keys()
        .filter(|&&k| k != ("shiny", "gold"))
        .map(|&k| dfs(&no_num_map, k, ("shiny", "gold")))
        .filter(|x| *x)
        .count()
}

fn dfs2<'a>(
    map: &'a HashMap<(&str, &str), Vec<(usize, (&str, &str))>>,
    start: (&str, &str),
) -> usize {
    let mut ans = 0;
    for &(n, b) in map.get(&start).unwrap_or(&vec![]) {
        ans += n + n * dfs2(map, b);
    }

    ans
}

fn p2(map: HashMap<(&str, &str), Vec<(usize, (&str, &str))>>) -> usize {
    dfs2(&map, ("shiny", "gold"))
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let map = input
        .lines()
        .map(|l| {
            let contain_split = l.split("contain").collect::<Vec<_>>();
            let c_bag = contain_split[0].split(" ").take(2).collect::<Vec<_>>();
            let c_bag_desc = c_bag[0];
            let c_bag_col = c_bag[1];
            let bags = contain_split[1]
                .split(",")
                .map(|b| {
                    let bs = b.split(" ").collect::<Vec<_>>();
                    if bs[1] == "no" {
                        return (0, ("", ""));
                    }
                    let num = bs[1].parse::<usize>().unwrap();
                    let bag_desc = bs[2];
                    let bag_col = bs[3];
                    (num, (bag_desc, bag_col))
                })
                .collect::<Vec<_>>();

            ((c_bag_desc, c_bag_col), bags)
        })
        .collect::<HashMap<_, _>>();

    println!("p1 {}", p1(map.clone()));
    println!("p2 {}", p2(map));
}
