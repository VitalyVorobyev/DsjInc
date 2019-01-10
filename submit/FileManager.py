""" BASF script generators

  Author: Vitaly Vorobyev (vvorob@inp.nsk.su)
  Date: Sept.-Dec. 2018

"""

from glob import glob

anal_dir = '/home/belle/vitaly/work/DsjInc'
stor_dir = '/gpfs/fs02/belle/users/vitaly/DsjInc'

class FileManager(object):
    """ """
    def __init__(self, name, adir=None, sdir=None):
        """ Constructor
            Args:
                - name: module name
        """
        self.adir  = anal_dir if adir is None else adir
        self.sdir  = stor_dir if sdir is None else sdir
        self.scrdir = '/'.join([self.adir, 'scripts'])
        self.logdir = '/'.join([self.adir, 'logs'])
        self.name  = name

    def dataPaths(self, dtype, exp, rs, re, skm='HadronBorJ', dt='Any', bl='caseB'):
        """ Returns dict with
            - [procurl, logfile and outfile] for skim
            - [procevt, logfile and outfile] for tuple
        """
        self.pdict = {
            'ex'  : str(exp), 'rs'  : str(rs), 're'  : str(re),
            'skm' : skm,      'dt'  : dt,      'bl'  : bl
        }
        return self.__dataNT() if dtype == 'tuple' else self.__dataSkim()

    def genPaths(self, dtype, exp, rs, re, ty, st, dt='Any', bl='caseB'):
        """ """
        self.pdict = {
            'ex' : str(exp), 'rs' : str(rs),
            're' : str(re),  'st' : str(st) if exp > 30 else str(st + 10),
            'ty' : ty,       'dt' : dt, 'bl' : bl
        }
        return self.__genmcNT() if dtype == 'tuple' else self.__genmcSkim()

    def sigMCPaths(self, ty, st, exp):
        """ Args:
            ty: 'ds', 'dsst0' or 'dsst1'
            st: int - stream number
        """
        self.pdict = {'ty' : ty, 'st' : str(st), 'ex' : str(exp)}
        return self.__pathdict(
            self.__sigMdstFiles(),
            self.__sigLogFile(),
            self.__sigTupleFile(),
            self.__sigScriptFile()
        )

    def __pathdict(self, procevt='', logfile='', outfile='', scrfile=''):
        return {
            'procevt' : procevt,  # process event line
            'logfile' : logfile,  # log file
            'outfile' : outfile,  # output file
            'scrfile' : scrfile   # script file
        }

    def __sigMdstFiles(self):
        """ List of mdst files for signal MC """
        fdir = '/'.join([self.sdir, 'SigMC', self.pdict['ty'], 's' + self.pdict['st']])
        fpat = '_'.join(['evtgen', 'exp', self.pdict['ex'], self.pdict['ty'] + 'Inc-*.mdst'])
        return glob('/'.join([fdir, fpat]))

    def __sigLogFile(self):
        """ Log file for sinal MC """
        return '/'.join([self.logdir,
                    '_'.join([self.name, 'sigmc', self.__pdictToInfoSigMC()]) + '.txt'])

    def __sigTupleFile(self):
        """ Signal MC tuple file """
        return '/'.join([self.sdir, 'signt',
                    '_'.join([self.name, 'sigmc', self.__pdictToInfoSigMC()]) + '.root'])

    def __sigScriptFile(self):
        """ Data script file """
        return '/'.join([self.scrdir,
                    '_'.join([self.name, 'sigmc', self.__pdictToInfoSigMC()]) + '.csh'])

    def __dataSkim(self):
        """ """
        return self.__pathdict(
            self.__processUrlData(),
            self.__dataSkimLogFile(),
            self.__dataSkimFile(),
            self.__dataSkimScriptFile(),
            )

    def __dataNT(self):
        """ """
        return self.__pathdict(
            self.__dataSkimFile(),
            self.__dataTupleLogFile(),
            self.__dataTupleFile(),
            self.__dataTupleScriptFile(),
            )

    def __genmcSkim(self):
        """ """
        return self.__pathdict(
            self.__processUrlGenMC(),
            self.__genmcSkimLogFile(),
            self.__genmcSkimFile(),
            self.__genmcSkimScriptFile(),
            )

    def __genmcNT(self):
        """ """
        return self.__pathdict(
            self.__genmcTupleFile(),
            self.__genmcTupleLogFile(),
            self.__genmcTupleFile(),
            self.__genmcTupleScriptFile(),
            )

    def __pdictToURL(self):
        """ """
        return '&'.join(['='.join([key, val]) if key != 'ty' else 'ty=evtgen-' + val\
                         for key, val in self.pdict.iteritems()])

    def __pdictToInfoSigMC(self):
        """ """
        return '_'.join([key + self.pdict[key] for key in ['ty', 'st', 'ex']])

    def __pdictToInfoData(self):
        """ """
        return '_'.join([key + self.pdict[key] for key in ['ex', 'rs', 're']])

    def __pdictToInfoGenMC(self):
        """ """
        return '_'.join([key + self.pdict[key] if key != 'ty' else self.pdict[key]\
                        for key in ['ty', 'st', 'ex', 'rs', 're']])

    def __processUrlData(self):
        """ """
        return 'http://bweb3/mdst.php?' + self.__pdictToURL()

    def __processUrlGenMC(self):
        """ process url string for generic MC """
        return 'http://bweb3/montecarlo.php?' + self.__pdictToURL()

    def __dataSkimFile(self):
        """ Data skim file """
        return '/'.join([self.sdir, 'dataskim', '_'.join([self.name, 'data', self.__pdictToInfoData()]) + '.index'])

    def __dataSkimLogFile(self):
        """ Data skim file """
        return '/'.join([self.logdir,
                    '_'.join([self.name, 'data', self.__pdictToInfoData()]) + '.txt'])

    def __dataSkimScriptFile(self):
        """ Data script file """
        return '/'.join([self.scrdir,
                    '_'.join([self.name, 'data', self.__pdictToInfoData()]) + '.csh'])

    def __dataTupleFile(self):
        """ Data tuple file """
        return '/'.join([self.sdir, 'datant',
                    '_'.join([self.name, 'data', self.__pdictToInfoData()]) + '.root'])

    def __dataTupleLogFile(self):
        """ Data tuple log file """
        return '/'.join([self.logdir,
                    '_'.join([self.name, 'datant', self.__pdictToInfoData()]) + '.txt'])

    def __dataTupleScriptFile(self):
        """ Data tuple script file """
        return '/'.join([self.scrdir,
                     '_'.join([self.name, 'datant', self.__pdictToInfoData()]) + '.csh'])

    def __genmcSkimFile(self):
        """ """
        return '/'.join([self.sdir, 'genskim', 's' + self.pdict['st'],
                    '_'.join([self.name, self.__pdictToInfoGenMC()]) + '.index'])

    def __genmcSkimLogFile(self):
        """ """
        return '/'.join([self.logdir,
                    '_'.join([self.name, 'skim', self.__pdictToInfoGenMC()]) + '.txt'])

    def __genmcSkimScriptFile(self):
        """ """
        return '/'.join([self.scrdir,
                    '_'.join([self.name, 'skim', self.__pdictToInfoGenMC()]) + '.csh'])

    def __genmcTupleFile(self):
        """ """ 
        return '/'.join([self.sdir, 'gennt', 's' + self.pdict['st'],
                    '_'.join([self.name, self.__pdictToInfoGenMC()]) + '.root'])

    def __genmcTupleLogFile(self):
        """ """
        return '/'.join([self.logdir,
                    '_'.join([self.name, 'nt', self.__pdictToInfoGenMC()]) + '.txt'])

    def __genmcTupleScriptFile(self):
        """ """
        return '/'.join([self.scrdir,
                    '_'.join([self.name, 'nt', self.__pdictToInfoGenMC()]) + '.csh'])

def main():
    """ Unit test """
    fm = FileManager('dsjinc')
    print('FileManager test: skim')
    print('  ** data paths **')
    for key, val in fm.dataPaths('skim', 7, 13, 39).iteritems():
        print('   {0} : {1}'.format(key, val))
    print('  ** genmc paths **')
    for key, val in fm.genPaths('skim', 7, 13, 39, 'charm', 1).iteritems():
        print('   {0} : {1}'.format(key, val))
   
    print('FileManager test: tuple')
    print('  ** data paths **')
    for key, val in fm.dataPaths('tuple', 7, 13, 39).iteritems():
        print('   {0} : {1}'.format(key, val))
    print('  ** genmc paths **')
    for key, val in fm.genPaths('tuple', 7, 13, 39, 'charm', 1).iteritems():
        print('   {0} : {1}'.format(key, val))

if __name__ == '__main__':
    main()
