def parse_entry(entry):
    lines = entry.split()
    H, W = [int(x) for x in lines[:2]]

    return H, W, [list(line) for line in lines[2:]]

def build_output(matrix, agent, obj_pos):
    out = '\n'
    ag_x = agent['pos']['x']
    ag_y = agent['pos']['y']
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if x == ag_x and y == ag_y:
                out += agent['dir']
            elif x == obj_pos['x'] and y == obj_pos['y']:
                out += 'x'
            else:
                out += matrix[y][x]
        out += '\n'
    return out

