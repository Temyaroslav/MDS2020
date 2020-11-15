def logical_xor(t):
	return t[0] ^ t[1]

inpt1 = input().split()
inpt1 = list(map(int, inpt1))
inpt2 = input().split()
inpt2 = list(map(int, inpt2))

res = map(logical_xor, zip(inpt1, inpt2))

print(' '.join(map(str, res)))
