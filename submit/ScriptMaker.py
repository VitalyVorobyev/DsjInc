""" BASF script generators

# Author: Vitaly Vorobyev (vvorob@inp.nsk.su)
# First version: September 2018
#   Last update: January 2019

"""

import os
from subprocess import call
from LumiAnalyzer import LumiAnalyzer
from FileManager import FileManager
import itertools

class ScriptWriter(object):
    """ """
    def __init__(self, name, queue='s', chdir=True, size=3000):
        """ Constructor 
            Args:
                - name: module name
        """
        self.fmgr = FileManager(name)
        if chdir:
            os.chdir(self.fmgr.adir)
        self.name = name
        self.size = size
        self.queue = queue

    def __writeHead(self):
        """ Write script header """
        self.f.write('\n'.join([
            '#! /bin/csh -f\n',
            'setenv USE_GRAND_REPROCESS_DATA 1',
            'source /sw/belle/local/etc/cshrc_general',
        '\n']))

    def __writePath(self, dtype, logfile):
        """ Write module path
            Args:
                dtype: 'skim' or 'tuple'
        """
        self.f.write('\n'.join([
            'basf <<EOF >& ' + logfile,
            'path create main',
            'path add_module main fix_mdst',
            'path create analysis',
            'path add_condition main <=:0:KILL',
            'path add_condition main >:0:analysis',
            'path add_module analysis ' + self.name + '\n',
        ]))
        if dtype is 'skim':
            self.f.write('path add_module analysis user_index\n')
        self.f.write('path add_condition analysis <=:0:KILL\n')
        self.f.write('initialize\n')

    def __writeModulePars(self, name, pdict):
        """ Module parameters """
        for key, val in pdict.iteritems():
            self.f.write('module put_parameter ' + name + ' ' + key + '\\' + val + '\n')

    def __writeFixMdstPars(self):
        """ fix_mdst module params """
        pdict = {
            'Make_pi0_option'      :  '2',
            'Make_pi0_lower_limit' : '-3.0',
            'Make_pi0_upper_limit' :  '3.0'}
        self.__writeModulePars('fix_mdst', pdict)

    def __makeScript(self, mode, dtype, pardict, exp, runs, rune, stream=None, gentype=None):
        """ Write generic MC skim or tuple script
        Args:
            mode:     'data', 'genmc' or 'sigmc'
            dtype:    'skim' or 'tuple'
            pardict:  dict of module parameters
            exp:      experiment number
            runs:     run start
            rune:     run end
            stream:   stream number
            gentype:  charm, charged, uds, mixed
        Returns: script file name
        """
        assert(mode in ['data', 'genmc', 'sigmc'])
        assert(dtype in ['skim', 'tuple'])
        if mode is 'genmc':
            paths = self.fmgr.genPaths(dtype, exp, runs, rune, gentype, stream)
        elif mode is 'data':
            paths = self.fmgr.dataPaths(dtype, exp, runs, rune)

        self.f = open(paths['scrfile'], 'w')
        self.__writeHead()
        self.__writePath(dtype, paths['logfile'])
        if dtype is 'tuple':
            self.f.write('nprocess set 0\n')
            pardict['ofile'] = '"' + paths['outfile'] + '"'
        else:
            self.f.write('output open ' + paths['outfile'] + '\n')
        self.__writeFixMdstPars()
        self.__writeModulePars(self.name, pardict)
        if dtype is 'tuple':
            self.f.write('process_event ' + paths['procevt'] + '\n')
        else:
            self.f.write('process_url ' + paths['procevt'] + '\n')
        self.f.write('EOF\n')
        self.f.close()
        call(['chmod', '755', paths['scrfile']])
        return paths['scrfile']

    def __writeScripts(self, mode, dtype, exp, submit, stream=None, gentype=None):
        """ """
        la = LumiAnalyzer()
        runs = la.chopExp(exp, self.size)
        pdict = {
            'mode'        : '2'   if mode  is 'genmc' else '0',
            'ntuple_flag' : '0'   if dtype is 'skim'  else '1',
            'min_ds_mom'  : '1.5' if dtype is 'skim'  else '2.0'
        }
        scripts = []
        for runs, rune in zip(runs[:-1], runs[1:]):
            scripts.append(self.__makeScript(mode, dtype, pdict, exp, runs, rune-1, stream, gentype))
            if submit:
                call(['bsub', '-q', self.queue, scripts[-1]])
        return scripts

    def __writeSigMCScript(self, ty, stream, exp, submit):
        """ """
        paths = self.fmgr.sigMCPaths(ty, stream, exp)
        if not paths['procevt']:
            return
        pdict = {
            'mode'        : '1',  # sigmc
            'ntuple_flag' : '1',
            'min_ds_mom'  : '2.0',
            'ofile'       : paths['outfile']
        }
        self.f = open(paths['scrfile'], 'w')
        self.__writeHead()
        self.__writePath('tuple', paths['logfile'])
        self.f.write('nprocess set 0\n')
        self.__writeFixMdstPars()
        self.__writeModulePars(self.name, pdict)
        for fname in paths['procevt']:
            self.f.write('process_event ' + fname + '\n')
        self.f.write('EOF\n')
        self.f.close()
        call(['chmod', '755', paths['scrfile']])
        if submit:
            call(['bsub', '-q', self.queue, paths['scrfile']])
        return paths['scrfile']

    def writeGenSkimScripts(self, exp, stream, gentype, submit=True):
        """ Proxi for gen skim """
        return self.__writeScripts('genmc', 'skim', exp, submit, stream, gentype)

    def writeGenTupleScripts(self, exp, stream, gentype, submit=True):
        """ Proxi method for gen tuple """
        return self.__writeScripts('genmc', 'tuple', exp, submit, stream, gentype)
    
    def writeDataSkimScripts(self, exp, submit=True):
        """ Proxi for data skim """
        return self.__writeScripts('data', 'skim', exp, submit)
    
    def writeDataTupleScripts(self, exp, submit=True):
        """ Proxi method for data tuple """
        return self.__writeScripts('data', 'tuple', exp, submit)

    def writeSigMCScript(self, ty, stream, exp, submit=True):
        """ Proxi method for sig NM tuple """
        return self.__writeSigMCScript(ty, stream, exp, submit)

def main():
    """ Unit test """
    sw = ScriptWriter('dsjinc')
    la = LumiAnalyzer()
    streams = [0, 1, 2, 3, 4, 5]
    gentypes = ['uds', 'charm', 'mixed', 'charged']
    print('Generating all scripts for data and gen MC...')
    cnt = 0
    for exp in la.expList():
        print('exp {0}'.format(exp))
        cnt = cnt + len(sw.writeDataSkimScripts(exp))
        cnt = cnt + len(sw.writeDataTupleScripts(exp))
        for stream, gentype in itertools.product(streams, gentypes):
            cnt = cnt + len(sw.writeGenSkimScripts(exp, stream, gentype))
            cnt = cnt + len(sw.writeGenTupleScripts(exp, stream, gentype))
        print(' {0} scripts generated'.format(cnt))

if __name__ == '__main__':
    main()
