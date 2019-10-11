from wisdem.aeroelasticse.runFAST_pywrapper import runFAST_pywrapper, runFAST_pywrapper_batch
from wisdem.aeroelasticse.CaseGen_IEC       import CaseGen_IEC

if __name__=="__main__":
    
    eagle = True
    
    iec = CaseGen_IEC()
    iec.Turbine_Class = 'I' # I, II, III, IV
    iec.Turbulence_Class = 'B'
    iec.D = 240.
    iec.z_hub = 150.
    
    
    # Turbine Data
    iec.init_cond = {} # can leave as {} if data not available
    iec.init_cond[("ElastoDyn","RotSpeed")] = {'U':[3., 10.5, 25.]}
    iec.init_cond[("ElastoDyn","RotSpeed")]['val'] = [2., 7.5, 7.5]
    iec.init_cond[("ElastoDyn","BlPitch1")] = {'U':  [3., 11.,  13.,  15.,  20., 25.]}
    iec.init_cond[("ElastoDyn","BlPitch1")]['val'] = [0.,  0.,   8.,  12.,  18., 22.]
    iec.init_cond[("ElastoDyn","BlPitch2")] = iec.init_cond[("ElastoDyn","BlPitch1")]
    iec.init_cond[("ElastoDyn","BlPitch3")] = iec.init_cond[("ElastoDyn","BlPitch1")]
    
    # DLC inputs
    iec.dlc_inputs = {}
    iec.dlc_inputs['DLC']   = [1.1, 1.3, 1.4, 1.5]
    iec.dlc_inputs['U']     = [[3., 5., 7., 9., 11., 13., 15., 17., 19., 21., 23., 25], [3., 5., 7., 9., 11., 13., 15., 17., 19., 21., 23., 25],[6.2, 8.2, 10.2],[3., 5., 7., 9., 11., 13., 15., 17., 19., 21., 23., 25]]
    iec.dlc_inputs['Seeds'] = [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [], []]
    
    iec.dlc_inputs['Yaw']   = [[], []]

    iec.transient_dir_change        = 'both'  # '+','-','both': sign for transient events in EDC, EWS
    iec.transient_shear_orientation = 'both'  # 'v','h','both': vertical or horizontal shear for EWS

    # Naming, file management, etc
    iec.wind_dir = 'outputs/wind_IEA'
    iec.case_name_base = 'IEA15'
    if eagle:
        iec.Turbsim_exe = '/projects/windse/importance_sampling/WT_Codes/Turbsim/TurbSim/bin/TurbSim_glin64'
        iec.cores = 36
    else:
        iec.Turbsim_exe = '/mnt/c/Material/Programs/TurbSim/TurbSim_glin64'
        iec.cores = 1
    
    iec.debug_level = 2
    iec.parallel_windfile_gen = True
    iec.run_dir = 'outputs/runs_IEA'

    # Run case generator / wind file writing
    case_inputs = {}
    case_inputs[('Fst','OutFileFmt')] = {'vals':[1], 'group':0}
    case_list, case_name_list = iec.execute(case_inputs=case_inputs)

    # Run FAST cases
    fastBatch = runFAST_pywrapper_batch(FAST_ver='OpenFAST',dev_branch = True)
    if eagle:
        fastBatch.FAST_exe = '/home/pbortolo/OpenFAST/build/glue-codes/openfast/openfast'   # Path to executable
        fastBatch.FAST_InputFile = 'NREL15mw_OpenFAST_prelim_v4.fst'   # FAST input file (ext=.fst)
        fastBatch.FAST_directory = '/home/pbortolo/wisdem_1_0_0/IEA-15-240-RWT/OpenFAST/NREL15mw_OpenFAST_prelim_v4'   # Path to fst directory files
    else:
        fastBatch.FAST_exe = '/mnt/c/Material/Programs/openfast/build/glue-codes/openfast/openfast'   # Path to executable
        fastBatch.FAST_InputFile = 'NREL15mw_OpenFAST_prelim_v4.fst'   # FAST input file (ext=.fst)
        fastBatch.FAST_directory = '/mnt/c/Material/Projects/IEATask37/IEA-15-240-RWT/OpenFAST/NREL15mw_OpenFAST_prelim_v4'   # Path to fst directory files
    fastBatch.FAST_runDirectory = iec.run_dir
    fastBatch.case_list = case_list
    fastBatch.case_name_list = case_name_list
    fastBatch.debug_level = 2
    
    if eagle:
        fastBatch.run_multi(36)
    else:
        fastBatch.run_serial()
    
    
    
    
    
    
    
