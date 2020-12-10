use std::collections::BTreeMap;

fn p1(ads: Vec<usize>) -> usize {
    let mut ones = 0;
    let mut threes = 0;
    for i in 0..(ads.len() - 1) {
        let diff = ads[i + 1] - ads[i];
        ones += if diff == 1 { 1 } else { 0 };
        threes += if diff == 3 { 1 } else { 0 };
    }

    ones * threes
}

fn rec(ads: &Vec<usize>, i: usize, cache: &mut BTreeMap<usize, usize>) -> usize {
    if cache.contains_key(&i) {
        return *cache.get(&i).unwrap();
    }
    if i == ads.len() - 1 {
        return 1;
    }

    let mut res = 0;
    for j in (i + 1)..=(i + 3) {
        if j < ads.len() && ads[j] - ads[i] <= 3 {
            res += rec(&ads, j, cache);
        }
    }
    cache.insert(i, res);

    res
}

fn p2(ads: Vec<usize>) -> usize {
    rec(&ads, 0, &mut BTreeMap::new())
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let mut ads: Vec<_> = input.lines().map(|n| n.parse::<usize>().unwrap()).collect();
    ads.push(0);
    ads.push(3 + *ads.iter().max().unwrap());
    ads.sort();
    println!("p1: {}", p1(ads.clone()));
    println!("p2: {}", p2(ads));
}
