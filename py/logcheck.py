import numpy as np
import matplotlib.pyplot as plt

data = {}
infile = [
        'dsjinc_sigmc_tydsst0_st1_ex55.txt',
        'dsjinc_sigmc_tydsst0IncTest_st0_ex55.txt',
        'dsjinc_sigmc_tydsst0IncPos_st0_ex55.txt',
        'dsjinc_sigmc_tydsst0IncNeg_st0_ex55.txt'
        ]

ppiflags = np.zeros(7, dtype=int)
pkflags  = np.zeros(7, dtype=int)
npiflags = np.zeros(7, dtype=int)
nkflags  = np.zeros(7, dtype=int)

counts = {key : 0 for key in [
    'pi+', 'pi-',
    'K- ', 'K+ ',
    ]}

founds = {key : 0 for key in [
    'Ds0(2317)-', 'Ds0(2317)+',
    'Ds-', 'Ds+',
]}

with open(infile[1]) as f:
    for line in f:
        if ':' in line and len(line.split()) == 2:
            key, val = line.split()
            key = key[:-1]
            val = int(val)
            if key in data:
                data[key].append(val)
            else:
                data[key] = [val]
        elif line.startswith('track'):
            _, _, ch, _, kfl, _, pifl = line.split()
            kfl = int(kfl)
            pifl = int(pifl)
            if ch == '1':
                pkflags[kfl] = pkflags[kfl] + 1
                ppiflags[pifl] = ppiflags[pifl] + 1
            else:
                nkflags[kfl] = nkflags[kfl] + 1
                npiflags[pifl] = npiflags[pifl] + 1
        else:
            for key, val in counts.items():
                if line.startswith('{} count'.format(key)):
                    counts[key] = counts[key] + int(line.split()[-1])
            for key, val in founds.items():
                if line.startswith('{} found'.format(key)):
                    founds[key] = founds[key] + 1

print('Counts')
for key, val in counts.items():
    print('{} : {}'.format(key, val))

print('Finds')
for key, val in founds.items():
    print('{} : {}'.format(key, val))

for key, vec in data.items():
    npvec = np.array(vec)
    print('{:.4f} +- {:.4f} <- {}'.format(np.mean(npvec), np.std(npvec)/np.sqrt(len(npvec)), key))

print('+ K  tracks: {} {}'.format(pkflags, sum(pkflags)))
print('+ pi tracks: {} {}'.format(ppiflags, sum(ppiflags)))
print('- K  tracks: {} {}'.format(nkflags, sum(nkflags)))
print('- pi tracks: {} {}'.format(npiflags, sum(npiflags)))

for key in [('Ds-', 'Ds+'), ('K-', 'K+'), ('K*0', 'K*0bar'), ('pi-', 'pi+')]:
    print(key)
    print([np.mean(data[k]) for k in key])
    plt.figure()
    plt.hist(data[key[0]], alpha=0.5, bins=10, range=[0., 10.])
    plt.hist(data[key[1]], alpha=0.5, bins=10, range=[0., 10.])
    plt.show()
