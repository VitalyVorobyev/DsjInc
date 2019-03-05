ids = {
    'Dsj0+'  :  10431,
    'Dsj0-'  : -10431,
    'Dsj1+'  :  20433,
    'Dsj1-'  : -20433,
    'Ds+'    :  431,
    'Ds-'    : -431,
    'Ds*+'   :  433,
    'Ds*-'   : -433,
    'gamma'  :  22,
    'pi0'    :  111,
    'phi'    :  333,
    'pi+'    :  211,
    'pi-'    : -211,
    'K+'     :  321,
    'K-'     : -321,
    'K*0'    :  313,
    'K*0bar' : -313,
    'Ks0'    :  310,
    'Kl0'    :  130,
    'e-'     :   11,
    'e+'     :  -11,
    'nu_e'   :  -12,
    'anti-nu_e' :  12,
    'mu-'     :   13,
    'mu+'     :  -13,
    'nu_mu'   :  -14,
    'anti-nu_mu' :  14,
    'nu_tau'   :  -16,
    'anti-nu_tau' :  16,
    'p' : 2212,
    'anti-p' : -2212,
    'n' : 2112,
    'anti-n' : -2112
}

names = {val : key for key, val in ids.iteritems()}

names_stable  = [
    'gamma',
    'e+', 'e-', 'nu_e', 'anti-nu_e',
    'mu+', 'mu-', 'nu_mu', 'anti-nu_mu',
    'nu_tau', 'anti-nu_tau',
    'pi+', 'pi-', 'K+', 'K-',
    'p', 'anti-p', 'n', 'anti-n',
    'Kl0', 'Ks0', 'Ds+', 'Ds-', 'Ds*+', 'Ds*-',
    'pi0', 'K*0', 'K*0bar', 'phi'
    ]

ids_stable = [ids[name] for name in names_stable]
