def read():
    with open("in.txt") as f:
        content = [x.strip() for x in f.readlines()]

    parents = {}
    inv_parents = {}

    [n, m] = content[0].split(" ")
    n, m = int(n), int(m)

    for i in range(1, n + 1):
        nodes = content[i].split(" ")
        parents[nodes[0]] = []
        inv_parents[nodes[0]] = inv_parents.get(nodes[0], [])
        for j in range(1, len(nodes)):
            parents[nodes[0]].append(nodes[j])
            inv_parents[nodes[j]] = inv_parents.get(nodes[j], [])
            inv_parents[nodes[j]].append(nodes[0])

    return n, m, parents, inv_parents, content


def dfs(node, X, Y, curr_path, p, inv_p):
    curr_path = curr_path.copy()
    curr_path.append(node)

    if node in Y:
        return [curr_path]

    result = []

    for v in p[node]:
        if v not in curr_path and not v in X:
            result.extend(dfs(v, X, Y, curr_path, p, inv_p))

    for v in inv_p[node]:
        if v not in curr_path and not v in X:
            result.extend(dfs(v, X, Y, curr_path, p, inv_p))

    return result


def path_active_given_z(path, parents, Z):
    for i in range(len(path) - 2):
        prev = path[i]
        curr = path[i + 1]
        next = path[i + 2]

        active_causal = False
        active_evidential = False
        active_cause = False
        active_effect = False

        if prev in parents[curr] and curr in parents[next] and curr not in Z:
            active_causal = True
        if curr in parents[prev] and next in parents[curr] and curr not in Z:
            active_evidential = True
        if curr in parents[prev] and curr in parents[next] and curr not in Z:
            active_cause = True
        if prev in parents[curr] and next in parents[curr] and curr in Z:
            active_effect = True

        if not active_causal and not active_evidential and not active_cause and not active_effect:
            return False

    return True


def run_inferences(n, m, parents, inv_parents, content):
    for i in range(n + 1, n + m + 1):
        [X, Y_Z] = content[i].split(';')
        X = list(filter(None, X.split(' ')))
        [Y, Z] = Y_Z.split('|')
        Y = list(filter(None, Y.split(' ')))
        Z = list(filter(None, Z.split(' ')))

        a_to_b_paths = []
        for x in X:
            a_to_b_paths.extend(dfs(x, X, Y, [], parents, inv_parents))

        is_active = False
        for path in a_to_b_paths:
            if path_active_given_z(path, parents, Z):
                is_active = True
                break
        if is_active:
            print("false")
        else:
            print("true")


if __name__ == "__main__":
    n, m, parents, inv_parents, content = read()
    run_inferences(n, m, parents, inv_parents, content)
