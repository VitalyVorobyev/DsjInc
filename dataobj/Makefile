Sources=dsjinc_evt.h dsjinc_mcevt.h ds_evt.h ds_mcevt.h

INC=-I/home/belle/vitaly/belle/include

dsjinc_evt_dict.cc: $(Sources)
	rootcint -f $@ -c $(INC) -p $^

