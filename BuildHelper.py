# Building

import subprocess
import os
import sys
import getopt
import filecmp

# current working directory 
current_path = os.getcwd()

def main(argv):
    section_directory = ''
    input_data_file = ''
    actual_output_file = ''
    expected_output_file = ''

    try:
        opts, args = getopt.getopt(argv,"d:",["section_directory="])
    except getopt.GetoptError:
        print ('BuildHelper.py -d <section directory>')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print ('BuildHelper.py -d <section directory>')
            sys.exit()
        elif opt in ("-d", "--sectionDirectory"):
            section_directory = arg

    directory_path = (current_path + "/" + section_directory)    

    for path, subdirs, files in os.walk(directory_path):
        for sub_directory in subdirs:
            if sub_directory == "Data":
                continue
            else:
                sub_directory_path = os.path.join(directory_path, sub_directory)
                print("Current Working Directory: " + sub_directory_path)

                # Set actual_output_file path and clear it
                expected_output_file = sub_directory_path + "/Data/expected_output.txt"
                actual_output_file = sub_directory_path + '/Data/actual_output.txt'
                open(actual_output_file, "w").close()

                # Set the environment variable to current path
                SetEnvVar = './SetEnvVar.sh {}/Data/actual_output.txt'.format(str(sub_directory_path))

                # Build
                source_file = sub_directory_path + "/" + sub_directory + ".cpp"
                binary_file = sub_directory_path + "/" + sub_directory
                subprocess.call(["g++-10", "-std=c++14", source_file, "-o", binary_file])

                # Execute
                runnable = './{}/{}/{}'.format(str(section_directory), str(sub_directory), str(sub_directory))
                input_data_file = '{}/{}/Data/input.txt'.format(str(section_directory), str(sub_directory))
                subprocess.run(''' 
                    export OUTPUT_PATH={0} &&  
                    ({1}<{2})'''.format(str(actual_output_file), str(runnable), str(input_data_file)), 
                        shell=True, check=True)

                # Compare actual values Vs. expected values
                comparison_result = filecmp.cmp(actual_output_file, expected_output_file, shallow = False)
                if(comparison_result):
                    print("+ The sample test-case \x1b[7;30;42m[PASS]\x1b[0m for " + sub_directory)
                else:
                    print("+ The sample test-case \x1b[7;30;41m[FAIL]\x1b[0m for " + sub_directory)
                    print("--> Expected: ")
                    print("--> Actual  : ")
                
                # Remove the binary
                cmd = "rm " + runnable
                os.system(cmd)

                # Clear the actual output data 
                open(actual_output_file, "w").close()
        

if __name__ == "__main__":
    main(sys.argv[1:])
