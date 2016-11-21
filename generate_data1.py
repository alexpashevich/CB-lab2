import random
import pickle
import sys

if __name__ == "__main__":
    n = 321
    y = []
    theta1 = random.random()
    theta2 = random.random()
    z = random.randint(1, n)
    print 'generation with theta = (%f,%f), z = %d' % (theta1, theta2, z)
    for i in xrange(n):
        if i < z:
            if random.random() < theta1:
                y.append(1)
            else:
                y.append(0)
        else:
            if random.random() < theta2:
                y.append(1)
            else:
                y.append(0)

    with open(sys.argv[1], 'w') as f_y:
        pickle.dump(y, f_y)
