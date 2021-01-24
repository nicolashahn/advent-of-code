use std::cell::RefCell;
use std::collections::HashMap;
use std::fmt;
use std::rc::Rc;

struct Node {
    val: u32,
    next: Option<Rc<RefCell<Node>>>,
}

impl fmt::Debug for Node {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.debug_struct("Node")
            .field("val", &self.val)
            .field("next", &self.next.as_ref().map(|rc| (*rc).borrow().val))
            .finish()
    }
}

fn play_game(input: Vec<u32>, steps: usize) -> HashMap<u32, Rc<RefCell<Node>>> {
    let len = input.len();
    let mut curr_val = input[0];
    let nodes = input
        .into_iter()
        .map(|val| Rc::new(RefCell::new(Node { val, next: None })))
        .collect::<Vec<_>>();

    for i in 0..len - 1 {
        let next = Some(nodes[i + 1].clone());
        (*nodes[i]).borrow_mut().next = next;
    }
    let next = Some(nodes[0].clone());
    (*nodes[len - 1]).borrow_mut().next = next;

    let dict: HashMap<u32, Rc<RefCell<Node>>> = nodes
        .into_iter()
        .map(|node| ((*node).borrow().val, node.clone()))
        .collect::<HashMap<_, _>>();

    let mut set = vec![];
    // do cup game
    for _ in 0..steps {
        let curr = dict.get(&curr_val).unwrap();

        // chop out next 3 cups
        let head_of_3 = curr.borrow().next.clone().unwrap();
        let mut next = head_of_3.clone();
        let mut last_of_3 = None;
        set.clear();
        for i in 0..3 {
            if i == 2 {
                last_of_3 = Some(next.clone());
            }
            set.push(next.borrow().val.clone());
            let next_next = next.borrow().next.clone().unwrap();
            next = next_next;
        }
        (*curr).borrow_mut().next = Some(next.clone());

        // find next "current" cup
        let mut dest_val = if curr_val != 1 {
            curr_val - 1
        } else {
            len as u32
        };
        while set.contains(&dest_val) {
            dest_val -= 1;
            if dest_val == 0 {
                dest_val = len as u32;
            }
        }

        // splice next 3 back into list
        let dest = dict.get(&dest_val).unwrap();
        last_of_3.unwrap().borrow_mut().next = Some(dest.borrow().next.clone().unwrap());
        dest.borrow_mut().next = Some(head_of_3);

        curr_val = curr.borrow().next.clone().unwrap().borrow().val;
    }

    dict
}

fn p1(input: Vec<u32>, steps: usize) -> Vec<u32> {
    let len = input.len();
    let dict = play_game(input, steps);
    let mut head = dict.get(&1).unwrap().borrow().next.clone().unwrap();
    let mut res = vec![];
    for _ in 0..len - 1 {
        res.push(head.borrow().val);
        let next = head.borrow().next.clone().unwrap();
        head = next;
    }

    res
}

fn p2(input: Vec<u32>, steps: usize) -> u64 {
    let dict = play_game(input, steps);
    let next = dict.get(&1).unwrap().borrow().next.clone().unwrap();
    let next_next = next.borrow().next.clone().unwrap();
    let next_val = next.borrow().val;
    let next_next_val = next_next.borrow().val;

    next_val as u64 * next_next_val as u64
}

fn main() {
    //let input = "389125467"
    let input = "853192647"
        .chars()
        .map(|c| c.to_digit(10).unwrap())
        .collect();

    println!(
        "p1: {}",
        p1(input, 100)
            .iter()
            .map(|n| n.to_string())
            .collect::<Vec<_>>()
            .join("")
    );

    let mut input2: Vec<u32> = "853192647"
        .chars()
        .map(|c| c.to_digit(10).unwrap())
        .collect();
    input2.extend(10..=1_000_000);

    println!("p2: {}", p2(input2, 10_000_000));
}
