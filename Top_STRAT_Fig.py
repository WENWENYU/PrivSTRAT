####################
##Generates figure similar to those in the paper
#####################
import sys;
import loadFile as ld;
from MU_STRAT import *;
from DP_util import PickTop as pt;

##
##Sees how much they overlap
##
def inter(a,b):
	if len(a)!=len(b):
		1/0.0;
		return;
	return len([i for i in a if i in b])/float(len(a));


##
##For making pics!
##
def plotTop(mret,eps,filename,binSize=1,savename=""):
	if len(savename)==0:
		savename="OutputDir/res_top_"+str(eps)+"_"+str(mret)+".txt"
	epsilons=[eps*i for i in range(1,11)];
	print "load Data"
	[y,BED]=ld.getData(filename);
	print "calc MU!"
	MU=MU_STRAT(BED,5,binSize=binSize);
	sc=MU.prod(y);
	sc=[abs(s) for s in sc];
	sc=sorted(sc,reverse=True);
	print "get True!";
	if binSize>1:
		binned=True;
	else:
		binned=False
	tru=pt(y,MU,mret,-1,algor="noise",binned=binned);
	neighs=[0.0 for i in range(1,11)];
	score=[0.0 for i in range(1,11)];
	noise=[0.0 for i in range(1,11)];
	reps=20;
	for i in range(0,10):
		e=epsilons[i];
		print e;
		for j in range(0,reps):
			print j;
			gs=pt(y,MU,mret,e,algor="neighbor",binned=binned,reuse=True);
			neighs[i]=neighs[i]+inter(tru,gs)/float(reps);	
			gs=pt(y,MU,mret,e,algor="score",binned=binned);
			score[i]=score[i]+inter(tru,gs)/float(reps);	
			gs=pt(y,MU,mret,e,algor="noise",binned=binned);
			noise[i]=noise[i]+inter(tru,gs)/float(reps);
		
	fil=open(savename,"w");
	fil.write("Testing Top SNPs with DP, "+filename);
	fil.write("\nEpsilon:")
	for i in range(0,10):
		fil.write(" "+str(epsilons[i]))
	fil.write("\nNoise:")
	for i in range(0,10):
		fil.write(" "+str(noise[i]))
	fil.write("\nScore:")
	for i in range(0,10):
		fil.write(" "+str(score[i]))
	fil.write("\nNeighbor:")
	for i in range(0,10):
		fil.write(" "+str(neighs[i]))
	fil.close();



if __name__=="__main__":
	filename="../../GWAS/cleaned"#"TestCases/pop";
	eps={};
	eps=[.5,.5,3.0,3.0];
	mret=[3,5,10,15];
	savename="OutputDir/pop_Top_bin";
	for i in range(0,4):
		plotTop(mret[i],eps[i],filename,binSize=100000,savename=savename+str(mret[i])+".txt");
	print "DONE!!"


