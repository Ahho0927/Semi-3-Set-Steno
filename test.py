from math import sqrt

r1 = int(input("r1 : "))
r2 = int(input("r2 : "))
max = int(sqrt(r1**2 + r2**2))
dot = [0, 0]
for n in range(max):
    dot[0] += int((-(n-1)+sqrt(2*r1**2 - (n-1)**2))/2 + ((n-1)+sqrt(2*r1**2 - (n-1)**2))/2)
    dot[1] += int((-(n-1)+sqrt(2*r2**2 - (n-1)**2))/2 + ((n-1)+sqrt(2*r2**2 - (n-1)**2))/2)

answer = 4*(dot[1] - dot[0]) -4*(r2-r1)
print(answer)