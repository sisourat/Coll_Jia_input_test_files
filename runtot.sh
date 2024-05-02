date
#cd /public/home/du16005/quantumpackage/He2+HeSSP/SSP
#./det_generateHe.sh
#cp det_total_he.dat /public/home/du16005/quantumpackage/He2+HeSSP/det_total.dat
#cd /public/home/du16005/quantumpackage/He2+HeSSP/

TEZFIO=He.ezfio/
PEZFIO=He.ezfio/

rm -r ints/ tinput_sta/ pinput_sta/
rm -r coll_input_phis2e_int_2e/
rm -r He.ezfio
rm fort.*
source /home/nico/Workspace/Progs/qp2/quantum_package.rc
qp create_ezfio -b "test" He.xyz -o He.ezfio
qp run scf
qp set cippres_20240414 finput_cippres he.xml

#qp set electrons elec_alpha_num 1
#qp set electrons elec_beta_num 0

qp run cippres_gencsf
qp set cippres_20240414 ifcsf 1
#qp set cippres ici1 1
#qp set cippres ici2 1
qp set cippres n_sta_cistate_analysis 3
qp run cippres_runci

echo "SETUP COLL"
qp set cippres_20240414 finput_coll cinput.xml
qp run cippres_setup_collision

cp cistates_det.txt He.ezfio/
python3.10 from_qp2_to_twoeint_input_t.py $TEZFIO t

################################################
python3.10 from_qp2_to_twoeint_input_p.py $PEZFIO p
## be careful: for P, it's wrong now, you need
## change something like the charge and others...

mkdir tinput_sta/
mkdir pinput_sta/
mkdir ints/
cp det_total.dat ints/

mv taobasis0.bas tinput_sta/
mv tinput.xml tinput_sta/
cp tmobasis.txt tinput_sta/
mv tmobasis.txt tinput_sta/tmo.txt
cp tcistates_det.txt ints/
mv tcistates_det.txt tinput_sta/

mv paobasis0.bas pinput_sta/
mv pinput.xml pinput_sta/
cp pmobasis.txt pinput_sta/
mv pmobasis.txt pinput_sta/pmo.txt
cp pcistates_det.txt ints/
mv pcistates_det.txt pinput_sta/

#qp set_file He.ezfio
#qp run cippres_two_e_int
#mv twoe_int_test.txt ./ints/twoe_int_tttt.txt 

#qp set_file He.ezfio
#qp run cippres_two_e_int
#mv twoe_int_test.txt ./ints/twoe_int_pppp.txt

echo "RUN PHIS2E"
/home/nico/Workspace/Progs/Coll_Jia/code-2e/phis2e cinput -rep
qp set_file $TEZFIO
qp run print_h1emo
mv h1emo.txt ./ints/h1emo_tt.txt
qp set_file $PEZFIO
qp run print_h1emo
mv h1emo.txt ./ints/h1emo_pp.txt

mv cinput_int_2e/impactb_* ./ints/
#mv coll_input_phis2e_int_2e/twoe_int* ints
#cp ints/twoe_int_tttt.txt ints/twoe_int_pppp.txt
#mv coll_input_phis2e_int_2e/onee_int_pp.txt ints
#mv coll_input_phis2e_int_2e/twoe_int_tttt.txt ints
#rm -r coll_input_phis2e_int_2e/

qp set_file He.ezfio
qp run cippres_two_e_int
cp twoe_int_test.txt ./ints/twoe_int_tttt.txt
cp ints/twoe_int_tttt.txt ints/twoe_int_pppp.txt

qp set_file He.ezfio
qp run cippres_prop_collision_jia

date
