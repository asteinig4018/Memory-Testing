#!/usr/bin/env python3

# this python script will run and create results for the generated c files

import os
import pickle
import time
import subprocess

COMPILER_ARGS = "gcc -lm -O1 -o test.out "

if __name__ =='__main__':
    pkl_file = open("fname_pkl", 'rb')
    fnames = pickle.load(pkl_file)

    outfile = open("results.csv", "w")

    outfile.write("filename,timeout,other fail,output\n")

    for fname in fnames:

        #compile the code

        process = subprocess.run(["gcc", "-lm", "-O1", "-o", "test.out", fname])

        if process.returncode != 0:
            print("compile failed: "+fname)

        #now run the compiled code
        tout = False
        other_fail = False

        try:
            process = subprocess.run(["./test.out"], stdout=subprocess.PIPE, universal_newlines=True, timeout=5)

        except subprocess.TimeoutExpired:
            #timed out
            tout= True
            print("timed out")

        except: 
            print("other failure")
            other_fail = True


        outfile.write(fname+","+str(tout)+","+str(other_fail)+","+process.stdout+"\n")

