list1 = "['list', 'set', 'tuple']"
list2 = list(list1.split(","))
for x in list2:
    x = x.replace("'", '')
    x = x.replace('[', '')
    x = x.replace(']', '')
    