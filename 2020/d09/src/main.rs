fn p1(nums: &[usize]) -> usize {
    'outer: for window in nums.windows(26) {
        let last = window[25];
        for x in 0..24 {
            for y in x..25 {
                if window[x] + window[y] == last {
                    continue 'outer;
                }
            }
        }
        return last;
    }
    panic!("no soln")
}

fn p2(nums: &[usize], p1_ans: usize) -> usize {
    let n = nums.len();
    for x in 0..(n - 1) {
        let mut sum = nums[x];
        let mut min = sum;
        let mut max = sum;
        for y in (x + 1)..n {
            min = usize::min(min, nums[y]);
            max = usize::max(max, nums[y]);
            sum += nums[y];
            if sum == p1_ans {
                return min + max;
            }
            if sum > p1_ans {
                break;
            }
        }
    }
    panic!("no soln")
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let nums: Vec<_> = input.lines().map(|n| n.parse::<usize>().unwrap()).collect();
    let p1_ans = p1(&nums.clone());
    println!("p1: {}", p1_ans);
    println!("p2: {}", p2(&nums, p1_ans));
}
