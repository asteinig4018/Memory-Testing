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

### Requirements

```
pip install pexpect
```

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

## Output

The output csv can be easily sorted, filtered, and anlyzed as an .xlsx in excel. 

## Results

I tested with `i` as an `int`, `int64_t`, and `double`; `arr` as an `int` and `int64_t`; and `k` as an `int`, `int64_t`, and `double`. 

I started the loop at `4`, `6`, `8`, and `20`. I ended the loop at `0`, `-1`, `-5`, `-6`, and `-20`. 

Expected out come: I expcted segmentation faults or `i` to be overwritten, causing an infinite loop. 

### Surface Pro (7th Gen Intel i7, 64 bit system)

#### Initial Observations
As it turned out, indexing any part of the array greater than its declared length would give a `*** stack smashing detected ***` error, crashing the test. 

An array end of `-20` also had the same effect as an array end of `-6`, so I just looked at one of them. 

#### Memory-Significant Patterns
* Whenever the array index went to `-5` or further negative, the program would inifite loop, unless i was an `int64_t` and arr was an `int` type. In that case, the program would segmentation fault. 
* When the array index went to `-1`, the program would usually finish normally, except in the cases below. 

|i type|arr type|k type|timeout|segfault|
|--|--|--|--|--|
|`int`|`int64_t`|`int`|TRUE|FALSE|
|`double`|`int`|`int`|TRUE|FALSE|
|`double`|`int64_t`|`int`|TRUE|FALSE|
|`int64_t`|`int`|`int`|FALSE|TRUE|
