#! /usr/bin/env python3
# R. Ruiz, C. Ramos
# 2026 August
# Purpose: To copy over set of files from MadGraph5_aMC@NLO's parameter scan into single directory with (more) sensible names
# Usage: $ python scotoLHC_Copy_Over_Scans.py
# IMPORTANT: set directory where folders with the generated events were stored

import os
import sys
import shutil

def main(kIsDebug=True):
    """function to copy over files from MadGraph5_aMC@NLO's parameter scan into single directory with (more) sensible names"""

    # file/path names
    eventsFoldersPath = '/Users/ramos/mg5amcnlo' # define path where events were generated
    basePathName='ScotoLHC'
    procListNLO = ['NCDY_EtaEta','CCDY_H0HX','DY_EtaEtaV']
    procListXLO = ['AAF_HpHm','GGF_EtaEta']
    orderList=["XLO","NLO"]
    suffixList=['LHC14','LHC100']
    baseOutName='mg5amc_ScotoScan'
    baseEnd='.txt'

    # input/output list to copy
    targetList=[]
    outFileList=[]

    # build XLO path names
    for proc in procListXLO:
        for energy in suffixList:
            # build proc
            procBase = "_".join([proc,orderList[0],energy])
            if(kIsDebug): print("Working on process %s" % procBase)
            
            # build output file
            targetOutput = "_".join([baseOutName,procBase])+baseEnd
            outFileList.append(targetOutput)
            if(kIsDebug): print("Built output file %s" % targetOutput)

            # find input file
            targetPath = "_".join([basePathName,procBase])
            targetPath = os.path.join(eventsFoldersPath,targetPath,"Events")
            dirContent = os.listdir(targetPath)
            for item in dirContent:
                if item[0:8] == 'scan_run':
                    targetPath = os.path.join(targetPath,item)
                    break
            targetList.append(targetPath)
            if(kIsDebug): print("Scan input file is %s" % targetPath)

    # build NLO pathnames
    for proc in procListNLO:
        for energy in suffixList:
            # build proc
            procBase = "_".join([proc,orderList[1],energy])
            if(kIsDebug): print("Working on process %s" % procBase)

            # build output file
            targetOutput = "_".join([baseOutName,procBase])+baseEnd
            targetOutput = targetOutput.replace("NLO","XXX")
            if(kIsDebug): print("Built output name %s" % targetOutput)

            # find input file
            targetPath = "_".join([basePathName,procBase])
            targetPath = os.path.join(eventsFoldersPath,targetPath,"Events")
            dirContent = os.listdir(targetPath)
            for item in dirContent:
                if item[-3:] == "txt":
                    if "LO" in item:
                        targetPathXLO = os.path.join(targetPath,item)
                        targetOutputXLO = targetOutput.replace("XXX","XLO")
                        if(kIsDebug): print("Scan input file is %s" % targetPathXLO)
                        if(kIsDebug): print("Scan output file is %s" % targetOutputXLO)
                        targetList.append(targetPathXLO)
                        outFileList.append(targetOutputXLO)
                    else:
                        targetPathNLO = os.path.join(targetPath,item)
                        targetOutputNLO = targetOutput.replace("XXX","NLO")
                        if(kIsDebug): print("Scan input file is %s" % targetPathNLO)
                        if(kIsDebug): print("Scan output file is %s" % targetOutputNLO)
                        targetList.append(targetPathNLO)
                        outFileList.append(targetOutputNLO)

    # sanity check
    assert len(targetList) == len(outFileList)
    print("building path names successful")

    # write output
    if(not kIsDebug):
        # build output directory
        outDir = os.path.join(os.getcwd(), 'data_files', 'data_xsec')

        # create output directory
        try:
            os.mkdir(outDir)
            print("%s directory created" % outDir)
        except FileExistsError:
            print("%s directory already exists" % outDir)

        # copy over files
        kk=0
        for i,o in zip(targetList,outFileList):
            kk += 1
            print("%s:\tcopying %s to %s" % (kk,i,o))
            shutil.copy(i,os.path.join(outDir,o))

        # ls directory
        if(kIsDebug): print("printing contents of output directory")
        if(kIsDebug): print(os.listdir(outDir))
        
            
if __name__ == '__main__':
    main(kIsDebug=False)
    print("have a nice day!")
