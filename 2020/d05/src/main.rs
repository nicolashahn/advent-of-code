use std::collections::HashSet;

fn get_row_col(seat: &str) -> (usize, usize) {
    let chars = seat.chars().rev().collect::<Vec<_>>();

    let col = (0..3)
        .filter(|i| chars[*i] == 'R')
        .map(|i| usize::pow(2, i as u32))
        .sum();
    let row = (3..10)
        .filter(|i| chars[*i] == 'B')
        .map(|i| usize::pow(2, i as u32 - 3))
        .sum();

    (row, col)
}

fn get_id(row: usize, col: usize) -> usize {
    row * 8 + col
}

fn p1(seats: &Vec<&str>) -> usize {
    seats
        .iter()
        .map(|&s| {
            let (row, col) = get_row_col(s);
            get_id(row, col)
        })
        .max()
        .unwrap()
}

fn p2(seats: &Vec<&str>) -> usize {
    let row_cols = seats
        .iter()
        .map(|&s| get_row_col(s))
        .collect::<HashSet<_>>();

    let mut first_block = false;
    for r in 0..128 {
        for c in 0..8 {
            // if seat is filled
            if row_cols.contains(&(r, c)) {
                // entered first block of contiguous seats
                first_block = true;
            } else {
                // found the first empty seat after the first block
                if first_block {
                    return get_id(r, c);
                }
            }
        }
    }
    panic!("oops")
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let seats = input.lines().collect::<Vec<_>>();
    println!("p1 {:?}", p1(&seats));
    println!("p2 {:?}", p2(&seats));
}
