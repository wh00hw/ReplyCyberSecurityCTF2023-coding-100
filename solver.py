from constraint import Problem, ExactSumConstraint, FunctionConstraint, RecursiveBacktrackingSolver
from pathlib import Path
import string
import pyzipper

class FuncExactValueHolder:
    def __init__(self, value):
        self.value = value
    
    def mul(self, *args):
        prod = 1
        for x in args:
            prod *= x
        return prod == self.value
    
    def sub(self, *args):
        x = args[0]
        y = args[1]
        if x > y:
            return x - y == self.value
        else:
            return y - x == self.value
        
    def div(self, *args):
        x = args[0]
        y = args[1]
        if x > y:
            return x / y == self.value
        else:
            return y / x == self.value
        
def solve(size, region_constraints, regions_indexes):
    problem = Problem(RecursiveBacktrackingSolver())

    for r in range(size):
        for c in range(size):
            problem.addVariable(f"n_{r}_{c}", range(1,size+1))
    
    for r in range(size):
        for c in range(size):
            mrc = f"n_{r}_{c}"
            for i in range(size):
                if i > r:
                    problem.addConstraint(lambda x, y: x != y, (mrc, f"n_{i}_{c}"))
                if i > c:
                    problem.addConstraint(lambda x, y: x != y, (mrc, f"n_{r}_{i}"))

    for region in regions_indexes.keys():
        c = region_constraints[string.ascii_lowercase.index(region)]
        if c[2] == "+":
            problem.addConstraint(ExactSumConstraint(int(c[1])), tuple(f"n_{pos[0]}_{pos[1]}" for pos in regions_indexes[region]))
        if c[2] == "*":
            problem.addConstraint(FunctionConstraint(FuncExactValueHolder(value=int(c[1])).mul), tuple(f"n_{pos[0]}_{pos[1]}" for pos in regions_indexes[region]))
        if c[2] == "-":
            problem.addConstraint(FunctionConstraint(FuncExactValueHolder(value=int(c[1])).sub), tuple(f"n_{pos[0]}_{pos[1]}" for pos in regions_indexes[region]))
        if c[2] == "/":
            problem.addConstraint(FunctionConstraint(FuncExactValueHolder(value=int(c[1])).div), tuple(f"n_{pos[0]}_{pos[1]}" for pos in regions_indexes[region]))
    
    solutions = problem.getSolution()
    passwords = []
    if solutions:
        return "".join([str(solutions[f"n_{r}_{c}"]) for r in range(size) for c in range(size)])
    return passwords


if __name__ == "__main__":
    level = 1
    out_dir = "solutions"
    flag = Path(f"{out_dir}/flag.txt")
    with pyzipper.AESZipFile("coding-100.zip") as zf:
        zf.extractall(path=out_dir)
    with pyzipper.AESZipFile(f"{out_dir}/challenge.zip") as zf:
        zf.extractall(path=out_dir)
    while True:
        regions = []
        level_filename = f"{out_dir}/lvl_{level}"
        with open(level_filename+".txt") as f:
            print(f"Solving problem {level}")
            region_constraints = []
            lines = f.readlines()
            data = regions
            for line in lines:
                if line[0] == "\n":
                    data = region_constraints
                    continue
                data.append(line.strip().split(" "))
        regions_indexes = {}
        for i, rows in enumerate(regions):
            for j, letter in enumerate(rows):
                if not regions_indexes.get(letter):
                    regions_indexes[letter] = list()
                regions_indexes[letter].append((i, j))
        
        password = solve(len(regions), region_constraints, regions_indexes)
        if password:
            try:
                with pyzipper.AESZipFile(level_filename+".zip") as zf:
                    zf.extractall(pwd=password.encode('utf-8'), path=out_dir)  # Decode the password to bytes
                print("Successfully extracted the zip file.")
                if flag.is_file():
                    with open(str(flag)) as f:
                        print(f"Flag: {f.read()}")
                        break
                level +=1
            except Exception as e:
                print(f"Failed to extract the zip file: {str(e)}")
                break