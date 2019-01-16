# def tuplePath():
#     """ """
#     return '/home/vitaly/Documents/Students/Kristina/DsJ/tuples'

# def tupleList(type, exp):
#     """ TODO: implement parameters """
#     tpath = tuplePath()
#     return sorted([f for f in listdir(tpath) if isfile(join(tpath, f))])

def makeCanvas(name):
    """ Makes new TCanvas """
    c1 = TCanvas(name, name, 200, 10, 800, 600)
    c1.SetGrid()
    return c1

def countDsModes(t):
    """ Count Ds modes """
    nev = [t.Draw('m', 'mode==' + str(mode) + ' && ds_gen.flag>0') for mode in [0, 1, 2]]
    mdict = dict(zip(['phi pi+', 'K*0 K+', 'Ks0 K+'], nev))
    print('Ds modes')
    for mode, nev in mdict.iteritems():
        print(mode + ': ' + str(nev))
    return mdict

def drawDsMass(t, mode):
    """ m(Ds) plot """
    c1 = makeCanvas('c1')
    nev = t.Draw('m', 'mode==' + str(mode) + ' && ds_gen.flag==1')
    print(str(nev) + ' events selected')
    c1.Print('hist_m' + str(mode) + '.png')
    raw_input("Press Enter to continue...")



    # tuples = tupleList('genMC', 7)
    
    # mdict = countDsModes(dst)
    # for idx, (mode, nev) in enumerate(mdict.iteritems()):
    #     if nev > 0:
    #         print(mode)
    #         drawDsMass(dst, idx)