def distance(a, b):
    x1 = a[0]
    y1 = a[1]
    x2 = b[0]
    y2 = b[1]
    return ((((x2 - x1)**2) + ((y2-y1)**2))**0.5)


base_list = [(125, 2385), (625, 1365), (1125, 135), (1365, 1125),
             (1635, 125), (1625, 615), (1875, 2135), (2125, 2135)]

dis_list = []

for b in base_list:
    dis_list.append(round(distance((0, 0), b), 2))

print(dis_list)
val = min(dis_list)
print(dis_list.index(val))
