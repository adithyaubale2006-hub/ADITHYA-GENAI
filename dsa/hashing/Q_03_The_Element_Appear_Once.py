#The element thst appear once
l = [2,2,1]
frq = {}
count = [[] for i in range(len(l))]

for i in l:
  frq[i] = frq.get(i, 0)+1
  
for i, c in frq.items():
  if c == 1:
    print(i)
