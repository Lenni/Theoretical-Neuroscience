# global imports
import numpy as np

def emp_mean_cov( samples ):
    n = len(samples)
    mean = np.sum( samples, axis=0 )/n
    cov_k = lambda x: [[ x[i]*x[j] for i in range(len(x))] for j in range(len(x)) ]
    cov = np.sum( np.array( list(map( cov_k, samples-mean )) ), axis=0 )/n
    return mean, cov

def theo_mean_cov( states, probs ):
    n = len(states)
    mean = np.sum( probs[:,None] * states, axis=0 )
    cov_k = lambda x: [[ x[i]*x[j] for i in range(len(x))] for j in range(len(x)) ]
    cov = np.sum( probs[:,None,None] * np.array( list(map( cov_k, states-mean )) ), axis=0 )
    return mean, cov


## define parameters
n = 1e5                                                       ## number of samples
states = np.array([ [0.,0.] , [0.,1.] , [1.,0.] , [1.,1.] ])  ## possible states
probs =  np.array([ 1.      , 1.      , 1.      , 2.    ] )   ## rel. probability of states
probs /= np.sum(probs)                                        ## normalisation

##########################################################################

## generate random samples from distribution
samples = []
for cs in range(int(n)):
    l = np.random.rand()
    i = 0
    while np.sum(probs[:i]) < l:
        i += 1
    samples += [states[i-1]]
samples = np.array(samples)

##########################################################################

## empirical statistics

means, cov = emp_mean_cov(samples)
mean_z1, mean_z2 = means
(var_z1, cov_z1z2), (_, var_z2) = cov

## theoretical statistics

means_theo, cov_theo = theo_mean_cov(states,probs)
mean_z1_theo, mean_z2_theo = means_theo
(var_z1_theo, cov_z1z2_theo), (_, var_z2_theo) = cov_theo

##########################################################################

## print the results
print("n = {:.1e}".format(n))
print()
print("              \t empirical \t theoretical")
print("Mean(z1)    : \t {:.4f}      \t {:.4f}       ".format(mean_z1, mean_z1_theo))
print("Mean(z2)    : \t {:.4f}      \t {:.4f}       ".format(mean_z2, mean_z2_theo))
print("Var(z1)     : \t {:.4f}      \t {:.4f}       ".format(var_z1, var_z1_theo))
print("Var(z2)     : \t {:.4f}      \t {:.4f}       ".format(var_z2, var_z2_theo))
print("Cov(z1,z2)  : \t {:.4f}      \t {:.4f}       ".format(cov_z1z2, cov_z1z2_theo))
