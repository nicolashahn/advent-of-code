use std::collections::HashMap;
use std::thread;

fn get_nth_num(lines: Vec<usize>, n: usize, mut map: &mut HashMap<usize, usize>) -> usize {
    if n == lines.len() - 1 {
        for i in 0..(n) {
            map.insert(lines[i], i);
        }
        return lines[n];
    }

    let last = get_nth_num(lines, n - 1, &mut map);
    if let Some(last_n) = map.get(&last).cloned() {
        map.insert(last, n - 1);

        n - last_n - 1
    } else {
        map.insert(last, n - 1);

        0
    }
}

fn p1(lines: Vec<usize>) -> usize {
    get_nth_num(lines, 2020 - 1, &mut HashMap::new())
}

fn p2(lines: Vec<usize>) -> usize {
    // lets us get extra stack space
    thread::Builder::new()
        .name("reductor".into())
        .stack_size(32 * 1024 * 1024 * 512)
        .spawn(move || get_nth_num(lines, 30000000 - 1, &mut HashMap::new()))
        .unwrap()
        .join()
        .unwrap()
}

fn main() {
    let input = vec![18, 11, 9, 0, 5, 1];
    println!("p1: {}", p1(input.clone()));
    println!("p2: {}", p2(input));
}
