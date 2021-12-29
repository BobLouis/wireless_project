
# path Loss = 32.45 + 20log(f(MHz))+20log(d(km))
from math import log


def path_loss(a, b, f):
    #f in Mhz
    x1 = a[0]
    y1 = a[1]
    x2 = b[0]
    y2 = b[1]
    dis = ((((x2 - x1)**2) + ((y2-y1)**2))**0.5)*0.01
    return 87.55 - 20*log(f, 10) - 20*log(dis, 10)


base_list = [(125, 2385), (625, 1365), (1125, 135), (1365, 1125),
             (1635, 125), (1625, 615), (1875, 2135), (2125, 2135)]

loss_list = []

for b in base_list:
    loss_list.append(
        round(path_loss((0, 0), b, base_list.index(b)*100+100), 2))

print(loss_list)
val = max(loss_list)
print(loss_list.index(val))
