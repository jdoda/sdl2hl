
def get_mask(items):
    return reduce(lambda x, y : x | y, items, 0)

def get_items(enum, mask, blacklist=frozenset()):
    items = set()
    for item in enum:
        if item not in blacklist and item & mask:
            items.add(item)
    return items
