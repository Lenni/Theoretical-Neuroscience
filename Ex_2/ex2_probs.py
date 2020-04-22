# global imports
import numpy as np

## define parameters
n = 1e5                                                       ## number of samples
states = np.array([ [0.,0.] , [0.,1.] , [1.,0.] , [1.,1.] ])  ## possible states
probs =  np.array([ 1.      , 1.      , 1.      , 2.    ] )   ## rel. probability of states
probs /= np.sum(probs)                                        ## normalisation

##########################################################################

## generate random samples from distribution
samples = []
for cs in xrange(int(n)):
    l = np.random.rand()
    i = 0
    while np.sum(probs[:i]) < l:
        i += 1
    samples += [states[i-1]]
samples = np.array(samples)

##########################################################################

## empirical statistics

# YOUR CODE HERE

## theoretical statistics

# YOUR CODE HERE

##########################################################################

## print the results
print
print "              \t empirical \t theoretical"
print "Mean(z1)    : \t %.4f      \t %.4f       " % (mean_z1, mean_z1_theo)
print "Mean(z2)    : \t %.4f      \t %.4f       " % (mean_z2, mean_z2_theo)
print "Var(z1)     : \t %.4f      \t %.4f       " % (var_z1, var_z1_theo)
print "Var(z2)     : \t %.4f      \t %.4f       " % (var_z2, var_z2_theo)
print "Cov(z1,z2)  : \t %.4f      \t %.4f       " % (cov_z1z2, cov_z1z2_theo)