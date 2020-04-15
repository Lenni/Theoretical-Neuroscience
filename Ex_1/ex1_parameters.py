# Parameter file for Brunel2000 simulation

# Simulation parameters

dt      = 0.1    # the resolution in ms
simtime = 1000.0 # Simulation time in ms

# Network parameters

NE        = 4000 # Number of excitatory neurons
NI        = 1000 # Number of inhibitory neurons
N_rec     = 50 # Number of recorded neurons 
epsilon   = 0.1  # Connection probability
CE        = int(epsilon*NE) # number of excitatory synapses per neuron
CI        = int(epsilon*NI) # number of inhibitory synapses per neuron  

# Neuron parameters

# Threshold
I_ext = 375
# Subthreshold
I_ext = 0.9*375
# Superthreshold
I_ext = 1.1*375

neuron_params = {
    'C_m': 250.0, # (pF)
    'E_L': 0., # (mV)
    'I_e': 0.0, # (pA)
    'V_m': 0., # (mV)
    'V_reset': 0., # (mV)
    'V_th': 15., # (mV)
    't_ref': 2.0, # (ms)
    'tau_m': 10.0, # (ms)
}


# Synapse parameters
d = 1.5 # Delay
J = 0.1 # Synaptic weight in mV
g = 6.1 # ratio of inhibitory to excitatory weight

# External poisson rate in Hz 
#nu_ext = 0000.
# Threshold
#nu_ext = 15000.
# Sup threshold
#nu_ext = 16000.
