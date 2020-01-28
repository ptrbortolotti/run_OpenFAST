from wisdem.aeroelasticse.runFAST_pywrapper import runFAST_pywrapper, runFAST_pywrapper_batch
from wisdem.aeroelasticse.CaseGen_IEC       import CaseGen_IEC

import shutil

if __name__=="__main__":
    
    eagle = True
    
    iec = CaseGen_IEC()
    iec.Turbine_Class = 'I' # I, II, III, IV
    iec.Turbulence_Class = 'A'
    iec.D = 204.
    iec.z_hub = 131.5
    
    # adjust later
    # Turbine Data
    iec.init_cond = {} # can leave as {} if data not available
    iec.init_cond[("ElastoDyn","RotSpeed")] = {'U':[4.000000000000000000e+00, 5.105263157894737169e+00, 6.210526315789474339e+00, 7.315789473684210620e+00, 8.421052631578948677e+00, 9.000000000000000000e+00, 2.500000000000000000e+01]}
    iec.init_cond[("ElastoDyn","RotSpeed")]['val'] = [3.744822190397536943e+00, 4.779575690375803987e+00, 5.814329190354071919e+00, 6.849082690332338963e+00, 7.883836190310606007e+00, 8.425849928394459454e+00, 8.425849928394459454e+00]
    iec.init_cond[("ElastoDyn","BlPitch1")] = {'U':[4.000000000000000000e+00, 1.066803743941258809e+01, 1.173684210526315752e+01, 1.284210526315789558e+01, 1.394736842105263186e+01, 1.505263157894736992e+01, 1.615789473684210620e+01, 1.726315789473684248e+01, 1.836842105263158231e+01, 1.947368421052631504e+01, 2.057894736842105488e+01, 2.168421052631579116e+01, 2.278947368421052744e+01, 2.389473684210526372e+01, 2.500000000000000000e+01]}
    iec.init_cond[("ElastoDyn","BlPitch1")]['val'] = [0., 0., 5.074352971947472035e+00, 7.786747053509759375e+00, 9.942305156633004515e+00, 1.182455292927485146e+01, 1.353567522224319397e+01, 1.512176953395546164e+01, 1.661022980833649498e+01, 1.801929396075015077e+01, 1.936157283370897986e+01, 2.064702870035782922e+01, 2.188383170827142266e+01, 2.307840321137150852e+01, 2.423572382317490437e+01]
    iec.init_cond[("ElastoDyn","BlPitch2")] = iec.init_cond[("ElastoDyn","BlPitch1")]
    iec.init_cond[("ElastoDyn","BlPitch3")] = iec.init_cond[("ElastoDyn","BlPitch1")]
    
    # DLC inputs
    iec.dlc_inputs = {}
    #iec.dlc_inputs['DLC']   = [1.1]
    #iec.dlc_inputs['U']     = [[4., 5., 7., 9., 11., 13., 15., 17., 19., 21., 23., 25]]
    #iec.dlc_inputs['Seeds'] = [[1, 2, 3, 4, 5, 6]]
    iec.dlc_inputs['DLC']   = [1.1, 1.3, 1.4, 1.5]
    iec.dlc_inputs['U']     = [[4., 5., 7., 9., 11., 13., 15., 17., 19., 21., 23., 25], [4., 5., 7., 9., 11., 13., 15., 17., 19., 21., 23., 25],[8., 10., 12.],[4., 5., 7., 9., 11., 13., 15., 17., 19., 21., 23., 25]]
    iec.dlc_inputs['Seeds'] = [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6], [], []]
    iec.dlc_inputs['Yaw']   = [[]]

    iec.transient_dir_change        = 'both'  # '+','-','both': sign for transient events in EDC, EWS
    iec.transient_shear_orientation = 'both'  # 'v','h','both': vertical or horizontal shear for EWS

    # Naming, file management, etc
    iec.wind_dir = 'outputs/wind_Hitachi'
    iec.case_name_base = 'Hitachi'
    if eagle:
        iec.Turbsim_exe = '/projects/windse/importance_sampling/WT_Codes/Turbsim/TurbSim/bin/TurbSim_glin64'
        iec.cores = 36
    else:
        iec.Turbsim_exe = '/mnt/c/Material/Programs/TurbSim/TurbSim_glin64'
        iec.cores = 1
    
    iec.debug_level = 2
    iec.parallel_windfile_gen = True
    iec.run_dir = 'outputs/200128_baseline_up'

    # Run case generator / wind file writing
    case_inputs = {}
    case_inputs[('Fst','OutFileFmt')] = {'vals':[1], 'group':0}
    case_list, case_name_list = iec.execute(case_inputs=case_inputs)

    # Run FAST cases
    fastBatch = runFAST_pywrapper_batch(FAST_ver='OpenFAST',dev_branch = True)
    if eagle:
        fastBatch.FAST_exe = '/projects/windse/hitachi/openfast/build/glue-codes/openfast/openfast'   # Path to executable
        fastBatch.FAST_InputFile = 'Baseline_Hit10MW.fst'   # FAST input file (ext=.fst)
        fastBatch.FAST_directory = '/projects/windse/hitachi/Hitachi_Design/OpenFAST/Baseline_Hit10MW_upwind'   # Path to fst directory files
    else:
        fastBatch.FAST_exe = '/mnt/c/GitHub/OpenFAST/build/glue-codes/openfast/openfast'   # Path to executable
        fastBatch.FAST_InputFile = 'Baseline_Hit10MW.fst'   # FAST input file (ext=.fst)
        fastBatch.FAST_directory = '/mnt/c/GitHub/Hitachi_Design/OpenFAST/Baseline_Hit10MW/'   # Path to fst directory files
    shutil.copyfile(fastBatch.FAST_directory + '/DISCON.IN',iec.run_dir + '/DISCON.IN')
    shutil.copyfile(fastBatch.FAST_directory + '/Cp_Ct_Cq_Hit10MW_v14.txt',iec.run_dir + '/Cp_Ct_Cq_Hit10MW_v14.txt')
    fastBatch.FAST_runDirectory = iec.run_dir
    fastBatch.case_list = case_list
    fastBatch.case_name_list = case_name_list
    fastBatch.debug_level = 2
    
    if eagle:
        fastBatch.run_multi(36)
    else:
        fastBatch.run_serial()
    
    
    
    
    
    
    
