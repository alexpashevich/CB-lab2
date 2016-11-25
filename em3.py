import random
import math

n_A = 186
n_B = 38
n_AB = 13
n_O = 284
N = 521

def expectation(p_A, p_B, p_O):
    n_AA = n_A * p_A** 2 / (p_A**2 + 2*p_A*p_O)
    n_AO = n_A * (2*p_A*p_O) / (p_A**2 + 2*p_A*p_O)
    n_BB = n_B * p_B**2 / (p_B**2 + 2*p_B*p_O)
    n_BO = n_B * (2*p_B*p_O) / (p_B**2 + 2*p_B*p_O)
    return (n_AA, n_AO, n_BB, n_BO)

def maximization(n_AA, n_AO, n_BB, n_BO):
    p_A = (2*n_AA + n_AO + n_AB) / (2*N)
    p_B = (2*n_BB + n_BO + n_AB) / (2*N)
    p_O = (2*n_O + n_AO + n_BO) / (2*N)
    return (p_A, p_B, p_O)

def em(p_init, epsilon):
    p_A = p_init[0]
    p_B = p_init[1]
    p_O = p_init[2]
    old_p_A = float("inf")
    old_p_B = float("inf")
    old_p_O = float("inf")
    k = 0

    while math.sqrt((p_A - old_p_A) ** 2 + (p_B - old_p_B) ** 2 + (p_O - old_p_O) ** 2) > epsilon:
        # print 'iter %d, cur p = (%f,%f,%f)' % (k, p_A, p_B, p_O)

        (n_AA, n_AO, n_BB, n_BO) = expectation(p_A, p_B, p_O)
        (old_p_A, old_p_B, old_p_O) = (p_A, p_B, p_O)
        (p_A, p_B, p_O) = maximization(n_AA, n_AO, n_BB, n_BO)

        k += 1

    print 'estimated p = (%f,%f,%f)' % (p_A, p_B, p_O)

if __name__ == "__main__":
    epsilon = 0.000001
    for it in xrange(100):
        p_A = random.random()
        p_B = random.random() * (1 - p_A)
        p_O = 1 - p_A - p_B
        em((p_A, p_B, p_O), epsilon)

