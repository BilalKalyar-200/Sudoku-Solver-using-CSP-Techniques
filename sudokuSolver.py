import os

#global counters for tracking
bt_calls = 0
bt_fails = 0


#file reading
def load_sudoku(file_name):
    grid = []
    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            if line != "":
                row_vals = []
                for ch in line:
                    row_vals.append(int(ch))
                grid.append(row_vals)
    return grid


def show_grid(grid):
    for i in range(9):
        if i == 3 or i == 6:
            print("------+-------+------")

        line = ""
        for j in range(9):
            if j == 3 or j == 6:
                line += "| "
            line += str(grid[i][j]) + " "
        print(line)
    print()

def make_domains(grid):
    dom = {}

    for i in range(9):
        for j in range(9):

            if grid[i][j] != 0:
                #already filled so only one value possible
                dom[(i, j)] = {grid[i][j]}
            else:
                #empty so all values possible in start
                possible = set()
                for v in range(1, 10):
                    possible.add(v)
                dom[(i, j)] = possible

    return dom

def find_neighbours(r, c):
    neigh = set()

    #row check
    for x in range(9):
        if x != c:
            neigh.add((r, x))

    #column check
    for x in range(9):
        if x != r:
            neigh.add((x, c))

    #box check
    start_r = (r // 3) * 3
    start_c = (c // 3) * 3

    for i in range(start_r, start_r + 3):
        for j in range(start_c, start_c + 3):
            if (i, j) != (r, c):
                neigh.add((i, j))

    return neigh


def run_ac3(dom):
    queue = []

    # make all arcs
    for var in dom:
        for nb in find_neighbours(var[0], var[1]):
            queue.append((var, nb))

    while len(queue) > 0:
        (a, b) = queue.pop(0)

        if make_consistent(dom, a, b):
            if len(dom[a]) == 0:
                return False  #domain finished -> no solution

            for k in find_neighbours(a[0], a[1]):
                if k != b:
                    queue.append((k, a))

    return True


def make_consistent(dom, xi, xj):
    changed = False

    #we copy because we may remove during loop
    for val in list(dom[xi]):
        #if xj has only same value then conflict
        if dom[xj] == {val}:
            dom[xi].remove(val)
            changed = True

    return changed


def pick_variable(dom, assigned):
    chosen = None
    smallest = 100  # big number

    for cell in dom:
        if cell not in assigned:
            size = len(dom[cell])
            if size < smallest:
                smallest = size
                chosen = cell

    return chosen


#forward checking
def do_forward(dom, assigned, cell, val):
    removed = []

    for nb in find_neighbours(cell[0], cell[1]):
        if nb not in assigned:
            if val in dom[nb]:
                dom[nb].remove(val)
                removed.append((nb, val))

                # if empty domain -> failure
                if len(dom[nb]) == 0:
                    return False, removed

    return True, removed


def restore(dom, removed):
    for (c, v) in removed:
        dom[c].add(v)


#backtracking
def solve_bt(dom, assigned):
    global bt_calls, bt_fails

    bt_calls += 1

    #if all filled
    if len(assigned) == 81:
        return assigned

    var = pick_variable(dom, assigned)

    #try all values
    for v in list(dom[var]):
        assigned[var] = v
        old_domain = set(dom[var])
        dom[var] = {v}

        ok, removed = do_forward(dom, assigned, var, v)

        if ok:
            res = solve_bt(dom, assigned)
            if res is not None:
                return res

        #undo changes (very important step)
        restore(dom, removed)
        dom[var] = old_domain
        del assigned[var]

    #if all values fail
    bt_fails += 1
    return None

def run_solver(file_name):
    global bt_calls, bt_fails
    bt_calls = 0
    bt_fails = 0

    print("Solving file:", os.path.basename(file_name))

    grid = load_sudoku(file_name)

    print("given puzzle:")
    show_grid(grid)

    dom = make_domains(grid)

    #first apply AC3
    if not run_ac3(dom):
        print("no solution after ac3\n")
        return

    assigned = {}

    #fill already fixed values
    for c in dom:
        if len(dom[c]) == 1:
            assigned[c] = list(dom[c])[0]

    result = solve_bt(dom, assigned)

    if result is None:
        print("solution not found\n")
    else:
        final = [[0 for _ in range(9)] for _ in range(9)]

        for (r, c), val in result.items():
            final[r][c] = val

        print("final answer:")
        show_grid(final)

    print("bt calls:", bt_calls)
    print("bt fails:", bt_fails)
    print()


if __name__ == "__main__":
    import os

    base = os.getcwd()

    files = ["easy.txt", "medium.txt", "hard.txt", "evil.txt"]

    for f in files:
        path = os.path.join(base, f)
        try:
            run_solver(path)
        except:
            print("file missing:", f)
