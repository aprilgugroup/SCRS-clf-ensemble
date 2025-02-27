#!/bin/bash

log_dir=".log" # ouput log directory
out_dir="output/zj/t1_cross_phase"
mkdir -p $log_dir
mkdir -p $out_dir

for training_dataset in {zj-exponential,zj-stationary-1,zj-stationary-2,zj-stationary-3}; do
	for testing_dataset in {zj-exponential,zj-stationary-1,zj-stationary-2,zj-stationary-3}; do
		if [[ "$training_dataset" != "$testing_dataset" ]]; then
			for dr in {none,kpca,lda,ism_sdr,pca,sup_pca}; do
				for cls in {gnb,knn,lda,lr,rf,svm_lin,svm_rbf,svm_lin_cv,svm_rbf_cv,nn}; do
					alloc_param="-p short -N1 -c1 --mem 16G --time 24:00:00"
					job_desc="$training_dataset.$dr.$cls.$testing_dataset"
					sbatch -J $job_desc \
						-o "$log_dir/"$job_desc".log" \
						-e "$log_dir/"$job_desc".err" \
						$alloc_param "$@" \
						--wrap \
"# run experiments #
echo \$SLURM_JOB_ID >&2
. /home/li.gua/.local/env/python-3.10-venv/bin/activate

python3 ./script/t1_methods_cross_dataset.py \\
	--training-dataset $training_dataset \\
	--testing-dataset $testing_dataset \\
	--dimreducer $dr \\
	--reduce-dim-to 35 \\
	--classifier $cls \\
	--output ${out_dir}/${job_desc}.json

deactivate"
				done
			done
		fi
	done
done
