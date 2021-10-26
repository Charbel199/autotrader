from collections import deque

l = [{'value': 'cars', 'blah': 2},
     {'value': 'cars', 'blah': 3},
     {'value': 'cars', 'blah': 4}]

test = [d.get('value', 'blah') for d in l]
print(len(test))
print(test)
