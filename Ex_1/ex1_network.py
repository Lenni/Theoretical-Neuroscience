# global imports
import time
import matplotlib.pylab as plt

# local imports
from ex1_parameters import *

# import simulator
import nest
import nest.raster_plot

nest.ResetKernel()

startbuild = time.time()

# Set time resolution of the simulation
nest.SetKernelStatus({'resolution': dt, 'print_time': True})

### CREATE NETWORK NODES ###
print('Building network')

# Set neuron parameters
nest.SetDefaults('iaf_psc_delta', neuron_params)

# Create neurons
nodes_ex=nest.Create('iaf_psc_delta', NE)
nodes_in=nest.Create('iaf_psc_delta', NI)

# Create poisson generator
noise = nest.Create('poisson_generator',params={'rate':nu_ext})

# Create spike detectors
espikes=nest.Create('spike_detector')
ispikes=nest.Create('spike_detector')
nest.SetStatus(espikes,[{'withtime': True,
                        'withgid': True,
                        'to_file': False}])
nest.SetStatus(ispikes,[{'withtime': True,
                         'withgid': True,
                         'to_file': False}])

# Define synapse dictionaries
syn_exc = {'weight': J, 'delay': d}
syn_inh = {'weight': -g*J, 'delay': d}

### CONNECT NETWORK ###
print('Connecting network')

# Connect noise
nest.Connect(noise,nodes_ex, 'all_to_all', syn_exc)
nest.Connect(noise,nodes_in, 'all_to_all', syn_exc)

# Connect spike detector
nest.Connect(nodes_ex[:N_rec], espikes, 'all_to_all')
nest.Connect(nodes_in[:N_rec], ispikes, 'all_to_all')                  

# Connect excitatory neurons
print('Excitatory connections')
conn_exc = {'rule': 'fixed_indegree', 'indegree': CE}
nest.Connect(nodes_ex, nodes_ex, conn_exc, syn_exc)
nest.Connect(nodes_ex, nodes_in, conn_exc, syn_exc)

# Connect inhibitry neurons
print('Inhibitory connections')
conn_inh = {'rule': 'fixed_indegree', 'indegree': CI}
nest.Connect(nodes_in, nodes_ex, conn_inh, syn_inh)
nest.Connect(nodes_in, nodes_in, conn_inh, syn_inh)

endbuild=time.time()

### SIMULATE ###
print('Simulating.')

nest.Simulate(simtime)

endsimulate= time.time()

### NETWORK EVALUATION ###

build_time = endbuild-startbuild
sim_time   = endsimulate-endbuild
events_ex = nest.GetStatus(espikes,'n_events')[0]
rate_ex   = events_ex/simtime*1000.0/N_rec
events_in = nest.GetStatus(ispikes,'n_events')[0]
rate_in   = events_in/simtime*1000.0/N_rec

print('Brunel network simulation (Python)')
print('Building time     : %.2f s' % build_time)
print('Simulation time   : %.2f s' % sim_time)
print('Ex Rate           : %.2f Hz' % rate_ex)
print('In Rate           : %.2f Hz' % rate_in)

if rate_ex > 0:
    # Show raster plot 
    nest.raster_plot.from_device(espikes, hist=True)
    plt.show()
