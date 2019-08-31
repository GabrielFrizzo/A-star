def parse_entry(entry):
    lines = entry.split()
    H, W = [int(x) for x in lines[:2]]

    return H, W, [list(line) for line in lines[2:]]

def build_output(maze):
    return '\n'.join([''.join(line) for line in maze])

