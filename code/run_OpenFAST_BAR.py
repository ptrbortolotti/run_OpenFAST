from wisdem.aeroelasticse.runFAST_pywrapper import runFAST_pywrapper, runFAST_pywrapper_batch
from wisdem.aeroelasticse.CaseGen_IEC       import CaseGen_IEC

    
eagle = True

iec = CaseGen_IEC()
iec.Turbine_Class = 'III' # I, II, III, IV
iec.Turbulence_Class = 'A'
iec.D = 206.
iec.z_hub = 140.


# Turbine Data
iec.init_cond = {} # can leave as {} if data not available
iec.init_cond[("ElastoDyn","RotSpeed")] = {'U':[3., 5., 7., 8.2, 25.]}
iec.init_cond[("ElastoDyn","RotSpeed")]['val'] = [2.92, 4.88, 6.81, 7.835, 7.88]
iec.init_cond[("ElastoDyn","BlPitch1")] = {'U':[3., 8.2,  9., 11.,  13.,  15.,  17., 19., 21., 23., 25]}
iec.init_cond[("ElastoDyn","BlPitch1")]['val'] = [0., 0., 2.93, 8.76, 12.01, 14.82, 17.37, 19.73, 21.96, 24.08, 26.10]
iec.init_cond[("ElastoDyn","BlPitch2")] = iec.init_cond[("ElastoDyn","BlPitch1")]
iec.init_cond[("ElastoDyn","BlPitch3")] = iec.init_cond[("ElastoDyn","BlPitch1")]

# DLC inputs
iec.dlc_inputs = {}
iec.dlc_inputs['DLC']   = [1.1, 1.3, 1.4, 1.5, 6.1, 6.3]
iec.dlc_inputs['U']     = [[3., 5., 7., 9., 11., 13., 15., 17., 19., 21., 23., 25], [3., 5., 7., 9., 11., 13., 15., 17., 19., 21., 23., 25],[6.2, 8.2, 10.2],[3., 5., 7., 9., 11., 13., 15., 17., 19., 21., 23., 25], [], []]
iec.dlc_inputs['Seeds'] = [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], range(1,7), range(1,7)]
iec.dlc_inputs['Yaw']   = [[], [], [], [], [], []]

iec.transient_dir_change        = 'both'  # '+','-','both': sign for transient events in EDC, EWS
iec.transient_shear_orientation = 'both'  # 'v','h','both': vertical or horizontal shear for EWS

# Naming, file management, etc
iec.wind_dir = 'outputs/wind'
iec.case_name_base = 'BAR00'
if eagle:
    iec.Turbsim_exe = '/projects/windse/importance_sampling/WT_Codes/Turbsim/TurbSim/bin/TurbSim_glin64'
    iec.cores = 36
else:
    iec.Turbsim_exe = '/Users/pbortolo/work/2_openfast/TurbSim/bin/TurbSim_glin64'
    iec.cores = 1

iec.debug_level = 2
iec.parallel_windfile_gen = True
iec.run_dir = 'outputs/OpenFAST'

# Run case generator / wind file writing
case_inputs = {}
case_inputs[('Fst','OutFileFmt')] = {'vals':[1], 'group':0}
case_list, case_name_list = iec.execute(case_inputs=case_inputs)

# Run FAST cases
fastBatch = runFAST_pywrapper_batch(FAST_ver='OpenFAST',dev_branch = True)
if eagle:
    fastBatch.FAST_exe = '/projects/windse/hitachi/openfast/build/glue-codes/openfast/openfast'   # Path to executable
    fastBatch.FAST_InputFile = 'OpenFAST_BAR_00.fst'   # FAST input file (ext=.fst)
    fastBatch.FAST_directory = '/home/pbortolo/wisdem_1_0_0/BAR/OpenFAST_Models/BAR_00'   # Path to fst directory files
else:
    fastBatch.FAST_exe = '/Users/pbortolo/work/2_openfast/openfast/build/glue-codes/openfast/openfast'   # Path to executable
    fastBatch.FAST_InputFile = 'OpenFAST_BAR_00.fst'   # FAST input file (ext=.fst)
    fastBatch.FAST_directory = '/Users/pbortolo/work/2_openfast/BAR/OpenFAST_Models/BAR_00'   # Path to fst directory files
fastBatch.FAST_runDirectory = iec.run_dir
fastBatch.case_list = case_list
fastBatch.case_name_list = case_name_list
fastBatch.debug_level = 2

if eagle:
    fastBatch.run_multi(36)
else:
    fastBatch.run_serial()
    
    
    
    
    
    
    
