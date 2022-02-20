#!/usr/bin/env python3

# this python script will run and create results for the generated c files

import os
import pickle
import time
import subprocess
import argparse
import pexpect

if __name__ =='__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-o',
        '--output',
        default="results.csv",
        help="output csv name"
    )

    parser.add_argument(
        '-p',
        '--optimization',
        default="-O0",
        help="Optimization flag given to gcc compiler"
    )

    args = parser.parse_args()

    pkl_file = open("fname_pkl", 'rb')
    fnames = pickle.load(pkl_file)

    outfile = open(args.output, "w")

    outfile.write("filename,type i,type arr,type k,loop start,loop end,returncode,timeout,segfault,other fail,stdout/stderr\n")

    for fname in fnames:

        #compile the code

        process = subprocess.run(["gcc", "-lm", args.optimization, "-o", "test.out", fname])

        if process.returncode != 0:
            print("compile failed: "+fname)

        #now run the compiled code
        tout = False
        perror = False
        perror_stdout = ""
        perror_stderr = ""
        other_fail = False
        ret_status = 0

        try:
            #using python 3.6 for portability
            #attempt1
            # process = subprocess.run(["./test.out"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
            # universal_newlines=True, check=True, timeout=5)
            #attempt2
            # process = subprocess.Popen(["./test.out"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
            #     shell=True, universal_newlines=True)

            # try:
            #     perror_stdout, perror_stderr = process.communicate(timeout=5)
            # except subprocess.TimeoutExpired:
            #     #timed out
            #     tout= True
            #     print("timed out")

            # perror=True
            #attempt3
            child = pexpect.spawn("./test.out", timeout=10)
            child.expect(pexpect.EOF)
            out = child.before
            child.close()

            if child.exitstatus is None:
                ret_status = -1 * child.signalstatus
                perror = True
            else:
                ret_status = child.exitstatus
        
        except pexpect.TIMEOUT:
            tout=True
            print(fname+" timed out")

        # except subprocess.TimeoutExpired:
        #     #timed out
        #     tout= True
        #     print(fname+" timed out")

        # except subprocess.CalledProcessError as e:
        #     print(fname+" process error")
        #     perror_stdout = e.stdout
        #     perror_stderr = e.stderr
        #     perror = True

        except Exception as e: 
            print("other failure")
            print(e)
            other_fail = True

        #Parse current filename
        prog_options = fname.split("-")
        itype = prog_options[1][1:]
        atype = prog_options[2][1:]
        ktype = prog_options[3][1:]
        lstart = prog_options[4]
        lend = 0

        if prog_options[5] == '':
            lend = "-"+prog_options[6][:-2]
        else:
            lend = prog_options[5][:-2]


        #outfile.write(fname+","+itype+","+atype+","+ktype+","+lstart+","+lend+","+str(process.returncode)+","+str(tout)+","+str(other_fail)+",")
        outfile.write(fname+","+itype+","+atype+","+ktype+","+lstart+","+lend+","+str(ret_status)+","+str(tout)+","+str(perror)+","+str(other_fail)+",")

        # write stdout and stderr if they exist
        if out is not None:
            outfile.write(str(out).replace("\n", " ").replace(","," ")+"\n")
        else:
            outfile.write("\n")


        # if process.stdout is not None:
        #     outfile.write(str(process.stdout).replace("\n"," ")+",")
        # if perror:
        #     outfile.write(str(perror_stdout).replace("\n", " ")+",")
        # else:
        #     outfile.write(",")
        # if process.stderr is not None:
        #     outfile.write(str(process.stderr).replace("\n"," ") + "\n") 
        # if perror:
        #     outfile.write(str(perror_stderr).replace("\n", " ") + "\n")
        # else:
        #     outfile.write(",\n")

