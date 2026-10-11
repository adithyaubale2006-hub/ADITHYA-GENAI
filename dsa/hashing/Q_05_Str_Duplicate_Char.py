l = "pyhton"
count = {}
duplicates = False

for i in l:
  if i in count:
    duplicates = True
    break
  
  count[i] = 1 
  
print(duplicates)
