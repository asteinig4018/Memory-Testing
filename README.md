# Memory Testing
The purpose of these files is to testing memory limits, mechanisms, and faults on various systems.

## C Testing

The C testing files try different types of this code:
```
int i = 0;

int arr[5];

int k = 54;

for(i = 6; i > -5; i--){
    arr[i] = i;
    printf("i: %d, arr[i] %d", i, arr[i]);
}
```

Where the loop's starting and ending values are changed along with the datatypes of i, arr, and k.
Optimizations are turned off (or can be set).

This is probably why people like Rust. 

## Usage

First, generate the C files. Create a directory c_files (in the future, you may be able to change this with a passed argument). Then run
```
python c_generator.py
```
This will also create a python pickle which will cache the file names for the runner program.
Next, run the runner program. This should work with Python 3.6 and above (not tested for 3.5 but might work, largely dependent on the subprocess module). You can supply an output csv file with `-o` (default is `results.csv`) and specify a gcc optimization flag with `-p`. The default is `-O0`.
```
python c_runner.py
```
This will take some time as there are over 300 programs that need to be compiled and run and there is a 5 second timeout for infinitely looping programs.

## Result

The output csv can be easily sorted, filtered, and anlyzed as an .xlsx in excel. 