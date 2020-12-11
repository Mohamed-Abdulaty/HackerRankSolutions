##################################################
## BuildHelper is a utility to help with the build
## and testing your implementation for HackerRank-
## s solutions
##################################################
##################################################
## Author: Mohamed Morsy
## Copyright: Copyright 2020, HackerRanksSolutions
## Credits: [Mohamed Morsy]
## License: MIT
## Version: 1.2.0
## Mmaintainer: -
## Email: --
## Status: dev
##################################################

import subprocess
import os
import sys
import getopt
import filecmp

# Global variables
section_directory = ''
input_data_file = ''
actual_output_file = ''
expected_output_file = ''
directory_path = ''
problem_name = ''

# current working directory 
current_path = os.getcwd()

def main(argv):
    
    single_problem = False
    complete_dir = False

    try:
        opts, args = getopt.getopt(argv,"h:d:p",["section_directory=", "problem_name="])
    except getopt.GetoptError:
        print ('BuildHelper.py -d <section directory>')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print ('BuildHelper.py -d <section directory>')
            print ('BuildHelper.py -p <single problem name>')
            sys.exit()
        elif opt in ('-d', '--section_directory'):
            section_directory = arg
            directory_path = (current_path + "/" + section_directory)
            complete_dir = True
        elif opt in ('-p', '--problem_name'):
            problem_name = arg
            single_problem, complete_dir = True, False
        else:
            print("Unknowen argument")
        
    if (single_problem is True): 
        # Build this problem only.
        print(">>> Build Single Problem.")
        print(f'{"Problem Name:":50}' + '{}'.format(str(problem_name)))
        # Get inside the section directory
        os.chdir('{}/{}'.format(str(current_path), str(section_directory)))

        if (IsDirAndFileExists(problem_name)):
            # Set Paths
            SetPaths(problem_name)
            # Build and Run
            BuildSourceAndExecute(problem_name)
            # Testing: Compare expected Vs. actual
            Testing(problem_name)
        else:
            print("Can not find the specified Folder/File name.")
    elif (complete_dir is True): 
        # Complete Directory Build
        print(">>> Build Complete Problems Section.")
        print(f'{"Section Name:":50}', end=" ")
        print('{}'.format(str(section_directory)))
        # Get inside the section directory
        os.chdir('{}/{}'.format(str(current_path), str(section_directory)))

        for path, subdirs, files in os.walk(directory_path):
            for sub_directory in subdirs:
                if sub_directory == "Data":
                    continue
                else:
                    print(f'{"Problem Name:":50}', end=" ")
                    print('{}'.format(str(sub_directory)))
                    # Set paths
                    SetPaths(sub_directory)
                    # Build and Run
                    BuildSourceAndExecute(sub_directory)
                    # Testing: Compare expected Vs. actual
                    Testing(sub_directory)
    else: # Invalid option.
        print ("This is an invalid option.")
        print ("Nothing to do here ...")
    
def IsDirAndFileExists(problem_name):
    ret = False
    # Is the problem file exists ?
    if(os.path.isdir(problem_name)):
        # Is the source file *.cpp & data files exists ? 
        ret = os.path.isfile('{}/{}.cpp'.format(str(problem_name), str(problem_name))) and \
              os.path.isfile('{}/Data/actual_output.txt'.format(str(problem_name))) and \
              os.path.isfile('{}/Data/expected_output.txt'.format(str(problem_name))) and \
              os.path.isfile('{}/Data/input.txt'.format(str(problem_name)))
    else:
        print(">> Problem Folder Does not Exists.")

    return ret

def SetPaths(problem_name):
    global expected_output_file
    global actual_output_file
    global input_data_file

    expected_output_file = '{}/Data/expected_output.txt'.format(str(problem_name))
    actual_output_file = '{}/Data/actual_output.txt'.format(str(problem_name))
    input_data_file = '{}/Data/input.txt'.format(str(problem_name))
    open(actual_output_file, "w").close()
    return

def BuildSourceAndExecute(problem_name):
    global actual_output_file

    # Build
    print (f'{"Start building":50}', end=" ")
    source_file = '{}/{}.cpp'.format(str(problem_name), str(problem_name))
    binary_file = '{}/{}_bin'.format(str(problem_name), str(problem_name))
    subprocess.call(["g++-10", "-std=c++14", source_file, "-o", binary_file])
    print ("[DONE]")

    # Execute
    print (f'{"Running":50}', end=" ")
    runnable = './{}/{}_bin'.format(str(problem_name), str(problem_name))
    subprocess.run(''' 
        export OUTPUT_PATH={0} &&  
        ({1}<{2})'''.format(str(actual_output_file), str(runnable), str(input_data_file)), 
            shell=True, check=True)
    print("[DONE]")

    print(f'{"Removing the binary":50}', end=" ")
    # Remove the binary
    cmd = "rm " + runnable
    os.system(cmd)
    print("[DONE]")

    return

def Testing(problem_name):
    global actual_output_file
    global expected_output_file
    # Compare actual values Vs. expected values
    comparison_result = filecmp.cmp(actual_output_file, expected_output_file, shallow = False)
    msg = "The sample test-case for " + problem_name
    if(comparison_result):
        print(f'{msg:50}', end=" ")
        print('\x1b[7;30;42m[PASS]\x1b[0m')
    else:
        print(f'{msg:50}', end=" ")
        print('\x1b[7;30;41m[FAIL]\x1b[0m')
        print("--> Expected: ")
        print("--> Actual  : ")
                    
    print(f'{"Clean the actual file data":50}', end=" ")
    # Clear the actual output data 
    open(actual_output_file, "w").close() 
    print("[DONE]")
    print("=========================================================")
    return

# MAIN
if __name__ == "__main__":
    main(sys.argv[1:])
