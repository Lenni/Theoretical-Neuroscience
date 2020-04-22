# global imports
import matplotlib.pyplot as plt

# import simulator
import nest

T = 1.2e3 # (ms)
I_ext = 0. # (pA)
nu_ext = 14000. # (Hz)
J = 0.1 # (mV)
d = .1 # (ms)

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

# set default neuron parameters
nest.SetDefaults('iaf_psc_delta', neuron_params)

# create neuron which receives constant current
neuron1 = nest.Create('iaf_psc_delta')
nest.SetStatus(neuron1, {'I_e': I_ext})

# create multimeter to record membrane potential of neuron1
multimeter1 = nest.Create('multimeter')
nest.SetStatus(multimeter1, {'record_from': ['V_m']})
nest.Connect(multimeter1, neuron1)

# create spike detector to record spikes of neuron1
spikedetector1 = nest.Create('spike_detector')
nest.SetStatus(spikedetector1, [{'withtime': True,
                                 'withgid': True,
                                 'to_file': False}])
nest.Connect(neuron1, spikedetector1)

# create neuron which receives Poissonian spike trains
neuron2 = nest.Create('iaf_psc_delta')
pgen = nest.Create('poisson_generator')
nest.SetStatus(pgen, {'rate': nu_ext})
syn_dic = {'weight': J, 'delay': d}
nest.Connect([pgen[0]], [neuron2[0]], 'one_to_one', syn_dic)

# create multimeter to record membrane potential of neuron2
multimeter2 = nest.Create('multimeter')
nest.SetStatus(multimeter2, {'record_from': ['V_m']})
nest.Connect(multimeter2, neuron2)

# create spike detector to record spikes of neuron2
spikedetector2 = nest.Create('spike_detector')
nest.SetStatus(spikedetector2, [{'withtime': True,
                                 'withgid': True,
                                 'to_file': False}])
nest.Connect(neuron2, spikedetector2)

# start simulation
nest.Simulate(T)

# get data for neuron1
data1 = nest.GetStatus(multimeter1)[0]['events']
v_mem1 = data1['V_m']
times1 = data1['times']
spikes1 = nest.GetStatus(spikedetector1)[0]['events']['times']
rate1 = float(len(spikes1))/T*1e3
print('\nRate of neuron stimulated with current input: %.2f spikes/s'%(rate1))

# get data for neuron2
data2 = nest.GetStatus(multimeter2)[0]['events']
v_mem2 = data2['V_m']
times2 = data2['times']
spikes2 = nest.GetStatus(spikedetector2)[0]['events']['times']
rate2 = float(len(spikes2))/T*1e3
print('Rate of neuron stimulated with Poissonian spike trains: %.2f spikes/s'%(rate2))

# plot results
fig1 = plt.figure(1)
ax1 = fig1.add_subplot(111)
ax1.plot(times1, v_mem1, label='current')
ax1.plot(times2, v_mem2, label='Poisson input')
ax1.set_xlabel('Time (ms)')
ax1.set_ylabel(r'$V_m$ (mV)')
ax1.set_xlim([0., T])
ax1.set_ylim([-5., 20.])
plt.legend()
plt.show()
