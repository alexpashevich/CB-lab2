import random
import pickle
import sys

if __name__ == "__main__":
    n = 321
    y = []
    theta1 = float(sys.argv[2])
    theta2 = float(sys.argv[3])
    theta3 = float(sys.argv[4])
    z1 = int(sys.argv[5])
    z2 = int(sys.argv[6])
    print 'generation with theta = (%f,%f,%f), z = (%d,%d)' % (theta1, theta2, theta3, z1, z2)
    for i in xrange(n):
        if i < z1:
            if random.random() < theta1:
                y.append(1)
            else:
                y.append(0)
        elif i < z2:
            if random.random() < theta2:
                y.append(1)
            else:
                y.append(0)
        else:
            if random.random() < theta3:
                y.append(1)
            else:
                y.append(0)

    with open(sys.argv[1], 'w') as f_y:
        pickle.dump(y, f_y)
