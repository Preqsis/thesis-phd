DATA_DIR=/home/preqsis/DATA/sim-thesis
MDH=/home/preqsis/Plocha/multilayer-dripping-handrail/bin/mld

# cases
# c1 -> q = 0.1, psi = 0.1
# c2 -> q = 0.1, psi = 0.9
# c3 -> q = 0.9, psi = 0.1
# c4 -> q = 0.9, psi = 0.9

########
# INIT #
########
echo "INIT: q = 0.1; psi = 0.1"
mpirun -n 8 --use-hwthread-cpus --quiet $MDH -v --sim -I 42 -J 265 -n 2e5 -Q 1e14 --T_flow 4500 --m_primary 0.63 --r_in 0.01 --r_out 1.16 -o $DATA_DIR/init_c1_42x265 -q 0.1 -psi 0.1

echo "INIT: q = 0.1; psi = 0.9"
mpirun -n 8 --use-hwthread-cpus --quiet $MDH -v --sim -I 42 -J 265 -n 2e5 -Q 1e14 --T_flow 4500 --m_primary 0.63 --r_in 0.01 --r_out 1.16 -o $DATA_DIR/init_c2_42x265 -q 0.1 -psi 0.9

echo "INIT: q = 0.9; psi = 0.1"
mpirun -n 8 --use-hwthread-cpus --quiet $MDH -v --sim -I 42 -J 265 -n 2e5 -Q 1e14 --T_flow 4500 --m_primary 0.63 --r_in 0.01 --r_out 1.16 -o $DATA_DIR/init_c3_42x265 -q 0.9 -psi 0.1

echo "INIT: q = 0.9; psi = 0.9"
mpirun -n 8 --use-hwthread-cpus --quiet $MDH -v --sim -I 42 -J 265 -n 2e5 -Q 1e14 --T_flow 4500 --m_primary 0.63 --r_in 0.01 --r_out 1.16 -o $DATA_DIR/init_c4_42x265 -q 0.9 -psi 0.9

#######
# SIM #
#######
# echo "SIM: q = 0.1; psi = 0.1"
# mpirun -n 8 --use-hwthread-cpus --quiet $MDH -v --sim --rad --obs -I 42 -J 265 -n 2880 -Q 1e14 --T_flow 4500 --m_primary 0.63 --r_in 0.01 --r_out 1.16 -o $DATA_DIR/c1_42x265 --init_file $DATA_DIR/init_c1_42x265/sim.h5 --init_dkey d99999 -q 0.1 -psi 0.1
#
# echo "SIM: q = 0.1; psi = 0.9"
# mpirun -n 8 --use-hwthread-cpus --quiet $MDH -v --sim --rad --obs -I 42 -J 265 -n 2880 -Q 1e14 --T_flow 4500 --m_primary 0.63 --r_in 0.01 --r_out 1.16 -o $DATA_DIR/c2_42x265 --init_file $DATA_DIR/init_c2_42x265/sim.h5 --init_dkey d99999 -q 0.1 -psi 0.9
#
# echo "SIM: q = 0.9; psi = 0.1"
# mpirun -n 8 --use-hwthread-cpus --quiet $MDH -v --sim --rad --obs -I 42 -J 265 -n 2880 -Q 1e14 --T_flow 4500 --m_primary 0.63 --r_in 0.01 --r_out 1.16 -o $DATA_DIR/c3_42x265 --init_file $DATA_DIR/init_c3_42x265/sim.h5 --init_dkey d99999 -q 0.9 -psi 0.1
#
# echo "SIM: q = 0.9; psi = 0.9"
# mpirun -n 8 --use-hwthread-cpus --quiet $MDH -v --sim --rad --obs -I 42 -J 265 -n 2880 -Q 1e14 --T_flow 4500 --m_primary 0.63 --r_in 0.01 --r_out 1.16 -o $DATA_DIR/c4_42x265 --init_file $DATA_DIR/init_c4_42x265/sim.h5 --init_dkey d99999 -q 0.9 -psi 0.9
