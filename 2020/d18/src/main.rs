use crate::Node::{List, Op, Val};
use crate::Operation::{Add, Mul};

#[derive(Eq, PartialEq, Debug, Clone)]
enum Node {
    List(Vec<Node>),
    Op(Operation),
    Val(i64),
}

#[derive(Eq, PartialEq, Debug, Clone)]
enum Operation {
    Add,
    Mul,
}

fn to_node(mut toks: &mut Vec<&str>) -> Node {
    let mut nodes = vec![];
    while !toks.is_empty() {
        let c = toks.remove(0);
        match c {
            "(" => nodes.push(to_node(&mut toks)),
            ")" => return List(nodes),
            "*" => nodes.push(Op(Mul)),
            "+" => nodes.push(Op(Add)),
            val => nodes.push(Val(val.parse().unwrap())),
        }
    }

    List(nodes)
}

fn eval(node: &Node) -> i64 {
    match node {
        Op(_) => panic!("can't eval just an operator"),
        Val(v) => *v,
        List(nodes) => {
            let mut iter = nodes.iter().peekable();
            let mut left = eval(iter.next().unwrap());
            while iter.peek().is_some() {
                let op = iter.next().unwrap();
                let right = eval(iter.next().unwrap());
                left = match op {
                    Op(Add) => left + right,
                    Op(Mul) => left * right,
                    _ => panic!("didn't get an operator where I expected it"),
                }
            }

            left
        }
    }
}

fn p1(nodes: Vec<Node>) -> i64 {
    nodes.iter().map(eval).sum()
}

fn eval2(node: &Node) -> i64 {
    match node {
        Op(_) => panic!("can't eval just an operator"),
        Val(v) => *v,
        List(nodes) => {
            // go through list and eval additions, any multiplication operations get added to a new
            // list of nodes and will get evaluated later
            // e.g. (8 * 4 + 1 * 3) -> (8 * 5 * 3)
            let mut new_nodes = vec![];
            let mut iter = nodes.iter().peekable();
            let mut left = eval2(iter.next().unwrap());
            while iter.peek().is_some() {
                let op = iter.next().unwrap();
                let right = eval2(iter.next().unwrap());
                left = match op {
                    Op(Add) => left + right,
                    Op(Mul) => {
                        new_nodes.push(Val(left));
                        new_nodes.push(Op(Mul));
                        right
                    }
                    _ => panic!("didn't get an operator where I expected it"),
                };
            }
            new_nodes.push(Val(left));

            if new_nodes.is_empty() {
                // there were no multiplication operators
                return left;
            }

            // here is where the multiplications get evaluated
            let mut iter = new_nodes.iter().peekable();
            let mut left = eval(iter.next().unwrap());
            while iter.peek().is_some() {
                let op = iter.next().unwrap();
                let right = eval(iter.next().unwrap());
                left = match op {
                    Op(Add) => panic!("shouldn't be any '+'s left"),
                    Op(Mul) => left * right,
                    _ => panic!("didn't get an operator where I expected it"),
                }
            }

            left
        }
    }
}

fn p2(nodes: Vec<Node>) -> i64 {
    nodes.iter().map(eval2).sum()
}

fn main() {
    let input = std::fs::read_to_string("./input").unwrap();
    let nodes = input
        .lines()
        .map(|line| {
            to_node(
                &mut line
                    // so that we can parse each whitespace-separated string of characters as a
                    // separate token instead of being smarter about parsing
                    .replace("(", " ( ")
                    .replace(")", " ) ")
                    .split(" ")
                    .filter(|t| t.len() > 0)
                    .collect::<Vec<_>>(),
            )
        })
        .collect::<Vec<_>>();
    println!("p1: {}", p1(nodes.clone()));
    println!("p2: {}", p2(nodes));
}
