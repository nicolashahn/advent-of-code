use parse_display::{Display, FromStr};
use std::collections::HashMap;

#[derive(Display, FromStr, PartialEq, Debug, Clone)]
#[display("mem[{addr}] = {val}")]
struct Stmt {
    addr: usize,
    val: usize,
}

#[derive(Display, FromStr, PartialEq, Debug, Clone)]
#[display("mask = {raw}")]
struct Mask {
    raw: String,
}

#[derive(PartialEq, Debug, Clone)]
enum Line {
    Stmt(Stmt),
    Mask(Mask),
}

fn apply_mask(mask: &str, val: usize) -> usize {
    let mut val_bin_chars = format!("{:0>36b}", val).chars().collect::<Vec<_>>();
    for (i, c) in mask.chars().enumerate() {
        if c != 'X' {
            val_bin_chars[i] = c;
        }
    }
    usize::from_str_radix(
        &String::from_utf8(val_bin_chars.into_iter().map(|c| c as u8).collect()).unwrap(),
        2,
    )
    .unwrap()
}

fn p1(lines: Vec<Line>) -> usize {
    let mut regs = HashMap::new();
    let mut mask = "".to_string();
    for line in lines.into_iter() {
        match line {
            Line::Stmt(reg) => {
                regs.insert(reg.addr, apply_mask(&mask, reg.val));
            }
            Line::Mask(mask_) => {
                mask = mask_.raw;
            }
        }
    }

    regs.values().sum()
}

fn get_possible_addrs(mask: &str, addr: usize) -> Box<dyn Iterator<Item = usize>> {
    let mut res = vec![vec![]];

    let mut mask_chars = mask.chars().collect::<Vec<_>>();
    for (i, c) in format!("{:0>36b}", addr).chars().enumerate() {
        if mask_chars[i] != 'X' && mask_chars[i] != '1' {
            mask_chars[i] = c;
        }
    }

    for c in mask_chars.into_iter() {
        if c == 'X' {
            // for each partial binary string in res, replace with 2 more with either a 0 or 1
            // appended
            let mut to_add = vec![];
            for mut s in res.into_iter() {
                let mut s_ = s.clone();
                s_.push('0');
                s.push('1');
                to_add.push(s_);
                to_add.push(s);
            }
            res = to_add;
        } else {
            for s in res.iter_mut() {
                s.push(c);
            }
        }
    }

    Box::new(
        res.into_iter()
            .map(|chars| usize::from_str_radix(&chars.iter().collect::<String>(), 2).unwrap()),
    )
}

fn p2(lines: Vec<Line>) -> usize {
    let mut regs = HashMap::new();
    let mut mask = "".to_string();
    for line in lines.into_iter() {
        match line {
            Line::Stmt(reg) => {
                for addr in get_possible_addrs(&mask, reg.addr) {
                    regs.insert(addr, reg.val);
                }
            }
            Line::Mask(mask_) => {
                mask = mask_.raw;
            }
        }
    }

    regs.values().sum()
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let lines: Vec<_> = input
        .lines()
        .map(|l| {
            if l.starts_with("mask") {
                Line::Mask(l.parse::<Mask>().unwrap())
            } else {
                Line::Stmt(l.parse::<Stmt>().unwrap())
            }
        })
        .collect();
    println!("p1: {}", p1(lines.clone()));
    println!("p2: {}", p2(lines));
}
