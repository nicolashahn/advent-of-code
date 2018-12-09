def get_nodes(nums):
    childs = []
    metas = []
    num_childs = nums.pop(0)
    num_metas = nums.pop(0)
    for c in range(num_childs):
        childs.append(get_nodes(nums))
    for m in range(num_metas):
        metas.append(nums.pop(0))
    return {'childs': childs, 'metas': metas}

def total_metas(node):
    total = sum(node['metas'])
    for child in node['childs']:
        total += total_metas(child)
    return total

def value(node):
    if not node['childs']:
        return sum(node['metas'])
    else:
        total = 0
        childs = node['childs']
        for meta in node['metas']:
            if meta in range(1,len(childs)+1):
                total += value(childs[meta-1])
        return total

with open('in.txt', 'r') as f:
    nums = [int(n) for n in f.read().split()]
    node = get_nodes(nums)
    # Part 1
    print(total_metas(node))
    # Part 2
    print(value(node))
