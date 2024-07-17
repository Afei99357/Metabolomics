from subprocess import Popen
import os


def format_code(input_dir, output_dir):
    return [
        "docker",
        "run",
        "-it",
        "--rm",
        "-e",
        "WINEDEBUG=-all",
        "-v",
        "/Users/yliao13/Desktop/raw_sample_test/" + input_dir + ":/data",
        "chambm/pwiz-skyline-i-agree-to-the-vendor-licenses",
        "wine",
        "msconvert",
        "--mzXML",
        "--filter=peakPicking",
        "/data/*.raw",
        "-o",
        output_dir,
    ]


filenames = sorted(os.listdir("/Users/yliao13/Desktop/raw_sample_test/"))
output_dirs = [f for f in filenames if "_convert" in filenames]
input_dirs = [f for f in filenames if "_convert" not in filenames]

processes = [
    Popen(format_code(input_dir, output_dir))
    for input_dir, output_dir in zip(input_dirs, output_dirs)
]
# runs all at once...
results = [x.wait() for x in processes]
for filename, result in zip(filenames, results):
    if result == 0:
        print("Processing succeeded", filename)
    else:
        print("Failed to process", filename)

assert all(results == 0 for x in results), "Some processes failed."
