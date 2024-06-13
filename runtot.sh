date

# clean old files
rm -r ints/ tinput_sta/ pinput_sta/
rm -r cinput_int_2e/
rm -r He.ezfio
rm fort.*
rm Prop*out
source /home/nico/Workspace/Progs/qp2/quantum_package.rc


# run scf for target and projectile (here same MOs)
qp create_ezfio -b "test" He.xyz -o He.ezfio
qp run scf
qp set cippres finput_cippres he.xml

# setup
TEZFIO=He.ezfio/
PEZFIO=He.ezfio/
#qp set electrons elec_alpha_num 1
#qp set electrons elec_beta_num 0

qp run cippres_gencsf
qp set cippres ifcsf 1
#qp set cippres ici1 1
#qp set cippres ici2 1
qp set cippres n_sta_cistate_analysis 3
qp run cippres_runci

# prepare files for phis2e and coll_jia
################################################
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

qp set_file $TEZFIO
qp run cippres_two_e_int
mv twoe_int_test.txt ./ints/twoe_int_tttt.txt

qp set_file $PEZFIO
qp run cippres_two_e_int
mv twoe_int_test.txt ./ints/twoe_int_pppp.txt

qp set_file $TEZFIO
qp run print_h1emo
mv h1emo.txt ./ints/h1emo_tt.txt
qp set_file $PEZFIO
qp run print_h1emo
mv h1emo.txt ./ints/h1emo_pp.txt

qp set cippres finput_coll cinput.xml

# running the dynamics one b at a time

i=0
for bproj in 0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5 5.0 5.5 6.0 6.5 7.0 7.5 8.0 8.5 9.0 9.5 10.0
 do

  let i++
  sed -e "s/bbb/$bproj/g" cinput.tmp > cinput.xml
  echo "SETUP COLL", $bproj
  qp run cippres_setup_collision

  echo "RUN PHIS2E"
  /home/nico/Workspace/Progs/Coll_Jia/code-2e/phis2e cinput -rep

  mv cinput_int_2e/impactb_* ./ints/

  qp set_file $TEZFIO
  qp run cippres_prop_collision_jia

  if [ "$i" -eq "1" ]
   then
     mv Prop_collision.out Prop_tot.out
   else
     tail -n 1  Prop_collision.out >> Prop_tot.out
   fi

 done
date
