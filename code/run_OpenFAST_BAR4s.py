from weis.aeroelasticse.runFAST_pywrapper import runFAST_pywrapper_batch
from weis.aeroelasticse.CaseGen_General import CaseGen_General
import numpy as np

fastBatch = runFAST_pywrapper_batch(FAST_ver='OpenFAST', dev_branch=True)

fastBatch.FAST_exe = '/home/pbortolo/OpenFAST/build/glue-codes/openfast/openfast'   # Path to executable
fastBatch.FAST_InputFile = 'BAR4.fst'   # FAST input file (ext=.fst)
fastBatch.FAST_directory = '/home/pbortolo/BAR_Designs/BAR4/OpenFAST'   # Path to fst directory files

fastBatch.FAST_runDirectory = '/projects/bar/njohnson1/stability/BAR4_25ms'
fastBatch.debug_level       = 2

rot_speeds  = [4.22194687529269, 5.27743359411587, 6.33292031293905, 7.38840703176222, 8.38645916978818, 8.54441629523521, 8.54441629523521, 8.54441629523521, 8.54441629523521, 8.54441629523521, 8.54441629523521, 8.54441629523521, 8.54441629523521, 8.54441629523521, 8.54441629523521, 8.54441629523521, 8.54441629523521, 8.54441629523521, 8.54441629523521, 8.54441629523521, 8.54441629523521, 8.54441629523521]
vs_rttq     = [15609.1724825517, 23821.030003987, 33670.63, 44665.2907278147, 57277.7417881564, 63890.8817881564, 63890.8817881564, 63890.8817881564, 63890.8817881564, 63890.8817881564, 63890.8817881564, 63890.8817881564, 63890.8817881564, 63890.8817881564, 63890.8817881564, 63890.8817881564, 63890.8817881564, 63890.8817881564, 63890.8817881564, 63890.8817881564, 63890.8817881564, 63890.8817881564]
pitch       = [0, 0, 0, 0, -0.0694593280059301, 1.39350131636704, 5.77704455697533, 7.98145486817877, 9.78076342227657, 11.4207912028573, 12.9592973195397, 14.3845813702857, 15.7418275793855, 17.0568685478912, 18.2973110702748, 19.5254856940195, 20.6820854737319, 21.8355140837904, 22.92929022846, 24.0211598956912, 25.05987276573, 26.0985856357687]
hws         = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
NLinTimes   = 36
TMax        = 55.

trim_case = np.zeros(len(rot_speeds), dtype=int)
trim_gain = np.zeros(len(rot_speeds))

for i in range(len(rot_speeds)):
    if pitch[i] == 0.:
        trim_case[i] = 2
        trim_gain[i] = 0
    else:
        trim_case[i] = 3
        trim_gain[i] = 0.001


LinTimes  = np.zeros([len(rot_speeds), NLinTimes])
for i in range(len(rot_speeds)):
    for j in range(NLinTimes):
        LinTimes[i,j] = TMax + j * 60./rot_speeds[i]/ NLinTimes
TMax += 15.        

case_inputs = {}
case_inputs[("ElastoDyn","FlapDOF1")]   = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","FlapDOF2")]   = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","EdgeDOF")]    = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","TeetDOF")]    = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","DrTrDOF")]    = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","GenDOF")]     = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","YawDOF")]     = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","TwFADOF1")]   = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","TwFADOF2")]   = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","TwSSDOF1")]   = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","TwSSDOF2")]   = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","TTDspFA")]    = {'vals':[5], 'group':0}
case_inputs[("Fst","TMax")]             = {'vals':[TMax], 'group':0}
case_inputs[("Fst","DT")]               = {'vals':[0.0004], 'group':0}
case_inputs[("Fst","CompInflow")]       = {'vals':[0], 'group':0}
case_inputs[("Fst","OutFileFmt")]       = {'vals':[1], 'group':0}
case_inputs[("Fst","CompElast")]        = {'vals':[2], 'group':0}
case_inputs[("Fst","CompAero")]         = {'vals':[0], 'group':0}

case_inputs[("Fst","Linearize")]        = {'vals':["True"], 'group':0}
case_inputs[("Fst","NLinTimes")]        = {'vals':[NLinTimes], 'group':0}
case_inputs[("Fst","LinTimes")]         = {'vals':LinTimes, 'group':1}
case_inputs[("Fst","LinInputs")]        = {'vals':[1], 'group':0}
case_inputs[("Fst","LinOutputs")]       = {'vals':[1], 'group':0}
case_inputs[("Fst","LinOutJac")]        = {'vals':["False"], 'group':0}
case_inputs[("Fst","LinOutMod")]        = {'vals':["False"], 'group':0}

case_inputs[("ServoDyn","PCMode")]      = {'vals':[0], 'group':0}
case_inputs[("ServoDyn","VSContrl")]    = {'vals':[0], 'group':0}
case_inputs[("ServoDyn","VS_RtGnSp")]   = {'vals':[9.9999E-6], 'group':0}
case_inputs[("ServoDyn","VS_Rgn2K")]    = {'vals':[9.9999E-6], 'group':0}
case_inputs[("ServoDyn","VS_SlPc")]     = {'vals':[9.9999E-6], 'group':0}
case_inputs[("ServoDyn","VS_RtTq")]     = {'vals':vs_rttq, 'group': 1}
case_inputs[("AeroDyn15","AFAeroMod")]  = {'vals':[1], 'group':0}
case_inputs[("InflowWind","WindType")]  = {'vals':[1], 'group':0}
case_inputs[("InflowWind","HWindSpeed")]= {'vals': hws, 'group': 1}
case_inputs[("ElastoDyn","RotSpeed")]   = {'vals': rot_speeds, 'group': 1}
case_inputs[("ElastoDyn","BlPitch1")]   = {'vals': pitch, 'group': 1}
case_inputs[("ElastoDyn","BlPitch2")]   = case_inputs[("ElastoDyn","BlPitch1")]
case_inputs[("ElastoDyn","BlPitch3")]   = case_inputs[("ElastoDyn","BlPitch1")]

case_list, case_name_list = CaseGen_General(case_inputs, dir_matrix=fastBatch.FAST_runDirectory, namebase='testing')

fastBatch.case_list = case_list
fastBatch.case_name_list = case_name_list

fastBatch.run_multi(36)


