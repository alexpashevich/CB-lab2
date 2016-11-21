import random
import math
import pickle
import sys
import numpy as np
import matplotlib.pyplot as plt
from itertools import chain

def calc_p_z(y, thetas_init):
    theta1 = thetas_init[0]
    theta2 = thetas_init[1]
    n = len(y)
    R = [1.]
    sum_R = R[0]

    for k in xrange(1, n):
        R.append(R[k - 1] * (theta1 / theta2) ** y[k] * ((1 - theta1) / (1 - theta2)) ** (1 - y[k]))
        sum_R += R[k]

    p_z = [0.]
    for k in range(0, n):
        p_z.append(R[k] / sum_R)

    return p_z



def find_interval(p_z, val):
    z = np.argmax(p_z)
    k = 0
    while sum(p_z[z - k: z + k]) < val:
        k += 1
    return (z - k, z + k)

def em(y, thetas_init, epsilon):
    theta1 = thetas_init[0]
    theta2 = thetas_init[1]
    old_theta1 = float("inf")
    old_theta2 = float("inf")
    n = len(y)
    k = 0

    sum_y = [0]
    for i in xrange(len(y)):
        sum_y.append(sum_y[i] + y[i])

    print sum_y

    while math.sqrt((theta1 - old_theta1) ** 2 + (theta2 - old_theta2) ** 2) > epsilon:
        print 'iter %d, cur theta = (%f,%f)' % (k, theta1, theta2)
        p_z = calc_p_z(y, (theta1, theta2)) # p_z[k] = p(z = k | y, thetas) so len(p_z) = n + 1, p_z[0] = undef

        (old_theta1, old_theta2) = (theta1, theta2)
        k += 1

        theta1 = np.sum([p_z[j] * sum_y[j - 1] for j in xrange(2, n + 1)]) / np.sum([p_z[j] * (j - 1) for j in xrange(2, n + 1)])
        theta2 = np.sum([p_z[j] * (sum_y[n] - sum_y[j-1]) for j in xrange(1, n + 1)]) / np.sum([p_z[j] * (n - j + 1) for j in xrange(1, n + 1)])

    plt.plot(p_z)
    plt.xlabel('z')
    plt.ylabel('p(z|y,theta)')
    plt.show()

    z = np.argmax(p_z)

    (z_l, z_u) = find_interval(p_z, 0.75)

    return (z, theta1, theta2, z_l, z_u)

if __name__ == "__main__":
    epsilon = 0.0001
    theta1_init = random.random()
    theta2_init = random.random()

    if sys.argv[1] == 'sequence.data':
        with open(sys.argv[1]) as f:
            y_2D = [[int(x) for x in line.split()] for line in f]
            y = list(chain.from_iterable(y_2D))
            (z, theta1, theta2, z_l, z_u) = em(y, (theta1_init, theta2_init), epsilon)
            print 'estimated z = %d, thetas = (%f,%f), (z_l, z_u) = (%d, %d)' % (z, theta1, theta2, z_l, z_u)
    else:
        with open(sys.argv[1], 'r') as f_y:
            y = pickle.load(f_y)
            (z, theta1, theta2, z_l, z_u) = em(y, (theta1_init, theta2_init), epsilon)
            print 'estimated z = %d, thetas = (%f,%f), (z_l, z_u) = (%d, %d)' % (z, theta1, theta2, z_l, z_u)

    


    
