import sys
import numpy as np

def printgto(i, gtos, gtop, gtod, gtof, gtog, gtoh,partner):

 fcol=open(partner+'aobasis'+str(i)+'.bas','w')

 if(len(gtos)>0):
  print("! s functions", file=fcol)
  print("H", len(gtos), len(gtos), file=fcol)
  for i in range(len(gtos)):
   c = np.zeros(len(gtos))
   c[i]=1.0
   print(gtos[i],' '.join(map(str, c)), file=fcol)
 
 if(len(gtop)>0):
  print(" ", file=fcol)
  print("! p functions", file=fcol)
  print("H", len(gtop), len(gtop), file=fcol)
  for i in range(len(gtop)):
   c = np.zeros(len(gtop))
   c[i]=1.0
   print(gtop[i],' '.join(map(str, c)), file=fcol)
 
 if(len(gtod)>0):
  print(" ", file=fcol)
  print("! d functions", file=fcol)
  print("H", len(gtod), len(gtod), file=fcol)
  for i in range(len(gtod)):
   c = np.zeros(len(gtod))
   c[i]=1.0
   print(gtod[i],' '.join(map(str, c)), file=fcol)

 if(len(gtof)>0):
  print(" ", file=fcol)
  print("! f functions", file=fcol)
  print("H", len(gtof), len(gtof), file=fcol)
  for i in range(len(gtof)):
   c = np.zeros(len(gtof))
   c[i]=1.0
   print(gtof[i],' '.join(map(str, c)), file=fcol)

 if(len(gtog)>0):
  print(" ", file=fcol)
  print("! g functions", file=fcol)
  print("H", len(gtog), len(gtog), file=fcol)
  for i in range(len(gtog)):
   c = np.zeros(len(gtog))
   c[i]=1.0
   print(gtog[i],' '.join(map(str, c)), file=fcol)

 if(len(gtoh)>0):
  print(" ", file=fcol)
  print("! h functions", file=fcol)
  print("H", len(gtoh), len(gtoh), file=fcol)
  for i in range(len(gtoh)):
   c = np.zeros(len(gtoh))
   c[i]=1.0
   print(gtoh[i],' '.join(map(str, c)), file=fcol)
 

 fcol.close()
 return 0
