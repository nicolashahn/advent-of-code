use std::collections::HashSet;

fn p1(ops: Vec<(&str, i32)>) -> i32 {
    let mut acc = 0;
    let mut i_ptr = 0;

    let mut seen = HashSet::new();

    loop {
        if seen.contains(&i_ptr) {
            return acc;
        }
        seen.insert(i_ptr);
        let (op, val) = ops[i_ptr as usize];
        match op {
            "acc" => acc += val,
            "nop" => (),
            "jmp" => i_ptr += val - 1,
            _ => (),
        }
        i_ptr += 1;
    }
}

fn p2(ops: Vec<(&str, i32)>) -> i32 {
    let terminal = ops.len();
    for i in 0..terminal {
        let mut acc = 0;
        let mut i_ptr = 0;
        let mut seen = HashSet::new();

        loop {
            if seen.contains(&i_ptr) {
                break;
            }
            seen.insert(i_ptr);
            let (mut op, val) = ops[i_ptr as usize];
            if i as i32 == i_ptr {
                if op == "jmp" {
                    op = "nop";
                } else if op == "nop" {
                    op = "jmp";
                }
            }
            match op {
                "acc" => {
                    acc += val;
                    i_ptr += 1;
                }
                "nop" => {
                    i_ptr += 1;
                }
                "jmp" => i_ptr += val,
                _ => panic!("unrecognized op"),
            }
            if i_ptr >= terminal as i32 {
                return acc;
            }
        }
    }
    panic!("no soln found")
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let ops = input
        .lines()
        .map(|l| {
            let toks = l.split(" ").collect::<Vec<_>>();
            (toks[0], toks[1].parse::<i32>().unwrap())
        })
        .collect::<Vec<_>>();
    println!("p1: {}", p1(ops.clone()));
    println!("p2: {}", p2(ops));
}
