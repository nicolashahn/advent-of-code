use std::collections::HashMap;
use Rule::{Concat, Or, Val};

#[derive(Eq, PartialEq, Debug, Clone)]
enum Rule {
    Or(Rules<usize>, Rules<usize>),
    Concat(Rules<usize>),
    Val(char),
}
type Rules<A> = Vec<A>;

/// For the given rule and the given character index of the input to start at: If the current rule
/// matches the input, return the new character index after consuming all the characters that the
/// rule matches on. If no match, return None.
fn matches(
    rules: &HashMap<usize, Rule>,
    ri: usize,
    chars: &Vec<char>,
    ci: usize,
) -> Option<Rules<usize>> {
    if ci == chars.len() {
        return None;
    }

    // nris = new rule indexes
    let match_nris = |nris: &Rules<usize>| -> Option<Rules<usize>> {
        // cci = current char index
        let mut ccis: Rules<_> = vec![ci].into_iter().collect();
        for &nri in nris.iter() {
            for &cci in ccis.clone().iter() {
                let maybe_ccis = matches(rules, nri, chars, cci);
                // new char index
                if let Some(ncis) = maybe_ccis {
                    ccis = ncis.clone();
                } else {
                    return None;
                }
            }
        }

        Some(ccis)
    };

    let res = match rules.get(&ri).unwrap() {
        Val(v) => {
            if v == &chars[ci] {
                Some(vec![ci + 1].into_iter().collect())
            } else {
                None
            }
        }
        Concat(nris) => match_nris(nris),
        Or(nris1, nris2) => match (match_nris(nris1), match_nris(nris2)) {
            (Some(mut ccis1), Some(ccis2)) => Some({
                ccis1.extend(ccis2);
                ccis1
            }),
            (Some(ccis), None) => Some(ccis),
            (None, Some(ccis)) => Some(ccis),
            (None, None) => None,
        },
    };

    //if ri == 11 || ri == 8 {
    //    println!("{} {} {:?}", ri, ci, res);
    //}

    res
}

fn p1(rules: HashMap<usize, Rule>, msgs: Vec<&str>) -> usize {
    //println!("{:?}, {:?}", rules, msgs);
    msgs.iter()
        .filter(|msg| {
            let chars = msg.chars().collect::<Vec<_>>();
            matches(&rules, 0, &chars, 0)
                .filter(|cis| {
                    //println!("{:?}, {}", cis, msg);
                    *cis.into_iter().next().unwrap() == chars.len()
                })
                .is_some()
        })
        .count()
}

fn p2(mut rules: HashMap<usize, Rule>, msgs: Vec<&str>) -> usize {
    rules.insert(8, Or(vec![42], vec![42, 8]));
    rules.insert(11, Or(vec![42, 31], vec![42, 11, 31]));
    p1(rules, msgs)
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let mut sections = input.split("\n\n");
    let rules = sections
        .next()
        .unwrap()
        .lines()
        .map(|l| {
            let mut split = l.split(": ");
            let rnum = split.next().unwrap().parse::<usize>().unwrap();
            let rhside = split.next().unwrap();
            let rsubs = if rhside.contains("\"") {
                Val(rhside.replace("\"", "").chars().next().unwrap())
            } else if rhside.contains(" | ") {
                let mut rs = rhside.split(" | ").map(|rsub| {
                    rsub.split(" ")
                        .map(|t| t.parse::<usize>().unwrap())
                        .collect()
                });
                Or(rs.next().unwrap(), rs.next().unwrap())
            } else {
                Concat(
                    rhside
                        .split(" ")
                        .map(|t| t.parse::<usize>().unwrap())
                        .collect(),
                )
            };

            (rnum, rsubs)
        })
        .collect::<HashMap<_, _>>();
    let msgs = sections.next().unwrap().lines().collect::<Vec<_>>();

    println!("p1: {}", p1(rules.clone(), msgs.clone()));
    //println!("p2: {}", p2(rules.clone(), msgs.clone()));
}
