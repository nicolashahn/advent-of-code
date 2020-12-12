const DIRS: [(i32, i32); 4] = [(1, 0), (0, 1), (-1, 0), (0, -1)];

fn p1(dirs: Vec<(char, i32)>) -> i32 {
    let (mut x, mut y) = (0, 0); // current location
    let mut di = 0; // current direction as index of DIRS

    for (d, n) in dirs {
        match d {
            'N' => y -= n,
            'S' => y += n,
            'E' => x += n,
            'W' => x -= n,
            'L' => {
                di -= n / 90;
                if di < 0 {
                    di += 4;
                }
            }
            'R' => {
                di += n / 90;
                if di > 3 {
                    di -= 4;
                }
            }
            'F' => {
                let (dx, dy) = DIRS[di as usize];
                x += dx * n;
                y += dy * n;
            }
            _ => panic!("unknown char"),
        }
    }

    x.abs() + y.abs()
}

fn p2(dirs: Vec<(char, i32)>) -> i32 {
    let (mut x, mut y) = (0, 0); // current location
    let (mut wx, mut wy) = (10, -1); // waypoint location

    for (d, n) in dirs {
        match d {
            'N' => wy -= n,
            'S' => wy += n,
            'E' => wx += n,
            'W' => wx -= n,
            'L' => {
                for _ in 0..(n / 90) {
                    let old_wy = wy;
                    wy = -wx;
                    wx = old_wy;
                }
            }
            'R' => {
                for _ in 0..(n / 90) {
                    let old_wy = wy;
                    wy = wx;
                    wx = -old_wy;
                }
            }
            'F' => {
                x += wx * n;
                y += wy * n;
            }
            _ => panic!("unknown char"),
        }
    }

    x.abs() + y.abs()
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let dirs: Vec<_> = input
        .lines()
        .map(|l| {
            let mut c = l.chars();
            let dir = c.next().unwrap();
            let num: i32 = c.collect::<String>().parse::<i32>().unwrap();

            (dir, num)
        })
        .collect();
    println!("p1: {}", p1(dirs.clone()));
    println!("p2: {}", p2(dirs));
}
