#! /usr/bin/env python3
# R. Ruiz, C. Ramos
# 2026 September
# Purpose: Copy MadGraph5_aMC@NLO decay-width scan files
# into a common directory with more convenient names.
# IMPORTANT: set mg5 path

import os
import shutil


def main(kIsDebug=True):
    # file/path names
    mg5Path = '/Users/ramos/mg5amcnlo'
    basePathName = 'ScotoLHC'

    decayList = ['ZtoNutNutbarN1N1','ZtoTauTauN1N1']

    baseOutName = 'mg5amc_ScotoScan'
    baseEnd = '.txt'

    # input/output list
    targetList = []
    outFileList = []

    # find scan files
    for decay in decayList:

        # build process directory name
        procName = '_'.join([basePathName,'decay' + decay])

        if kIsDebug:
            print(f'Working on process {procName}')

        # build path to Events directory
        targetPath = os.path.join(mg5Path,procName,'Events')

        # find scan output file
        dirContent = os.listdir(targetPath)
        scanFile = None

        for item in dirContent:
            if item.startswith('scan_run_') and item.endswith('.txt'):
                scanFile = item
                break

        if scanFile is None:
            raise FileNotFoundError(f'No scan output file found in {targetPath}')

        targetPath = os.path.join(targetPath, scanFile)

        # build output file name
        targetOutput = f'{baseOutName}_decay{decay}{baseEnd}'

        targetList.append(targetPath)
        outFileList.append(targetOutput)

        if kIsDebug:
            print(f'Scan input file is {targetPath}')
            print(f'Scan output file is {targetOutput}')

    # sanity check
    assert len(targetList) == len(outFileList)
    print('building path names successful')

    # write output
    if not kIsDebug:

        outDir = os.path.join(os.getcwd(),'data_files','data_decay')

        os.makedirs(outDir, exist_ok=True)

        # copy over files
        for i, o in zip(targetList, outFileList):
            print(f'copying {i} to {o}')
            shutil.copy(i, os.path.join(outDir, o))

        print('Output files:')
        for f in os.listdir(outDir):
            print(f)


if __name__ == '__main__':
    main(kIsDebug=False)
    print('have a nice day!')
