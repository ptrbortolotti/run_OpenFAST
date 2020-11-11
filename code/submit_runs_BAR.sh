#!/bin/bash
#SBATCH --account=bar
#SBATCH --time=2-00:00:00
#SBATCH --job-name=bar3
#SBATCH --nodes=7
#SBATCH --mail-user pbortolo@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL
####SBATCH --partition=debug
#######SBATCH --qos=high
######SBATCH --mem=1000GB      # RAM in MB
#SBATCH --output=job_log.%j.out  # %j will be replaced with the job ID

module purge
module use /nopt/nrel/apps/modules/centos74/modulefiles
module load conda
#module load mkl/2019.1.144 cmake/3.12.3
#module load gcc/8.2.0

# source deactivate
source activate /projects/weis/multifidelity/weis-env

# mpirun -np 247 python run_OpenFAST_BAR0.py
# mpirun -np 199 python run_OpenFAST_BAR1.py
# mpirun -np 199 python run_OpenFAST_BAR2.py
mpirun -np 247 python run_OpenFAST_BAR3.py
# mpirun -np 247 python run_OpenFAST_BAR4.py


