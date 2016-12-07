import random
import math
import pickle
import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
from itertools import chain
from scipy import ndimage

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

    while math.sqrt((theta1 - old_theta1) ** 2 + (theta2 - old_theta2) ** 2) > epsilon:
        print 'iter %d, cur theta = (%f,%f)' % (k, theta1, theta2)
        p_z = calc_p_z(y, (theta1, theta2)) # p_z[k] = p(z = k | y, thetas) so len(p_z) = n + 1, p_z[0] = undef

        (old_theta1, old_theta2) = (theta1, theta2)
        k += 1

        theta1 = np.sum([p_z[j] * sum_y[j - 1] for j in xrange(2, n + 1)]) / np.sum([p_z[j] * (j - 1) for j in xrange(2, n + 1)])
        theta2 = np.sum([p_z[j] * (sum_y[n] - sum_y[j-1]) for j in xrange(1, n + 1)]) / np.sum([p_z[j] * (n - j + 1) for j in xrange(1, n + 1)])

    # plt.hist(p_z_hist, nb_bins, normed=True)
    plt.bar(range(n), p_z[1:])
    plt.xlabel('z - 70')
    plt.ylabel('p(z|y,theta)')
    plt.show()

    z = np.argmax(p_z)

    (z_l, z_u) = find_interval(p_z, 0.75)

    return (z, theta1, theta2, z_l, z_u, p_z)

if __name__ == "__main__":
    epsilon = 0.0001
    theta1_init = random.random()
    theta2_init = random.random()
    markers_on = [120,260]

    if sys.argv[1] == 'sequence.data':
        with open(sys.argv[1]) as f:
            y_2D = [[int(x) for x in line.split()] for line in f]
            y = list(chain.from_iterable(y_2D))
            plt.plot(y)
            plt.show()
            # if len(sys.argv) == 2:

            first_val = 140
            second_val = 70

            (z1, theta1, theta2, z_l, z_u, p_z) = em(y[:first_val], (theta1_init, theta2_init), epsilon)
            print 'estimated z = %d, thetas = (%f,%f), (z_l, z_u) = (%d, %d)' % (z1, theta1, theta2, z_l, z_u)

            (z2, theta1, theta2, z_l, z_u, p_z) = em(y[second_val:], (theta1_init, theta2_init), epsilon)
            print 'estimated z = %d, thetas = (%f,%f), (z_l, z_u) = (%d, %d)' % (z2 + second_val, theta1, theta2, z_l + second_val, z_u + second_val)

            markers_on = [z1, second_val + z2]

            # else:
                # summation = np.zeros(len(y))
                # stride = 10
                # len_sub = 100
                # for i in xrange((len(y) - len_sub) / stride):
                #     (z, theta1, theta2, z_l, z_u, p_z) = em(y[i * stride:i * stride + len_sub], (theta1_init, theta2_init), epsilon)
                #     # print len(y)
                #     # print len(p_z)
                #     # print summation.shape
                #     # print summation[i * stride:i * stride + len_sub].shape
                #     summation[i * stride:i * stride + len_sub] += p_z[1:]
                #     print 'y[%d:%d]: estimated z = %d, thetas = (%f,%f), (z_l, z_u) = (%d, %d)' % \
                #                         (i * stride, i * stride + len_sub, z, theta1, theta2, z_l, z_u)
                # y_foat = np.asarray(y, dtype=np.float32)
                # gaus = ndimage.filters.gaussian_filter1d(y_foat, 10)
                # plt.plot(gaus)
                # plt.show()
            
    else:
        with open(sys.argv[1], 'r') as f_y:
            # df = pd.read_csv(sys.argv[1], header=None)
            # print df
            # print вы
            # y = list(df)
            # plt.plot(y)
            # plt.show()
            # print y
            # theta1_init = 0.8
            # theta1_init = 0.65
            y = pickle.load(f_y)
            (z, theta1, theta2, z_l, z_u, p_z) = em(y, (theta1_init, theta2_init), epsilon)
            print 'estimated z = %d, thetas = (%f,%f), (z_l, z_u) = (%d, %d)' % (z, theta1, theta2, z_l, z_u)

    y_foat = np.asarray(y, dtype=np.float32)
    gaus = ndimage.filters.gaussian_filter1d(y_foat, 10)
    plt.plot(gaus, '-gD', markevery=markers_on)
    plt.xlabel('y')
    plt.ylabel('Gauss(y)')
    plt.show()


    
