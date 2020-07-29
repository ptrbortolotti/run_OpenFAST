#!/bin/bash
#SBATCH --account=bar
#SBATCH --time=0-24:00:00
#SBATCH --job-name=bar02
#SBATCH --nodes=7
#SBATCH --mail-user pbortolo@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL
####SBATCH --partition=debug
####SBATCH --qos=high
######SBATCH --mem=1000GB      # RAM in MB
#SBATCH --output=job_log.%j.out  # %j will be replaced with the job ID

module purge
module load conda
module load mkl/2019.1.144 cmake/3.12.3
module load gcc/8.2.0

source deactivate
conda activate wisdem-env

mpirun -np 250 python run_OpenFAST_BAR02.py
