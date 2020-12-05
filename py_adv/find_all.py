import re

lines = []

while True:
    inpt = input()
    if inpt == '':
        break
    else:
        lines.append(inpt)

pattern = re.compile(r'<i>(.*?)</i>')
res = re.findall(pattern, ' '.join(lines))
res[:] = [x for x in res if x[-1] != ' ']
print(*res, sep='\n')
