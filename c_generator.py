#!/usr/bin/env python3

# this python script will generate C files for memory testing

import os
import pickle

FILE_LOCATION_PREFIX = "c_files/"

TYPE_INT = "int"
TYPE_INT64 = "int64_t"
TYPE_DOUBLE = "double"

i_types = [TYPE_INT, TYPE_INT64, TYPE_DOUBLE]

i_init = "0"

arr_types = [TYPE_INT, TYPE_INT64]

arr_len = "5"

k_types = [TYPE_INT, TYPE_INT64, TYPE_DOUBLE]

k_val = "54"

loop_starts = ["20", "8", "6", "4"]

loop_ends = ["0", "-1", "-5", "-6", "-20"]#, "-2100000"]

if __name__ == "__main__":

    f_name_mem = list()

    for it in i_types:
        for arrt in arr_types:
            for kt in k_types:
                for ls in loop_starts:
                    for le in loop_ends:

                        filename = "ts-i"+it+"-a"+arrt+"-k"+kt+"-"+ls+"-"+le+".c"

                        f_name_mem.append(FILE_LOCATION_PREFIX + filename)

                        f = open(FILE_LOCATION_PREFIX + filename, 'w')
                        if f is not None:
                            # starting writing
                            f.write("#include <stdio.h>\n#include <stdlib.h>\n#include <stdint.h>\nint main(int argc, char** argv){\n")
                            f.write(it)
                            f.write(" i = "+i_init+";\n")
                            f.write(arrt)
                            f.write(" arr["+arr_len+"];\n")
                            f.write(kt)
                            f.write(" k = "+k_val+";\n")
                            f.write("for(i = "+ls+"; i >= "+le+"; --i){\n")

                            #cast if necessary
                            if it == TYPE_DOUBLE:
                                f.write("arr[(int)i] = 1;\n")
                            else:
                                f.write("arr[i] = 1;\n")

                            #ensure correct printing types
                            if it == TYPE_DOUBLE:
                                f.write("printf(\"l- i: %lf")
                            elif it == TYPE_INT64:
                                f.write("printf(\"l- i: %ld")
                            else:
                                f.write("printf(\"l- i: %d")

                            if arrt == TYPE_INT:
                                f.write(" arr[i]: %d, ")
                            elif arrt == TYPE_INT64:
                                f.write(" arr[i]: %ld, ")


                            if kt == TYPE_DOUBLE:
                                f.write("k: %lf\\n\"")
                            elif kt == TYPE_INT64:
                                f.write("k: %ld\\n\"")
                            else:
                                f.write("k: %d\\n\"")

                            if it == TYPE_DOUBLE:
                                f.write(", i, arr[(int) i], k);\n")
                            else:
                                f.write(", i, arr[i], k);\n")

                            f.write("}\n")
                            f.write("printf(\"done\\n\");\n")
                            f.write("}\n")

                            f.close()

                        else:
                            print("Error opening file")

    pkl_file = open("fname_pkl", "wb")
    pickle.dump(f_name_mem, pkl_file)
    pkl_file.close()
