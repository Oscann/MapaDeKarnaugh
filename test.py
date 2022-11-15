test = [1, 2, 3]
test2 = [4, 5, 6]
carlos = []

carlos.extend(test) if False else carlos.extend(test2)
josa = [x for x in range(6) if x in (test if False else test2)]

print(carlos)
print(josa)
