from wisdem.aeroelasticse.runFAST_pywrapper import runFAST_pywrapper, runFAST_pywrapper_batch
from wisdem.aeroelasticse.CaseGen_IEC       import CaseGen_IEC

    

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
iec.dlc_inputs['DLC']   = [1.4]
iec.dlc_inputs['U']     = [[ 6.2]]
iec.dlc_inputs['Seeds'] = [[1]]
iec.dlc_inputs['Yaw']   = [[]]

iec.transient_dir_change        = 'both'  # '+','-','both': sign for transient events in EDC, EWS
iec.transient_shear_orientation = 'both'  # 'v','h','both': vertical or horizontal shear for EWS

# Naming, file management, etc
iec.wind_dir = 'outputs/wind'
iec.case_name_base = 'Hitachi'
iec.Turbsim_exe = '/Users/pbortolo/work/2_openfast/TurbSim/bin/TurbSim_glin64'
iec.cores = 1

iec.debug_level = 2
iec.parallel_windfile_gen = True
iec.run_dir = 'outputs/Hitachi'

# Run case generator / wind file writing
case_inputs = {}
case_inputs[('Fst','OutFileFmt')] = {'vals':[1], 'group':0}
case_inputs[("Fst","CompHydro")]         = {'vals':[0], 'group':0}
case_inputs[("Fst","CompSub")]           = {'vals':[0], 'group':0}
case_inputs[("ElastoDyn","PtfmSgDOF")]   = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","PtfmSwDOF")]   = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","PtfmHvDOF")]   = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","PtfmRDOF")]    = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","PtfmPDOF")]    = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","PtfmYDOF")]    = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","TwFADOF1")]    = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","TwFADOF2")]    = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","TwSSDOF1")]    = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","TwSSDOF2")]    = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","FlapDOF1")]    = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","FlapDOF2")]    = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","EdgeDOF")]     = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","DrTrDOF")]     = {'vals':["False"], 'group':0}
case_inputs[("ElastoDyn","GenDOF")]      = {'vals':["True"], 'group':0}
case_inputs[("ElastoDyn","YawDOF")]      = {'vals':["False"], 'group':0}




case_list, case_name_list = iec.execute(case_inputs=case_inputs)

# Run FAST cases
fastBatch = runFAST_pywrapper_batch(FAST_ver='OpenFAST',dev_branch = True)
fastBatch.FAST_exe = '/Users/pbortolo/work/2_openfast/openfast/build/glue-codes/openfast/openfast'   # Path to executable
fastBatch.FAST_InputFile = 'DW0.fst'   # FAST input file (ext=.fst)
fastBatch.FAST_directory = '/Users/pbortolo/work/3_projects/1_Hitachi/files2Hitachi/OpenFAST/DW0'   # Path to fst directory files
fastBatch.FAST_runDirectory = iec.run_dir
fastBatch.case_list = case_list
fastBatch.case_name_list = case_name_list
fastBatch.debug_level = 2
fastBatch.run_serial()
    
    
    
    
    
    
    
