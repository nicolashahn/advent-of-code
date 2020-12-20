use std::collections::{HashMap, HashSet};

const TW: usize = 10;

type RawTile = Vec<Vec<char>>;

#[derive(Eq, PartialEq, Debug, Clone, std::hash::Hash)]
struct TileSides {
    id: usize,
    t: Vec<char>,
    b: Vec<char>,
    l: Vec<char>,
    r: Vec<char>,
}

impl TileSides {
    fn new(id: usize, tile: &RawTile) -> TileSides {
        // order is
        // top (from left to right)
        // bottom (from left to right),
        // left (from top to bottom,
        // right (from top to bottom)
        TileSides {
            id,
            t: (tile[0].clone()),
            b: (tile[TW - 1].clone()),
            l: (tile.iter().map(|l| l[0]).collect()),
            r: (tile.iter().map(|l| l[TW - 1]).collect()),
        }
    }

    /// rotate right
    fn rot(&mut self) {
        let nt = self.l.iter().rev().cloned().collect();
        let nr = self.t.clone();
        let nb = self.r.iter().rev().cloned().collect();
        let nl = self.b.clone();
        self.t = nt;
        self.r = nr;
        self.b = nb;
        self.l = nl;
    }

    /// flip across '/' diagonal axis
    fn flip(&mut self) {
        let nt = self.r.iter().rev().cloned().collect();
        let nr = self.t.iter().rev().cloned().collect();
        let nb = self.l.iter().rev().cloned().collect();
        let nl = self.b.iter().rev().cloned().collect();
        self.t = nt;
        self.r = nr;
        self.b = nb;
        self.l = nl;
    }

    fn all_orientations(&mut self) -> Vec<Self> {
        let mut res = vec![self.clone()];
        self.rot();
        res.push(self.clone());
        self.rot();
        res.push(self.clone());
        self.rot();
        res.push(self.clone());
        self.flip();
        res.push(self.clone());
        self.rot();
        res.push(self.clone());
        self.rot();
        res.push(self.clone());
        self.rot();
        res.push(self.clone());

        res
    }

    fn all_sides_as_strings(&self) -> Vec<String> {
        [
            self.r.clone(),
            self.l.clone(),
            self.t.clone(),
            self.b.clone(),
        ]
        .iter()
        .map(|cs| cs.iter().collect::<String>())
        .collect()
    }
}

/// check if grid is in a legal state for each of the tiles that have been placed
fn check_grid(flat: &Vec<&TileSides>, sw: usize) -> bool {
    for i in 0..flat.len() {
        let this = &flat[i];
        // left
        if i % sw > 0 {
            let other = &flat[i - 1];
            if other.r != this.l {
                return false;
            }
        }
        // right
        if i % sw < sw - 1 && i < flat.len() - 1 {
            let other = &flat[i + 1];
            if other.l != this.r {
                return false;
            }
        }
        // up
        if i > sw {
            let other = &flat[i - sw];
            if other.b != this.t {
                return false;
            }
        }
        // down
        if i < sw * (sw - 1) && i + sw < flat.len() {
            let other = &flat[i + sw];
            if other.t != this.b {
                return false;
            }
        }
    }
    true
}

fn p2(tiles: Vec<(usize, Vec<Vec<char>>)>) -> usize {
    // square width
    let sw = (tiles.len() as f64).sqrt() as usize;

    let all_orientations: HashMap<usize, Vec<TileSides>> = tiles
        .iter()
        .map(|(id, raw)| (*id, TileSides::new(*id, raw).all_orientations()))
        .collect();

    // grid flattened out from 2 to 1 dimension
    let mut flat: Vec<&TileSides> = vec![];
    let mut taken = HashSet::new();

    let mut tried: HashSet<Vec<&TileSides>> = HashSet::new();
    'main: loop {
        println!("{}", flat.len());
        for i in 0..tiles.len() {
            if taken.contains(&tiles[i].0) {
                continue;
            }
            for ts in all_orientations.get(&tiles[i].0).unwrap() {
                taken.insert(ts.id);
                flat.push(ts);
                if !tried.contains(&flat) {
                    tried.insert(flat.clone());
                    if check_grid(&flat, sw) {
                        if flat.len() == tiles.len() {
                            break 'main;
                        }
                        continue 'main;
                    }
                    let ts = flat.pop().unwrap();
                    taken.remove(&ts.id);
                } else {
                    let ts = flat.pop().unwrap();
                    taken.remove(&ts.id);
                }
            }
        }
        // impossible to proceed with current arrangement
        let ts = flat.pop().unwrap();
        taken.remove(&ts.id);
    }

    let c_idxs = [0, sw - 1, tiles.len() - 1, tiles.len() - sw];

    //println!("{:?}", flat[c_idxs[0]]);
    //println!("{:?}", flat[c_idxs[1]]);
    //println!("{:?}", flat[c_idxs[2]]);
    //println!("{:?}", flat[c_idxs[3]]);

    //println!("{:?}", flat.iter().map(|ts| ts.id).collect::<Vec<_>>());

    c_idxs.iter().map(|&i| flat[i].id).product()
}

fn p1(tiles: Vec<(usize, Vec<Vec<char>>)>) -> usize {
    let tilesides: Vec<_> = tiles
        .iter()
        .map(|(id, raw)| TileSides::new(*id, raw))
        .collect();
    let mut side_to_ids: HashMap<String, HashSet<usize>> = HashMap::new();
    for ts in tilesides.iter() {
        for s in ts.all_sides_as_strings().into_iter() {
            let rs = s.chars().rev().collect::<String>();
            side_to_ids
                .entry(s)
                .and_modify(|ids| {
                    ids.insert(ts.id);
                })
                .or_insert(vec![ts.id].into_iter().collect());
            side_to_ids
                .entry(rs)
                .and_modify(|ids| {
                    ids.insert(ts.id);
                })
                .or_insert(vec![ts.id].into_iter().collect());
        }
    }
    let mut sidvec = side_to_ids
        .into_iter()
        .filter(|(s, ids)| ids.len() == 1)
        .map(|(s, ids)| ids.into_iter().collect::<Vec<_>>()[0])
        .collect::<Vec<_>>();
    sidvec.sort();
    let mut ctr = HashMap::new();
    for sv in sidvec.into_iter() {
        if !ctr.contains_key(&sv) {
            ctr.insert(sv, 0);
        }
        ctr.insert(sv, ctr.get(&sv).unwrap() + 1);
    }
    let corners = ctr
        .into_iter()
        .filter(|(_, ct)| *ct == 4)
        .map(|(id, _)| id)
        .collect::<Vec<_>>();

    corners.iter().product()
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let tiles = input
        .split("\n\n")
        .map(|t| {
            let mut ls = t.lines();
            let id = ls
                .next()
                .unwrap()
                .chars()
                .filter(|c| c.is_digit(10))
                .collect::<String>()
                .parse::<usize>()
                .unwrap();
            let tile = ls
                .map(|l| l.chars().collect::<Vec<_>>())
                .collect::<Vec<_>>();
            (id, tile)
        })
        .collect::<Vec<_>>();
    println!("tile len {}", tiles.len());
    println!("p1: {}", p1(tiles.clone()));
    //println!("p2: {}", p2(tiles));
}
