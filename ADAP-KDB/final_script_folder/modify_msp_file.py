import pandas as pd

# Using readlines()
file1 = open('/Users/ericliao/Desktop/manuscript_revise/adap-kdb_consensus_spectra_GAS_HIGH_RESOLUTION_copy.msp', 'r')
Lines = file1.readlines()

modified_line_list = []
# Strips the newline character
for line in Lines:
    modified_line_list.append(line)
    if line.startswith("Name: "):
        modified_line_list.append("Spectrum_type: MS2\n")
        modified_line_list.append("PrecursorMZ: 363.2541\n")

with open("/Users/ericliao/Desktop/manuscript_revise/adap-kdb_consensus_spectra_GAS_HIGH_RESOLUTION_new.msp", "w") as f:
        contents = f.writelines(modified_line_list)




# line_index = -1
# for i in range(10806):
#     with open("/Users/ericliao/Desktop/manuscript_revise/adap-kdb_consensus_spectra_GAS_HIGH_RESOLUTION_copy.msp", "r+",
#               encoding='utf8', errors='ignore') as f:
#         lines = f.readlines()
#
#     for index, line in enumerate(lines):
#         if line.startswith("Name: ") and index > line_index:
#             line_index = index
#             break
#     lines.insert(line_index+1, "Spectrum_type: MS2\n")
#     lines.insert(line_index+1, "PrecursorMZ: 363.2541\n")
#
#     with open("/Users/ericliao/Desktop/manuscript_revise/adap-kdb_consensus_spectra_GAS_HIGH_RESOLUTION_copy.msp", "w") as f:
#         contents = f.writelines(lines)
#
# # print("Line{}: {}".format(count, line.strip()))