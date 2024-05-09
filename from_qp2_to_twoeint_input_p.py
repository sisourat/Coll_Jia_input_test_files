import sys
import numpy as np
import gzip
from printout import *

# from xyz.txt to input.xml
dir_ezfio = sys.argv[1]
partner = str(sys.argv[2])

fxyz = gzip.open(dir_ezfio+"nuclei/nucl_coord.gz","rt")
n = int(fxyz.readline().split()[0])
ncent = int(fxyz.readline().split()[0])
xyz = np.zeros((ncent,3))
for j in range(3):
 for i in range(ncent):
  w = fxyz.readline().split()
  xyz[i][j]=w[0]

fcharge = gzip.open(dir_ezfio+"nuclei/nucl_charge.gz","rt")
n = int(fcharge.readline().split()[0])
n = int(fcharge.readline().split()[0])


felecalpha = open(dir_ezfio+"electrons/elec_alpha_num","rt")
elec_alpha_num = int(felecalpha.readline().split()[0])
felecbeta = open(dir_ezfio+"electrons/elec_beta_num","rt")
elec_beta_num = int(felecbeta.readline().split()[0])
felecalpha.close()
felecbeta.close()

fxml = open(partner+"input.xml","w")
print("<GetStaInput>", file=fxml)
for i in range(ncent):
 print(" ", file=fxml)
 print("  <Center>", file=fxml)
 print("     <Position  x='"+str(xyz[i][0])+"' y='"+str(xyz[i][1])+"' z='"+str(xyz[i][2])+"' />" , file=fxml)
 print("     <Basisset file='./"+partner+"aobasis"+str(i)+".bas' />", file=fxml)
 w =  fcharge.readline().split()[0]
 print("     <Potential charge='"+str(w[0])+"' exponent='0.0' />", file=fxml)
 #print("     <Potential charge='2' exponent='0.0' />", file=fxml)
 print("  </Center>", file=fxml)
print(" ", file=fxml)
print("</GetStaInput>", file=fxml)

fxyz.close()
fxml.close()
fcharge.close()

## create aobasis.bas 

fbasnucl = gzip.open(dir_ezfio+"ao_basis/ao_nucl.gz","rt")
n = int(fbasnucl.readline().split()[0])
nao = int(fbasnucl.readline().split()[0])
aonucl = np.zeros(nao, dtype=int)
nao_per_center = np.zeros(ncent, dtype=int)
for j in range(nao):
  aonucl[j]=int(fbasnucl.readline().split()[0] )-1
  nao_per_center[aonucl[j]]+=1

fbaspow = gzip.open(dir_ezfio+"ao_basis/ao_power.gz","rt")
n = int(fbaspow.readline().split()[0])
n = int(fbaspow.readline().split()[0])

aopow = np.zeros((nao,3), dtype=int)
for i in range(3):
 for j in range(nao):
  aopow[j][i]=int(fbaspow.readline().split()[0] )

fbas = gzip.open(dir_ezfio+"ao_basis/ao_expo.gz","rt")
n = int(fbas.readline().split()[0])
n = int(fbas.readline().split()[0])
expao = np.zeros(nao)
for j in range(nao):
 w = float(fbas.readline().split()[0])
 expao[j] = w

fbascoef = gzip.open(dir_ezfio+"ao_basis/ao_coef.gz","rt")
n = int(fbascoef.readline().split()[0])
n = int(fbascoef.readline().split()[0])
for j in range(nao):
 w = float(fbascoef.readline().split()[0])
 if(not(w==1.0)):
  print("AO Coeffs should all be equal to 1, I stop")
#  sys.exit()
#### ccjia comment

aopow_cent = []
expao_cent = []
for k in range(ncent):
 aopow_temp = []
 expao_temp = []
 for j in range(nao): 
  if(aonucl[j]==k):
   aopow_temp.append(np.sum(aopow[j]))
   expao_temp.append(expao[j])
 aopow_cent.append(aopow_temp)
 expao_cent.append(expao_temp)

 gtos = []
 gtop = []
 gtod = []
 gtof = []
 gtog = []
 gtoh = []
 for j in range(nao_per_center[k]):
  if(aopow_cent[k][j]==0):
    gtos.append(expao_cent[k][j])
  elif(aopow_cent[k][j]==1):
    exist_count = gtop.count(expao_cent[k][j])
    if(not(exist_count)): 
     gtop.append(expao_cent[k][j])
  elif(aopow_cent[k][j]==2):
    exist_count = gtod.count(expao_cent[k][j])
    if(not(exist_count)): 
     gtod.append(expao_cent[k][j])
  elif(aopow_cent[k][j]==3):
    exist_count = gtof.count(expao_cent[k][j])
    if(not(exist_count)): 
     gtof.append(expao_cent[k][j])
  elif(aopow_cent[k][j]==4):
    exist_count = gtog.count(expao_cent[k][j])
    if(not(exist_count)): 
     gtog.append(expao_cent[k][j])
  elif(aopow_cent[k][j]==5):
    exist_count = gtoh.count(expao_cent[k][j])
    if(not(exist_count)): 
     gtoh.append(expao_cent[k][j])

printgto(k,gtos,gtop,gtod,gtof,gtog,gtoh,partner)

fxml = open(partner+"mobasis.txt","w")
fmobas = gzip.open(dir_ezfio+"mo_basis/mo_coef.gz","rt")
n = int(fmobas.readline().split()[0])
nmo = int(fmobas.readline().split()[1])
#nmo = 2
print(nmo, nao, file=fxml)
#coef = np.zeros((nmo,nao))
for i in range(nmo):
 for j in range(nao):
  w = float(fmobas.readline().split()[0])
  print(w, file=fxml)
#  coef[i][j] = w


# READS THE DETERMINANTS OF CISTATES 1 
fcistate1 = open(dir_ezfio+"cistates_det.txt","rt")
fcis = open(partner+"cistates_det.txt","w")
mo_num, ndets1, nstate1 = ( int(x) for x in fcistate1.readline().split())
print(mo_num, ndets1, nstate1, file=fcis)
#print(elec_alpha_num, elec_beta_num, file=fcis)
print(0, 0, file=fcis)
dets_alp1 = []
dets_bet1 = []
for i in range(ndets1):
  fcistate1.readline()
  deta = []
  l = fcistate1.readline().split()
  deta += [ i for i in range(len(l[0])) if (l[0][i]=='+')]
  detb = []
  l = fcistate1.readline().split()
  detb += [ i for i in range(len(l[0])) if (l[0][i]=='+')]
  print(1.0, " ".join(map(str,deta)), " ".join(map(str,detb)), file=fcis)

# READS THE CI COEFFS
for i in range(nstate1):
  d = fcistate1.readline().split()
  esta1 = float(d[0])
  print(" ", file=fcis)
  print(esta1, file=fcis)
  for j in range(ndets1):
   d = fcistate1.readline().split()[0]
   print(d, end=" ", file=fcis)






