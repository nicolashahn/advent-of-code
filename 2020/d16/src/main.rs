use parse_display::{Display, FromStr};
use std::collections::{HashMap, HashSet};

#[derive(Hash, Display, FromStr, PartialEq, Eq, Debug, Clone)]
#[display("{name}: {l1}-{h1} or {l2}-{h2}")]
struct Field {
    name: String,
    l1: usize,
    h1: usize,
    l2: usize,
    h2: usize,
}

// since ticket values can only be up to 1000, just use an array you can index into to check if a
// number is valid for the given field
fn make_valids_arr(fields: &Vec<Field>) -> [bool; 1000] {
    let mut valids = [false; 1000];
    for field in fields.iter() {
        for i in field.l1..field.h1 {
            valids[i] = true;
        }
        for i in field.l2..field.h2 {
            valids[i] = true;
        }
    }

    valids
}

fn p1(fields: Vec<Field>, tickets: Vec<Vec<usize>>) -> usize {
    let valids = make_valids_arr(&fields);

    let mut invalids = 0;
    for ticket in tickets.iter() {
        for val in ticket.iter() {
            if !valids[*val] {
                invalids += val;
            }
        }
    }

    invalids
}

fn p2(fields: Vec<Field>, tickets: Vec<Vec<usize>>, mine: Vec<usize>) -> usize {
    let valids = make_valids_arr(&fields);

    let good_tickets = tickets
        .iter()
        .filter(|t| {
            for val in t.iter() {
                if !valids[*val] {
                    return false;
                }
            }
            true
        })
        .collect::<Vec<_>>();

    // value is valid for given Field based in its two ranges
    let is_valid = |field: Field, val: usize| {
        (val >= field.l1 && val <= field.h1) || (val >= field.l2 && val <= field.h2)
    };

    // based on good_tickets, each field could possibly match up with these ticket positions
    let mut possibilities = HashMap::new();
    for field in fields.iter() {
        for pos in 0..good_tickets[0].len() {
            if good_tickets
                .iter()
                .map(|t| t[pos])
                .filter(|v| is_valid(field.clone(), *v))
                .count()
                == good_tickets.len()
            {
                possibilities
                    .entry(field.name.as_str())
                    .or_insert_with(HashSet::new)
                    .insert(pos);
            }
        }
    }

    // final field->position mappings
    let mut mapping = HashMap::new();
    while mapping.len() < fields.len() {
        let (mut found_n, mut found_p) = ("", 999);
        for (&f, ps) in possibilities.iter() {
            if ps.len() == 1 {
                found_n = f;
                found_p = ps.iter().next().unwrap().clone();
                mapping.insert(found_p, found_n);
                break;
            }
        }
        for (_, ps) in possibilities.iter_mut() {
            ps.remove(&found_p);
        }
        possibilities.remove(&found_n);
    }

    // translate my ticket into field->val mapping
    let mine_mapped = mine
        .into_iter()
        .enumerate()
        .map(|(i, v)| (*mapping.get(&i).unwrap(), v))
        .collect::<HashMap<_, _>>();

    // multiply departure field values
    mine_mapped
        .into_iter()
        .filter_map(|(f, v)| {
            if f.starts_with("departure") {
                Some(v)
            } else {
                None
            }
        })
        .product()
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let sections = input
        .split("\n\n")
        .map(|s| s.lines().collect::<Vec<_>>())
        .collect::<Vec<_>>();
    let fields = sections[0]
        .iter()
        .map(|l| l.parse::<Field>().unwrap())
        .collect::<Vec<_>>();
    let mine = sections[1][1]
        .split(",")
        .map(|n| n.parse::<usize>().unwrap())
        .collect();
    let tickets = sections[2]
        .iter()
        .skip(1)
        .map(|l| {
            l.split(",")
                .map(|n| n.parse::<usize>().unwrap())
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();
    println!("p1: {}", p1(fields.clone(), tickets.clone()));
    println!("p2: {}", p2(fields, tickets, mine));
}
