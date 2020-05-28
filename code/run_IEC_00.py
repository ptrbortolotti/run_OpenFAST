from __future__ import print_function
import os, sys, time, shutil
import multiprocessing as mp
import numpy as np
import ruamel_yaml as ry
import matplotlib.pyplot as plt

from wisdem.aeroelasticse.runFAST_pywrapper import runFAST_pywrapper_batch
from wisdem.aeroelasticse.CaseGen_IEC       import CaseGen_General, CaseGen_IEC
from wisdem.aeroelasticse.FAST_post         import return_timeseries, return_fname

plt.rcParams["font.size"] = 10
plt.rcParams["font.family"] = "DejaVu Serif"
plt.rcParams['mathtext.fontset'] = "dejavuserif"

def load_yaml(fname_input):
    with open(fname_input, 'r') as myfile:
        text_input = myfile.read()
    myfile.close()
    yaml = ry.YAML()
    return dict(yaml.load(text_input))


def runFAST_CaseGenIEC(init_cond, offshore=False):

    ####
    #TMax    = 720.
    #TStart  = 120.
    #T_trans = 320.
    TMax    = 840.
    TStart  = 240.
    T_trans = 540.
    ####


    iec = CaseGen_IEC()

    # Turbine Data
    iec.init_cond = {} # can leave as {} if data not available
    iec.init_cond[("ElastoDyn","RotSpeed")]        = {'U':init_cond['Wind1VelX']}
    iec.init_cond[("ElastoDyn","RotSpeed")]['val'] = init_cond['RotSpeed']
    iec.init_cond[("ElastoDyn","BlPitch1")]        = {'U':init_cond['Wind1VelX']}
    iec.init_cond[("ElastoDyn","BlPitch1")]['val'] = init_cond['BldPitch1']
    iec.init_cond[("ElastoDyn","BlPitch2")]        = iec.init_cond[("ElastoDyn","BlPitch1")]
    iec.init_cond[("ElastoDyn","BlPitch3")]        = iec.init_cond[("ElastoDyn","BlPitch1")]

    if offshore:
        iec.init_cond[("HydroDyn","WaveHs")]        = {'U':[3, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 25, 40, 50]}
        iec.init_cond[("HydroDyn","WaveHs")]['val'] = [1.101917033, 1.101917033, 1.179052649, 1.315715154, 1.536867124, 1.835816514, 2.187994638, 2.598127096, 3.061304068, 3.617035443, 4.027470219, 4.51580671, 4.51580671, 9.686162473, 11.307125]
        iec.init_cond[("HydroDyn","WaveTp")]        = {'U':[3, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 25, 40, 50]}
        iec.init_cond[("HydroDyn","WaveTp")]['val'] = [8.515382435, 8.515382435, 8.310063688, 8.006300889, 7.6514231, 7.440581338, 7.460834063, 7.643300307, 8.046899942, 8.521314105, 8.987021024, 9.451641026, 9.451641026, 16.65396967, 18.50491229]
        iec.init_cond[("HydroDyn","PtfmSurge")]        = {'U':[3., 15., 25.]}
        iec.init_cond[("HydroDyn","PtfmSurge")]['val'] = [4., 15., 10.]
        iec.init_cond[("HydroDyn","PtfmPitch")]        = {'U':[3., 15., 25.]}
        iec.init_cond[("HydroDyn","PtfmPitch")]['val'] = [-1., 3., 1.3]
        iec.init_cond[("HydroDyn","PtfmHeave")]        = {'U':[3., 25.]}
        iec.init_cond[("HydroDyn","PtfmHeave")]['val'] = [0.5,0.5]

    iec.Turbine_Class    = 'I' # I, II, III, IV
    iec.Turbulence_Class = 'B'
    iec.D                = 240.
    iec.z_hub            = 150.

    V_rated = 8.25867815

    # DLC inputs
    iec.dlc_inputs = {}
    #iec.dlc_inputs['DLC']   = [1.1]
    #iec.dlc_inputs['U']     = [np.arange(3., 26., 2.)] #
    #iec.dlc_inputs['Seeds'] = [range(1,7)]
    #iec.dlc_inputs['Yaw']   = [[]]
    iec.dlc_inputs['DLC']   = [1.1, 1.3, 1.4, 1.5, 6.1, 6.3]
    iec.dlc_inputs['U']     = [np.arange(3., 26., 2.), np.arange(3., 26., 2.), [V_rated-2., V_rated, V_rated+2.], np.arange(3., 26., 2.), [], []] #
    iec.dlc_inputs['Seeds'] = [range(1,7), range(1,7), [], [], range(1,7), range(1,7)]
    iec.dlc_inputs['Yaw']   = [[], [], [], [], [], []]
    #iec.dlc_inputs['DLC']   = [1.1]
    #iec.dlc_inputs['U']     = [[13.]] #
    #iec.dlc_inputs['Seeds'] = [[1]]
    #iec.dlc_inputs['Yaw']   = [[]]

    iec.transient_dir_change        = 'both'  # '+','-','both': sign for transient events in EDC, EWS
    iec.transient_shear_orientation = 'both'  # 'v','h','both': vertical or horizontal shear for EWS
    iec.TMax                        = TMax    # wind file length
    iec.TStart                      = T_trans # start of transcient events (annoying different use of TStart var name)

    # Naming, file management, etc
    iec.wind_dir              = 'run_dir/BAR00_IEC_run2/wind'
    iec.case_name_base        = 'BAR00_IEC_run2'
    iec.Turbsim_exe           = "TurbSim"
    # iec.Turbsim_exe           = "/mnt/c/linux/WT_Codes/TurbSim_v2.00.07a-bjj/TurbSim_glin64"
    iec.debug_level           = 2
    iec.overwrite             = False
    iec.parallel_windfile_gen = True
    iec.cores                 = 24
    iec.run_dir               = 'run_dir/BAR00_IEC_run2'
    iec.flag_enlarge_grid     = True

    # Run case generator / wind file writing
    case_inputs = {}
    # case_inputs[("Fst","TStart")]            = {'vals':[0.], 'group':0} # 120
    # case_inputs[("Fst","TMax")]              = {'vals':[200.], 'group':0} # 720
    case_inputs[("Fst","DT")]                = {'vals':[0.01], 'group':0}
    case_inputs[("Fst","OutFileFmt")]        = {'vals':[2], 'group':0}
    case_inputs[("Fst","TMax")]              = {'vals':[TMax], 'group':0} # 720
    case_inputs[("Fst","TStart")]            = {'vals':[TStart], 'group':0} # 120
    if offshore:
        # case_inputs[("Fst","DT_Out")]            = {'vals':[0.05], 'group':0} # 720
        case_inputs[("Fst","CompHydro")]         = {'vals':[1], 'group':0}
        case_inputs[("HydroDyn","WaveMod")]      = {'vals':[2], 'group':0}
        case_inputs[("HydroDyn","WvDiffQTF")]    = {'vals':["False"], 'group':0}
        # case_inputs[("Fst","CompSub")]           = {'vals':[1], 'group':0}
        case_inputs[("ElastoDyn","PtfmSgDOF")]   = {'vals':["True"], 'group':0}
        case_inputs[("ElastoDyn","PtfmSwDOF")]   = {'vals':["True"], 'group':0}
        case_inputs[("ElastoDyn","PtfmHvDOF")]   = {'vals':["True"], 'group':0}
        case_inputs[("ElastoDyn","PtfmRDOF")]    = {'vals':["True"], 'group':0}
        case_inputs[("ElastoDyn","PtfmPDOF")]    = {'vals':["True"], 'group':0}
        case_inputs[("ElastoDyn","PtfmYDOF")]    = {'vals':["True"], 'group':0}
    else:
        case_inputs[("Fst","CompHydro")]         = {'vals':[0], 'group':0}
        case_inputs[("Fst","CompSub")]           = {'vals':[0], 'group':0}
        case_inputs[("ElastoDyn","PtfmSgDOF")]   = {'vals':["False"], 'group':0}
        case_inputs[("ElastoDyn","PtfmSwDOF")]   = {'vals':["False"], 'group':0}
        case_inputs[("ElastoDyn","PtfmHvDOF")]   = {'vals':["False"], 'group':0}
        case_inputs[("ElastoDyn","PtfmRDOF")]    = {'vals':["False"], 'group':0}
        case_inputs[("ElastoDyn","PtfmPDOF")]    = {'vals':["False"], 'group':0}
        case_inputs[("ElastoDyn","PtfmYDOF")]    = {'vals':["False"], 'group':0}
    case_inputs[("ElastoDyn","TwFADOF1")]    = {'vals':["False"], 'group':0}
    case_inputs[("ElastoDyn","TwFADOF2")]    = {'vals':["False"], 'group':0}
    case_inputs[("ElastoDyn","TwSSDOF1")]    = {'vals':["False"], 'group':0}
    case_inputs[("ElastoDyn","TwSSDOF2")]    = {'vals':["False"], 'group':0}
    case_inputs[("ElastoDyn","FlapDOF1")]    = {'vals':["True"], 'group':0}
    case_inputs[("ElastoDyn","FlapDOF2")]    = {'vals':["True"], 'group':0}
    case_inputs[("ElastoDyn","EdgeDOF")]     = {'vals':["True"], 'group':0}
    case_inputs[("ElastoDyn","DrTrDOF")]     = {'vals':["False"], 'group':0}
    case_inputs[("ElastoDyn","GenDOF")]      = {'vals':["True"], 'group':0}
    case_inputs[("ElastoDyn","YawDOF")]      = {'vals':["False"], 'group':0}
    case_inputs[("ServoDyn","PCMode")]       = {'vals':[5], 'group':0}
    case_inputs[("ServoDyn","VSContrl")]     = {'vals':[5], 'group':0}

    case_inputs[("AeroDyn15","WakeMod")]     = {'vals':[1], 'group':0}
    case_inputs[("AeroDyn15","AFAeroMod")]   = {'vals':[2], 'group':0}
    case_inputs[("AeroDyn15","TwrPotent")]   = {'vals':[0], 'group':0}
    case_inputs[("AeroDyn15","TwrShadow")]   = {'vals':['False'], 'group':0}
    case_inputs[("AeroDyn15","TwrAero")]     = {'vals':['False'], 'group':0}
    case_inputs[("AeroDyn15","SkewMod")]     = {'vals':[1], 'group':0}
    case_inputs[("AeroDyn15","TipLoss")]     = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","HubLoss")]     = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","TanInd")]      = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","AIDrag")]      = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","TIDrag")]      = {'vals':['True'], 'group':0}
    case_inputs[("AeroDyn15","IndToler")]    = {'vals':[1.e-5], 'group':0}
    case_inputs[("AeroDyn15","MaxIter")]     = {'vals':[5000], 'group':0}
    case_inputs[("AeroDyn15","UseBlCm")]     = {'vals':['True'], 'group':0}

    case_list, case_name_list = iec.execute(case_inputs=case_inputs)

    # Run FAST cases
    fastBatch = runFAST_pywrapper_batch(FAST_ver='OpenFAST', dev_branch = True)

    fastBatch.post               = return_fname
    fastBatch.debug_level        = 1
    fastBatch.FAST_exe           = 'openfast'   # Path to executable
    fastBatch.FAST_InputFile     = 'OpenFAST_BAR_00.fst'   # FAST input file (ext=.fst)
    fastBatch.FAST_namingOut     = 'BAR00_IEC_run2'
    # fastBatch.FAST_directory     = 'IEA-15-240-RWT/OpenFAST'   # Path to fst directory files
    fastBatch.FAST_directory     = "/projects/windse/egaertne/bar_loads/BAR/OpenFAST_Models/BAR_00/"
    fastBatch.FAST_runDirectory  = 'run_dir/BAR00_IEC_run2/'

    fastBatch.case_list = case_list
    fastBatch.case_name_list = case_name_list
    fastBatch.debug_level = 2

    # Out Channels
    var_out = ["TipDxc1", "TipDyc1", "TipDzc1", "TipDxb1", "TipDyb1", "TipDxc2", "TipDyc2", "TipDzc2", "TipDxb2", "TipDyb2", "TipDxc3", "TipDyc3", "TipDzc3", "TipDxb3", "TipDyb3", "RootMxc1", "RootMyc1", "RootMzc1", "RootMxb1", "RootMyb1", "RootMxc2", "RootMyc2", "RootMzc2", "RootMxb2", "RootMyb2", "RootMxc3", "RootMyc3", "RootMzc3", "RootMxb3", "RootMyb3", "TwrBsMxt", "TwrBsMyt", "TwrBsMzt", "GenPwr", "GenTq", "RotThrust", "RtAeroCp", "RtAeroCt", "RotSpeed", "BldPitch1", "TTDspSS", "TTDspFA", "NacYaw", "Wind1VelX", "Wind1VelY", "Wind1VelZ", "LSSTipMxa","LSSTipMya","LSSTipMza","LSSTipMxs","LSSTipMys","LSSTipMzs","LSShftFys","LSShftFzs"]
    channels = {}
    for var in var_out:
        channels[var] = True
    fastBatch.channels = channels

    #fastBatch.run_serial()
    output = fastBatch.run_multi(iec.cores)


    # results
    outdir    = 'results/BAR00_IEC_run2/'
    outnaming = "BAR00_IEC_run2" + "_outfile_list.dat"
    fname     = os.path.join(outdir, outnaming)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    output = [os.path.abspath(file) for file in output]
    np.savetxt(fname, output, fmt='%s')

    shutil.copyfile(os.path.join(fastBatch.FAST_runDirectory, "case_matrix.txt"), os.path.join(outdir, "case_matrix.txt"))


if __name__=="__main__":

    steady_results = "/projects/windse/egaertne/bar_loads/results/BAR00_steady_run0/BAR00_steady_run0.yaml"
    init_cond      = load_yaml(steady_results)

    try:
        for var in list(init_cond.keys()):
            init_cond[var] = init_cond[var]['mean']
    except:
        pass

    runFAST_CaseGenIEC(init_cond, offshore=False)


