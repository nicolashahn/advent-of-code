const DIRS: [(i32, i32); 8] = [
    (0, 1),
    (0, -1),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
    (1, 0),
    (-1, 0),
];

// index into grid using i32 instead of usize
fn idx(grid: &Vec<Vec<char>>, x: i32, y: i32) -> char {
    grid[y as usize][x as usize]
}

// check if coordinate is in the grid
fn on_grid(grid: &Vec<Vec<char>>, x: i32, y: i32) -> bool {
    x >= 0 && y >= 0 && x < grid[0].len() as i32 && y < grid.len() as i32
}

fn tick1(grid: Vec<Vec<char>>) -> Vec<Vec<char>> {
    let mut new = grid.clone();

    let ct_adj = |x: i32, y: i32| {
        let mut ct = 0;
        for (dx, dy) in DIRS.iter() {
            if on_grid(&grid, x + dx, y + dy) && idx(&grid, x + dx, y + dy) == '#' {
                ct += 1
            }
        }

        ct
    };

    for y in 0..grid.len() {
        for x in 0..grid[0].len() {
            if grid[y][x] == '.' {
                continue;
            }
            let ct = ct_adj(x as i32, y as i32);
            let occupied = grid[y][x] == '#';
            new[y][x] = if occupied && ct >= 4 {
                'L'
            } else if !occupied && ct == 0 {
                '#'
            } else {
                grid[y][x]
            }
        }
    }

    new
}

fn tick2(grid: Vec<Vec<char>>) -> Vec<Vec<char>> {
    let mut new = grid.clone();

    let step = |x: i32, y: i32, dx: i32, dy: i32| (x + dx, y + dy);

    let ct_adj = |x: i32, y: i32| {
        let mut ct = 0;

        for &(dx, dy) in DIRS.iter() {
            let (mut nx, mut ny) = (x + dx, y + dy);
            while on_grid(&grid, nx, ny) && idx(&grid, nx, ny) == '.' {
                let (nx2, ny2) = step(nx, ny, dx, dy);
                nx = nx2;
                ny = ny2;
            }
            if on_grid(&grid, nx, ny) && idx(&grid, nx, ny) == '#' {
                ct += 1;
            }
        }

        ct
    };

    for y in 0..grid.len() {
        for x in 0..grid[0].len() {
            if grid[y][x] == '.' {
                continue;
            }
            let ct = ct_adj(x as i32, y as i32);
            let occupied = grid[y][x] == '#';
            new[y][x] = if occupied && ct >= 5 {
                'L'
            } else if !occupied && ct == 0 {
                '#'
            } else {
                grid[y][x]
            }
        }
    }

    new
}

fn sim_til_stable<F>(grid: Vec<Vec<char>>, tick: F) -> usize
where
    F: Fn(Vec<Vec<char>>) -> Vec<Vec<char>>,
{
    let mut last = grid.clone();
    let mut curr = tick(grid);
    while last != curr {
        last = curr.clone();
        curr = tick(curr);
    }

    curr.iter().flatten().filter(|&&c| c == '#').count()
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let grid: Vec<_> = input
        .lines()
        .map(|l| l.chars().collect::<Vec<_>>())
        .collect();
    println!("p1: {}", sim_til_stable(grid.clone(), tick1));
    println!("p2: {}", sim_til_stable(grid, tick2));
}
