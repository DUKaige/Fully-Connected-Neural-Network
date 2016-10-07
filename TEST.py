__author__ = 'liukaige'
import math
summ = 0
for i in range(0,201):
    summ += (math.atan(-2.296 + 0.01148*i )- 2.12)**2 #* 0.01148/2
#summ -= (math.atan(-2.296) - 2.12)**2 + (math.atan(0) - 2.12)**2 * 0.01148/2
print summ