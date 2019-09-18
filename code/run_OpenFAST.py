from wisdem.aeroelasticse.runFAST_pywrapper import runFAST_pywrapper, runFAST_pywrapper_batch
from wisdem.aeroelasticse.CaseGen_IEC       import CaseGen_IEC

if __name__=="__main__":
    
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
    
    channels = {"GenPwr"   : True, "HSShftTq" : True, "HSSBrTq"  : True, "GenSpeed" : True, "RotSpeed" : True, "TSR"      : True, "TeetDefl" : True, "Azimuth"  : True, "NacYaw"   : True, "TTDspFA"  : True, "TTDspSS"  : True, "NcIMUTAxs": True, "NcIMUTAys": True, "BldPitch2": True, "OoPDefl1" : True, "OoPDefl2" : True, "OoPDefl3" : True, "TipClrnc1": True, "TipClrnc2": True, "TipClrnc3": True, "TipDxb1"  : True, "TipDxb2"  : True, "TipDxb3"  : True, "Spn1MLxb1": True, "Spn2MLxb1": True, "Spn3MLxb1": True, "Spn4MLxb1": True, "Spn5MLxb1": True, "Spn6MLxb1": True, "Spn7MLxb1": True, "Spn8MLxb1": True, "Spn9MLxb1": True, "Spn1MLyb1": True, "Spn2MLyb1": True, "Spn3MLyb1": True, "Spn4MLyb1": True, "Spn5MLyb1": True, "Spn6MLyb1": True, "Spn7MLyb1": True, "Spn8MLyb1": True, "Spn9MLyb1": True, "Spn1MLzb1": True, "Spn2MLzb1": True, "Spn3MLzb1": True, "Spn4MLzb1": True, "Spn5MLzb1": True, "Spn6MLzb1": True, "Spn7MLzb1": True, "Spn8MLzb1": True, "Spn9MLzb1": True, "Spn1FLxb1": True, "Spn2FLxb1": True, "Spn3FLxb1": True, "Spn4FLxb1": True, "Spn5FLxb1": True, "Spn6FLxb1": True, "Spn7FLxb1": True, "Spn8FLxb1": True, "Spn9FLxb1": True, "Spn1FLyb1": True, "Spn2FLyb1": True, "Spn3FLyb1": True, "Spn4FLyb1": True, "Spn5FLyb1": True, "Spn6FLyb1": True, "Spn7FLyb1": True, "Spn8FLyb1": True, "Spn9FLyb1": True, "Spn1FLzb1": True, "Spn2FLzb1": True, "Spn3FLzb1": True, "Spn4FLzb1": True, "Spn5FLzb1": True, "Spn6FLzb1": True, "Spn7FLzb1": True, "Spn8FLzb1": True, "Spn9FLzb1": True, "RootFxc1" : True, "RootFxc2" : True, "RootFxc3" : True, "RootFyc1" : True, "RootFyc2" : True, "RootFyc3" : True, "RootFxb1" : True, "RootFxb2" : True, "RootFxb3" : True, "RootFyb1" : True, "RootFyb2" : True, "RootFyb3" : True, "RootFzb1" : True, "RootFzb2" : True, "RootFzb3" : True, "RootMxc1" : True, "RootMxc2" : True, "RootMxc3" : True, "RootMyc1" : True, "RootMyc2" : True, "RootMyc3" : True, "RootMxb1" : True, "RootMxb2" : True, "RootMxb3" : True, "RootMyb1" : True, "RootMyb2" : True, "RootMyb3" : True, "RootMzb1" : True, "RootMzb2" : True, "RootMzb3" : True, "YawBrFxn" : True, "YawBrFyn" : True, "YawBrFzn" : True, "YawBrFxp" : True, "YawBrFyp" : True, "YawBrMxn" : True, "YawBrMyn" : True, "YawBrMzn" : True, "YawBrMxp" : True, "YawBrMyp" : True, "RotThrust": True, "LSShftTq" : True, "LSShftFxa": True, "LSShftFya": True, "LSShftFza": True, "LSShftFys": True, "LSShftFzs": True, "LSShftMxa": True, "LSSTipMya": True, "LSSTipMza": True, "LSSTipMys": True, "LSSTipMzs": True, "TwrBsFxt" : True, "TwrBsFyt" : True, "TwrBsFzt" : True, "TwrBsMxt" : True, "TwrBsMyt" : True}

    # DLC inputs
    iec.dlc_inputs = {}
    iec.dlc_inputs['DLC']   = [1.1, 1.5]
    iec.dlc_inputs['U']     = [[3., 5., 7., 9., 11., 13., 15., 17., 19., 21., 23., 25], [8.2]]
    iec.dlc_inputs['Seeds'] = [[1, 2, 3, 4, 5, 6], []]
    iec.dlc_inputs['Yaw']   = [[], []]

    iec.transient_dir_change        = 'both'  # '+','-','both': sign for transient events in EDC, EWS
    iec.transient_shear_orientation = 'both'  # 'v','h','both': vertical or horizontal shear for EWS

    # Naming, file management, etc
    iec.wind_dir = 'outputs/wind'
    iec.case_name_base = 'testing'
    if eagle:
        iec.Turbsim_exe = '/projects/windse/importance_sampling/WT_Codes/Turbsim/TurbSim/bin/TurbSim_glin64'
        iec.cores = 36
    else:
        iec.Turbsim_exe = '/mnt/c/Material/Programs/TurbSim/TurbSim_glin64'
        iec.cores = 4
    
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
        fastBatch.FAST_exe = '/home/pbortolo/OpenFAST/build/glue-codes/openfast/openfast'   # Path to executable
        fastBatch.FAST_InputFile = 'RotorSE_FAST_BAR_005a.fst'   # FAST input file (ext=.fst)
        fastBatch.FAST_directory = '/home/pbortolo/wisdem_1_0_0/OpenFAST_BAR005a'   # Path to fst directory files
    else:
        fastBatch.FAST_exe = '/mnt/c/Material/Programs/openfast/build/glue-codes/openfast/openfast'   # Path to executable
        fastBatch.FAST_InputFile = 'RotorSE_FAST_BAR_005a.fst'   # FAST input file (ext=.fst)
        fastBatch.FAST_directory = '/mnt/c/Material/Projects/RefTurbines/BAR/OpenFAST_BAR005a'   # Path to fst directory files
    fastBatch.FAST_runDirectory = iec.run_dir
    fastBatch.case_list = case_list
    fastBatch.case_name_list = case_name_list
    fastBatch.debug_level = 2
    
    if eagle:
        fastBatch.run_multi(36)
    else:
        fastBatch.run_serial()
    
    
    
    
    
    
    