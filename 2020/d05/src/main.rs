use std::collections::HashSet;

fn get_row_col(seat: &str) -> (usize, usize) {
    let chars = seat.chars().collect::<Vec<_>>();
    let mut row = 0;
    let mut col = 0;

    let mut p = 64;
    for i in 0..7 {
        if chars[i] == 'B' {
            row += p;
        }
        p /= 2;
    }
    let mut p = 4;
    for i in 7..10 {
        if chars[i] == 'R' {
            col += p;
        }
        p /= 2;
    }

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

fn p2(seats: &Vec<&str>) {
    let row_cols = seats
        .iter()
        .map(|&s| get_row_col(s))
        .collect::<HashSet<_>>();

    for r in 0..128 {
        for c in 0..8 {
            if !row_cols.contains(&(r, c)) {
                println!("{}", get_id(r, c))
            }
        }
    }
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let seats = input.split("\n").filter(|&s| s != "").collect::<Vec<_>>();
    println!("p1 {:?}", p1(&seats));
    // inspect output manually and look for the odd number out
    p2(&seats);
}
