use std::collections::HashMap;

fn p1(passports: &Vec<HashMap<String, String>>) -> usize {
    let fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"];
    passports
        .iter()
        .filter(|&p| fields.iter().filter(|&&f| p.contains_key(f)).count() == 7)
        .count()
}

fn p2(passports: &Vec<HashMap<String, String>>) -> usize {
    let fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"];
    passports
        .iter()
        .filter(|&p| fields.iter().filter(|&&f| p.contains_key(f)).count() == 7)
        .filter(|&p| {
            if let Some(byr) = p.get("byr").unwrap().parse::<i64>().ok() {
                if byr < 1920 || byr > 2002 {
                    return false;
                }
            }

            if let Some(iyr) = p.get("iyr").unwrap().parse::<i64>().ok() {
                if iyr < 2010 || iyr > 2020 {
                    return false;
                }
            }

            if let Some(eyr) = p.get("eyr").unwrap().parse::<i64>().ok() {
                if eyr < 2020 || eyr > 2030 {
                    return false;
                }
            }

            let hgt_raw = p.get("hgt").unwrap();
            let last_two: String = hgt_raw.chars().rev().take(2).collect();
            let hgt = hgt_raw
                .chars()
                .take(hgt_raw.len() - 2)
                .collect::<String>()
                .parse::<i64>()
                .ok();
            if let Some(hgt) = hgt {
                if last_two == "mc" {
                    if hgt < 150 || hgt > 193 {
                        return false;
                    }
                } else if last_two == "ni" {
                    if hgt < 59 || hgt > 76 {
                        return false;
                    }
                } else {
                    return false;
                }
            } else {
                return false;
            }

            let hcl_chars = p.get("hcl").unwrap().chars().collect::<Vec<_>>();
            if hcl_chars.len() != 7 || hcl_chars[0] != '#' {
                return false;
            }
            for i in 1..7 {
                if !"1234567890abcdef".contains(hcl_chars[i]) {
                    return false;
                }
            }

            if !["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
                .contains(&p.get("ecl").unwrap().as_str())
            {
                return false;
            }

            let pid = p.get("pid").unwrap().chars().collect::<Vec<_>>();
            if pid.iter().filter(|c| !c.is_numeric()).count() != 0 || pid.len() != 9 {
                return false;
            }

            true
        })
        .count()
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let passports = input
        .split("\n\n")
        .filter(|&s| s != "")
        .map(|w| {
            w.replace("\n", " ")
                .split(" ")
                .filter(|&s| s != "")
                .map(|f| {
                    let pair = f.split(":").map(|s| s.to_string()).collect::<Vec<_>>();
                    (pair[0].clone(), pair[1].clone())
                })
                .collect::<HashMap<_, _>>()
        })
        .collect::<Vec<_>>();

    println!("p1: {:?}", p1(&passports));
    println!("p2: {:?}", p2(&passports));
}
