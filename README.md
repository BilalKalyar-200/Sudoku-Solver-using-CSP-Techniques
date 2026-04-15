# Sudoku-Solver-using-CSP-Techniques
```markdown
# 🧩 Sudoku Solver using CSP

This project implements a Sudoku solver using **Constraint Satisfaction Problem (CSP)** techniques.  
It efficiently solves Sudoku puzzles of varying difficulty using AI-based methods.

---

## 🚀 Features

- Solves 9×9 Sudoku puzzles
- Uses CSP techniques:
  - Backtracking Search
  - Forward Checking
  - AC-3 Algorithm
- Handles puzzles from easy to very difficult (evil)
- Tracks performance:
  - Number of backtracking calls
  - Number of failures

---

## 📂 Input Format

- Input is read from `.txt` files
- Each file must contain:
  - 9 lines
  - Each line has 9 digits (0–9)
  - `0` represents empty cells

### Example:
```

004030050
609400000
005100489
...

```

---

## ▶️ How to Run

1. Place puzzle files in the same directory:
   - `easy.txt`
   - `medium.txt`
   - `hard.txt`
   - `evil.txt`

2. Run the program:
```

python sudoku_solver.py

```

3. The solver will:
   - Display the puzzle
   - Print the solved Sudoku
   - Show backtracking statistics

---

## 📊 Output

For each puzzle, the program prints:
- Given Sudoku board
- Final solved board
- Backtracking calls
- Backtracking failures

---

## 🧠 Techniques Used

- **Backtracking**: Searches for valid assignments
- **Forward Checking**: Reduces domains early
- **AC-3**: Ensures arc consistency before search

---

## 📎 Repository Contents

- `solver.py` → Main implementation  
- `easy.txt`, `medium.txt`, `hard.txt`, `evil.txt` → Input puzzles  
- `report.pdf` → Project report  
