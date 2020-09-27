from itertools import product, permutations, combinations, combinations_with_replacement

print("Consider the selection of k items from n option. Let k = 2, n = 3, options: a, b, c")

print("Tuples: ")
for c in product("abc", repeat=2):
    print("".join(c))
 
print("Permutations: ")
for c in permutations("abc", 2):
    print("".join(c))

print("ombinations: ")
for c in combinations("abc", 2):
    print("".join(c))

for c in combinations_with_replacement("abc", 2):
    print("".join(c))
 