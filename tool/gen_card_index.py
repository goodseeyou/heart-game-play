import Card

cii = {}
for i in Card.SUIT_VALUE_DICT:
    for j in Card.SUIT_INDEX_DICT:
        card_string = '%s%s' % (i, j)
        ii = Card.Card(card_string).instance_index
        cii[card_string] = ii

_t = []
for k in cii:
    v = cii[k]
    _t.append((k, v))
print sorted(_t, key=lambda x: x[1])

print cii
