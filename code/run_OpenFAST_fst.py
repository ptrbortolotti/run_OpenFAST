from wisdem.aeroelasticse.runFAST_pywrapper import runFAST_pywrapper


if __name__=="__main__":

    FAST_ver = 'OpenFAST'
    dev_branch = True
    
    # channels = {"GenPwr"   : True, "HSShftTq" : True, "HSSBrTq"  : True, "GenSpeed" : True, "RotSpeed" : True, "TSR"      : True, "TeetDefl" : True, "Azimuth"  : True, "NacYaw"   : True, "TTDspFA"  : True, "TTDspSS"  : True, "NcIMUTAxs": True, "NcIMUTAys": True, "BldPitch2": True, "OoPDefl1" : True, "OoPDefl2" : True, "OoPDefl3" : True, "TipClrnc1": True, "TipClrnc2": True, "TipClrnc3": True, "TipDxb1"  : True, "TipDxb2"  : True, "TipDxb3"  : True, "Spn1MLxb1": True, "Spn2MLxb1": True, "Spn3MLxb1": True, "Spn4MLxb1": True, "Spn5MLxb1": True, "Spn6MLxb1": True, "Spn7MLxb1": True, "Spn8MLxb1": True, "Spn9MLxb1": True, "Spn1MLyb1": True, "Spn2MLyb1": True, "Spn3MLyb1": True, "Spn4MLyb1": True, "Spn5MLyb1": True, "Spn6MLyb1": True, "Spn7MLyb1": True, "Spn8MLyb1": True, "Spn9MLyb1": True, "Spn1MLzb1": True, "Spn2MLzb1": True, "Spn3MLzb1": True, "Spn4MLzb1": True, "Spn5MLzb1": True, "Spn6MLzb1": True, "Spn7MLzb1": True, "Spn8MLzb1": True, "Spn9MLzb1": True, "Spn1FLxb1": True, "Spn2FLxb1": True, "Spn3FLxb1": True, "Spn4FLxb1": True, "Spn5FLxb1": True, "Spn6FLxb1": True, "Spn7FLxb1": True, "Spn8FLxb1": True, "Spn9FLxb1": True, "Spn1FLyb1": True, "Spn2FLyb1": True, "Spn3FLyb1": True, "Spn4FLyb1": True, "Spn5FLyb1": True, "Spn6FLyb1": True, "Spn7FLyb1": True, "Spn8FLyb1": True, "Spn9FLyb1": True, "Spn1FLzb1": True, "Spn2FLzb1": True, "Spn3FLzb1": True, "Spn4FLzb1": True, "Spn5FLzb1": True, "Spn6FLzb1": True, "Spn7FLzb1": True, "Spn8FLzb1": True, "Spn9FLzb1": True, "RootFxc1" : True, "RootFxc2" : True, "RootFxc3" : True, "RootFyc1" : True, "RootFyc2" : True, "RootFyc3" : True, "RootFxb1" : True, "RootFxb2" : True, "RootFxb3" : True, "RootFyb1" : True, "RootFyb2" : True, "RootFyb3" : True, "RootFzb1" : True, "RootFzb2" : True, "RootFzb3" : True, "RootMxc1" : True, "RootMxc2" : True, "RootMxc3" : True, "RootMyc1" : True, "RootMyc2" : True, "RootMyc3" : True, "RootMxb1" : True, "RootMxb2" : True, "RootMxb3" : True, "RootMyb1" : True, "RootMyb2" : True, "RootMyb3" : True, "RootMzb1" : True, "RootMzb2" : True, "RootMzb3" : True, "YawBrFxn" : True, "YawBrFyn" : True, "YawBrFzn" : True, "YawBrFxp" : True, "YawBrFyp" : True, "YawBrMxn" : True, "YawBrMyn" : True, "YawBrMzn" : True, "YawBrMxp" : True, "YawBrMyp" : True, "RotThrust": True, "LSShftTq" : True, "LSShftFxa": True, "LSShftFya": True, "LSShftFza": True, "LSShftFys": True, "LSShftFzs": True, "LSShftMxa": True, "LSSTipMya": True, "LSSTipMza": True, "LSSTipMys": True, "LSSTipMzs": True, "TwrBsFxt" : True, "TwrBsFyt" : True, "TwrBsFzt" : True, "TwrBsMxt" : True, "TwrBsMyt" : True}
    
    
    fast = runFAST_pywrapper(FAST_ver=FAST_ver, dev_branch=dev_branch, debug_level=2)
    # fast = runFAST_pywrapper(FAST_ver=FAST_ver, dev_branch=dev_branch, debug_level=2, channels=channels)

    fast.FAST_exe = '/mnt/c/Material/Programs/openfast/build/glue-codes/openfast/openfast'   # Path to executable
    fast.FAST_InputFile = 'RotorSE_FAST_BAR_005a.fst'   # FAST input file (ext=.fst)
    fast.FAST_directory = '/mnt/c/Material/Projects/RefTurbines/BAR/OpenFAST_BAR005a'   # Path to fst directory files
    fast.FAST_runDirectory = 'temp'
    fast.FAST_namingOut = 'test_1'

    fast.execute()