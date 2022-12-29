PYTHON_DIR=../python
DATA_FILE=/home/preqsis/DATA/sim-thesis/extract.h5

# cases
# c1 -> q = 0.1, psi = 0.1
# c2 -> q = 0.1, psi = 0.9
# c3 -> q = 0.9, psi = 0.1
# c4 -> q = 0.9, psi = 0.9

python $PYTHON_DIR/plot_density_temperature.py --data_file $DATA_FILE --plot_file ../img/plot_density_temperature_c1.pdf --dkey init_c1_d72000 

python $PYTHON_DIR/plot_density_temperature.py --data_file $DATA_FILE --plot_file ../img/plot_density_temperature_c2.pdf --dkey init_c2_d199999 

python $PYTHON_DIR/plot_density_temperature.py --data_file $DATA_FILE --plot_file ../img/plot_density_temperature_c3.pdf --dkey c3_d1000 

python $PYTHON_DIR/plot_density_temperature.py --data_file $DATA_FILE --plot_file ../img/plot_density_temperature_c4.pdf --dkey c4_d1000 

# bloby
python $PYTHON_DIR/plot_density_temperature.py --data_file $DATA_FILE --plot_file ../img/plot_density_temperature_c5.pdf --dkey c5_d1000 

python $PYTHON_DIR/plot_density_temperature.py --data_file $DATA_FILE --plot_file ../img/plot_density_temperature_c6.pdf --dkey c6_d1000 

python $PYTHON_DIR/plot_density_temperature.py --data_file $DATA_FILE --plot_file ../img/plot_density_temperature_c7.pdf --dkey c7_d1000 
