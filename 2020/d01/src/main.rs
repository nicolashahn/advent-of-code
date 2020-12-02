use anyhow::{Error, Result};
use std::{collections::HashSet, fs};

fn p1(nums: &HashSet<i64>) -> Result<i64> {
    for &num in nums.iter() {
        if nums.contains(&(2020 - num)) {
            return Ok(num * (2020 - num));
        }
    }

    Err(Error::msg("no answer found for p1"))
}

fn p2(nums: &HashSet<i64>) -> Result<i64> {
    let numvec: Vec<&i64> = nums.iter().collect();
    for i in 0..nums.len() {
        for j in 0..nums.len() {
            let third = 2020 - numvec[i] - numvec[j];
            if nums.contains(&third) {
                return Ok(numvec[i] * numvec[j] * third);
            }
        }
    }

    Err(Error::msg("no answer found for p2"))
}

fn main() {
    let input = fs::read_to_string("./input").unwrap();
    let nums = input
        .split("\n")
        .filter(|&n| n != "")
        .map(|n| n.parse::<i64>().unwrap())
        .collect::<HashSet<_>>();

    println!("p1: {}", p1(&nums).unwrap());
    println!("p2: {}", p2(&nums).unwrap());
}
