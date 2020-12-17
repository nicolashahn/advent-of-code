use std::collections::HashSet;

#[derive(Hash, PartialEq, Eq, Copy, Clone)]
struct Coord3(i64, i64, i64);

#[derive(Hash, PartialEq, Eq, Copy, Clone)]
struct Coord4(i64, i64, i64, i64);

trait Adjacents
where
    Self: Eq + std::hash::Hash + Copy,
{
    /// Get all adjacent coordinates to this one (in all dimensions)
    fn get_adj(&self) -> Vec<Self>
    where
        Self: std::marker::Sized;
}

impl Adjacents for Coord3 {
    fn get_adj(&self) -> Vec<Self> {
        let mut res = vec![];
        let self_tuple = (self.0, self.1, self.2);
        let (x, y, z) = self_tuple;
        for nx in (x - 1)..=(x + 1) {
            for ny in (y - 1)..=(y + 1) {
                for nz in (z - 1)..=(z + 1) {
                    if (nx, ny, nz) != self_tuple {
                        res.push(Coord3(nx, ny, nz));
                    }
                }
            }
        }

        res
    }
}

impl Adjacents for Coord4 {
    fn get_adj(&self) -> Vec<Self> {
        let mut res = vec![];
        let self_tuple = (self.0, self.1, self.2, self.3);
        let (x, y, z, a) = self_tuple;
        for nx in (x - 1)..=(x + 1) {
            for ny in (y - 1)..=(y + 1) {
                for nz in (z - 1)..=(z + 1) {
                    for na in (a - 1)..=(a + 1) {
                        if (nx, ny, nz, na) != self_tuple {
                            res.push(Coord4(nx, ny, nz, na));
                        }
                    }
                }
            }
        }

        res
    }
}

/// Get all adjacent coordinates that are not active for each active coordinate
fn get_inactives<A: Adjacents>(actives: &HashSet<A>) -> HashSet<A> {
    let mut inactives = HashSet::new();
    for &active in actives.iter() {
        for &adj in active.get_adj().iter() {
            if !actives.contains(&adj) {
                inactives.insert(adj);
            }
        }
    }

    inactives
}

/// Do one step of the simulation
fn step<A: Adjacents>(actives: HashSet<A>) -> HashSet<A> {
    let inactives = get_inactives(&actives);
    let mut next = HashSet::new();

    for &active in actives.iter() {
        if (2..=3).contains(
            &active
                .get_adj()
                .iter()
                .filter(|&xyz| actives.contains(xyz))
                .count(),
        ) {
            next.insert(active);
        }
    }

    for &inactive in inactives.iter() {
        if 3 == inactive
            .get_adj()
            .iter()
            .filter(|&xyz| actives.contains(xyz))
            .count()
        {
            next.insert(inactive);
        }
    }

    next
}

/// Step through simulation six times and return the count of active coordinates
fn sim<A: Adjacents>(mut actives: HashSet<A>) -> usize {
    for _ in 0..6 {
        actives = step(actives);
    }
    actives.iter().count()
}

fn main() {
    let input = "..#..#..
#.#...#.
..#.....
##....##
#..#.###
.#..#...
###..#..
....#..#";
    let mut pairs = HashSet::new();
    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c == '#' {
                pairs.insert((x as i64, y as i64));
            }
        }
    }
    println!(
        "p1: {}",
        sim(pairs.iter().map(|&(x, y)| Coord3(x, y, 0)).collect())
    );
    println!(
        "p2: {}",
        sim(pairs.iter().map(|&(x, y)| Coord4(x, y, 0, 0)).collect())
    );
}
