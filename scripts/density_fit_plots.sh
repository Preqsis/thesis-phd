PYTHON_DIR=../python
DATA_DIR=/home/preqsis/DATA/sim-thesis

# C2
python $PYTHON_DIR/plot_mean_density_fit.py --plot_file ../img/plot_c2_mean_density_fit.pdf --data_file $DATA_DIR/c2_42x265/sim.h5 --id C2

# C3
python $PYTHON_DIR/plot_mean_density_fit.py --plot_file ../img/plot_c3_mean_density_fit.pdf --data_file $DATA_DIR/c3_42x265/sim.h5 --id C3

# C4
python $PYTHON_DIR/plot_mean_density_fit.py --plot_file ../img/plot_c4_mean_density_fit.pdf --data_file $DATA_DIR/c4_42x265/sim.h5 --id C4
