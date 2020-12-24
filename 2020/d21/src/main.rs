use std::collections::{HashMap, HashSet};

fn p1(ings_alrs: Vec<(HashSet<String>, HashSet<String>)>) -> usize {
    let mut all_alrs: HashSet<&str> = HashSet::new();
    let mut all_ings: HashSet<&str> = HashSet::new();
    for (ings, alrs) in ings_alrs.iter() {
        all_alrs.extend(alrs.iter().map(|s| s.as_str()).collect::<HashSet<_>>());
        all_ings.extend(ings.iter().map(|s| s.as_str()).collect::<HashSet<_>>());
    }
    let mut alr_possibilities: HashMap<&str, HashSet<&str>> = HashMap::new();
    for (ings, alrs) in ings_alrs.iter() {
        for alr in alrs.iter() {
            if !alr_possibilities.contains_key(alr.as_str()) {
                alr_possibilities.insert(
                    &alr,
                    ings.iter().map(|s| s.as_str()).collect::<HashSet<_>>(),
                );
            } else {
                if let Some(s) = alr_possibilities.get_mut(alr.as_str()) {
                    let ing_set = ings.iter().map(|s| s.as_str()).collect::<HashSet<_>>();
                    let new_s = s.intersection(&ing_set).cloned().collect::<HashSet<_>>();
                    alr_possibilities.insert(alr.as_str(), new_s);
                }
            }
        }
    }

    let all_allergic_ings = alr_possibilities
        .values()
        .flatten()
        .cloned()
        .collect::<HashSet<_>>();

    let mut count = 0;
    for (ings, _) in ings_alrs.iter() {
        for ing in ings.iter() {
            if !all_allergic_ings.contains(ing.as_str()) {
                count += 1;
            }
        }
    }

    count
}

fn p2(ings_alrs: Vec<(HashSet<String>, HashSet<String>)>) -> String {
    let mut all_alrs: HashSet<&str> = HashSet::new();
    let mut all_ings: HashSet<&str> = HashSet::new();
    for (ings, alrs) in ings_alrs.iter() {
        all_alrs.extend(alrs.iter().map(|s| s.as_str()).collect::<HashSet<_>>());
        all_ings.extend(ings.iter().map(|s| s.as_str()).collect::<HashSet<_>>());
    }
    let mut alr_possibilities: HashMap<&str, HashSet<&str>> = HashMap::new();
    for (ings, alrs) in ings_alrs.iter() {
        for alr in alrs.iter() {
            if !alr_possibilities.contains_key(alr.as_str()) {
                alr_possibilities.insert(
                    &alr,
                    ings.iter().map(|s| s.as_str()).collect::<HashSet<_>>(),
                );
            } else {
                if let Some(s) = alr_possibilities.get_mut(alr.as_str()) {
                    let ing_set = ings.iter().map(|s| s.as_str()).collect::<HashSet<_>>();
                    let new_s = s.intersection(&ing_set).cloned().collect::<HashSet<_>>();
                    alr_possibilities.insert(alr.as_str(), new_s);
                }
            }
        }
    }

    let mut alr_map: HashMap<&str, &str> = HashMap::new();
    while !alr_possibilities.is_empty() {
        let mut single = "";
        for (alr, ings) in alr_possibilities.iter() {
            if ings.len() == 1 {
                single = alr;
            }
        }
        let ing = alr_possibilities
            .get(single)
            .unwrap()
            .iter()
            .next()
            .unwrap()
            .clone();
        alr_map.insert(single, ing);
        for (_, other_ings) in alr_possibilities.iter_mut() {
            other_ings.remove(ing);
        }
        alr_possibilities.remove(single);
    }

    let mut sorted = alr_map.into_iter().collect::<Vec<_>>();
    sorted.sort();

    sorted
        .into_iter()
        .map(|(_, i)| i)
        .collect::<Vec<_>>()
        .join(",")
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let ingredients_allergens = input
        .lines()
        .map(|line| {
            let split = line
                .split(" (contains ")
                .map(|s| s.to_string())
                .collect::<Vec<String>>();
            let ingredients = split[0]
                .split(" ")
                .map(|s| s.to_string())
                .collect::<HashSet<String>>();
            let mut allergens = split[1]
                .split(", ")
                .map(|s| s.to_string())
                .collect::<Vec<String>>();
            let last = allergens.len() - 1;
            allergens[last] = allergens[last].replace(")", "");

            (ingredients, allergens.into_iter().collect::<HashSet<_>>())
        })
        .collect::<Vec<_>>();
    println!("p1: {}", p1(ingredients_allergens.clone()));
    println!("p2: {}", p2(ingredients_allergens));
}
