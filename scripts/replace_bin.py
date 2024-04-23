import os
from pathlib import Path
import shutil


if __name__ == '__main__':
    rootDir = Path(r'F:\database\BYD\无法复现\shuiniguancheweibao')
    srcDir = rootDir/'bin'
    dstDir = rootDir/'raw'
    Bins = sorted(list(srcDir.glob('*.bin')),key=lambda p: int(str(p).split('.')[0].split('_')[-1]))
    AlgoBins = sorted(list(dstDir.glob('*_Raw_Algo.bin')))
    print('nBins: {} nAlgoBins: {}'.format(len(Bins),len(AlgoBins)))
    lastAlgoBin = AlgoBins[-1]
    print(lastAlgoBin)

    ind = int(str(lastAlgoBin.stem).split('_')[0])
    for bin in Bins[::-1]:
        print(bin)
        dstName = dstDir/'{}_Raw_Algo.bin'.format(ind)
        ind -= 1
        print(dstName)
        shutil.copy(bin,dstName)
