import pandas as pd
import pubchempy as pcp
import time
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# nist_file_dir = "/Users/yliao13/Desktop/metabolights_studies/MTBLS1301/MTBLS1301_nist.tsv"
# df_nist = pd.read_csv(nist_file_dir, sep='\t', header=3, index_col=None)
# df_nist["pubchem_id"] = ""
# df_nist["smiles"] = ""
#
# df_metabolights = pd.read_csv('/Users/yliao13/Desktop/metabolights_studies/MTBLS1301/m_MTBLS1301_LC-MS_negative_hilic_metabolite_profiling_v2_maf.tsv', sep='\t', header=0, index_col=None)
#
# inchikey_list = df_nist["InChIKey"].tolist()

results = pcp.get_compounds('N[C@H](Cc1c[nH]c2ccccc12)C(O)=O', 'smile')
print(results)

# index = 0
# for i in inchikey_list:
#     if not pd.isna(i):
#         print(index)
#         time.sleep(0.5)
#         compound = pcp.get_compounds(i, 'inchikey')
#         if len(compound) != 0 and not pd.isna(compound[0]):
#             # print(compound[0])
#             pubchem_id = compound[0].__getattribute__('cid')
#             smiles = compound[0].__getattribute__("isomeric_smiles")
#             df_nist.at[index, 'pubchem_id'] = pubchem_id
#             df_nist.at[index, 'smiles'] = smiles
#             index = index + 1
#         else:
#             index = index + 1
#     else:
#         index = index + 1

df_nist

# df_combine = pd.merge(left=df_nist, right=df_workbench, left_on='pubchem_id', right_on='pubchem_id')

# df_combine