def modify_list(a):
    a[:] = [i / 2 for i in a if i % 2 == 0]
