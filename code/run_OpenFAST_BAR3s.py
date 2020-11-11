from weis.aeroelasticse.runFAST_pywrapper import runFAST_pywrapper_batch
from weis.aeroelasticse.CaseGen_General import CaseGen_General
import numpy as np

fastBatch = runFAST_pywrapper_batch(FAST_ver='OpenFAST', dev_branch=True)

#eagle =  True

#if eagle:
#    fastBatch.FAST_exe = '/home/njohnso1/openfast-dev/build/glue-codes/openfast/openfast'   # Path to executable
fastBatch.FAST_InputFile = 'BAR3.fst'   # FAST input file (ext=.fst)
fastBatch.FAST_directory = '/home/pbortolo/BAR_Designs/BAR3/OpenFAST'   # Path to fst directory files
#else:
fastBatch.FAST_exe = '/home/pbortolo/OpenFAST/build/glue-codes/openfast/openfast'   # Path to executable
#    fastBatch.FAST_InputFile = 'OpenFAST_BAR_02.fst'   # FAST input file (ext=.fst)
#    fastBatch.FAST_directory = '/Users/pbortolo/work/2_openfast/BAR/OpenFAST_Models/BAR_00'   # Path to fst directory files

fastBatch.FAST_runDirectory = '/projects/bar/pbortolo/stability_BAR3_2tons'
fastBatch.debug_level       = 2

rot_speeds  = [3.89402902770845, 4.86753628463557, 5.84104354156269, 6.81455079848979, 7.74597418411393, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711]
vs_rttq     = [3.89402902770845, 4.86753628463557, 5.84104354156269, 6.81455079848979, 7.74597418411393, 7.88077303226711, 7.88077303226711, 9.3691340462867, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711, 7.88077303226711]
pitch       = [0, 0, 0, 0, 0, 4.070379436, 6.51155994232614, 8.43327866258402, 10.0679704768828, 11.5755627871602, 13.0017101713448, 14.3343395149246, 15.609677425119, 16.8494763077444, 18.0255503331993, 19.1916771429219, 20.2950891003584, 21.396277235847, 22.4455033280989, 23.493048544028, 24.4937272196032, 25.4944058951784]
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

#if eagle:
fastBatch.run_multi(36)
#else:
#    fastBatch.run_serial()

