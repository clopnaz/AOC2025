use std::fs;

fn main() {
    // file_path = "input.txt";
    let lines: Vec<String> = fs::read_to_string("input.txt")
        .expect("Failed to read input.txt")
        .lines()
        .map(|line| {
            let r_or_l = line.chars().next().unwrap();
            match r_or_l {
                'R' => 

    println!("{lines:#?}");
}
