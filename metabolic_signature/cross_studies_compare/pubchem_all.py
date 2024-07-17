import datetime
import requests
import pandas as pd
import time


def get_info_from_inchikey(inchikey):
    r = requests.get(
        f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/{inchikey}/property/CanonicalSMILES,InChI,IUPACName/JSON')
    code = r.status_code
    print(code)
    if code != 200:
        csmiles = "Nah"
        cinchi = "Nah"
        iupac = "Nah"
    else:
        r = r.json()
        if not (r['PropertyTable']['Properties'][0]['CanonicalSMILES'] is None):
            csmiles = r['PropertyTable']['Properties'][0]['CanonicalSMILES']
        else:
            csmiles = "Nah"
        if not(r['PropertyTable']['Properties'][0]['InChI'] is None):
            cinchi = r['PropertyTable']['Properties'][0]['InChI']
        else:
            cinchi = "Nah"
        # if not (r['PropertyTable']['Properties'][0]['IUPACName'] is None):
        #     iupac = r['PropertyTable']['Properties'][0]['IUPACName']
        # else:
        #     iupac = "Nah"
        #title = r['PropertyTable']['Properties'][0]['Title']
    return csmiles, cinchi

def get_info_from_isosmiles(isosmile):
    r = requests.get(
        f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{isosmile}/property/CompoundID,CanonicalSMILES,InChI,InChIKey/JSON')
    code = r.status_code
    print(code)
    if code != 200:
        csmiles = "Nah"
        cinchi = "Nah"
        cid = "Nah"
        inchik = "Nah"
    else:
        r = r.json()
        if not (r['PropertyTable']['Properties'][0]['CanonicalSMILES'] is None):
            csmiles = r['PropertyTable']['Properties'][0]['CanonicalSMILES']
        else:
            csmiles = "Nah"
        if not(r['PropertyTable']['Properties'][0]['InChI'] is None):
            cinchi = r['PropertyTable']['Properties'][0]['InChI']
        else:
            cinchi = "Nah"
        if not (r['PropertyTable']['Properties'][0]['CompoundID'] is None):
            cid = r['PropertyTable']['Properties'][0]['CompoundID']
        else:
            cid = "Nah"
        if not (r['PropertyTable']['Properties'][0]['InChIKey'] is None):
            inchik = r['PropertyTable']['Properties'][0]['InChIKey']
        else:
            inchik = "Nah"
        #title = r['PropertyTable']['Properties'][0]['Title']
    return csmiles, cinchi, cid, inchik


def get_info_from_inch(inchi):
    r = requests.get(
        f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchi/{inchi}/property/CompoundID,CanonicalSMILES,InChIKey/JSON')
    code = r.status_code
    print(code)
    if code != 200:
        csmiles = "Nah"
        cid = "Nah"
        inchik = "Nah"
    else:
        r = r.json()
        if not (r['PropertyTable']['Properties'][0]['CanonicalSMILES'] is None):
            csmiles = r['PropertyTable']['Properties'][0]['CanonicalSMILES']
        else:
            csmiles = "Nah"
        if not (r['PropertyTable']['Properties'][0]['CompoundID'] is None):
            cid = r['PropertyTable']['Properties'][0]['CompoundID']
        else:
            cid = "Nah"
        if not (r['PropertyTable']['Properties'][0]['InChIKey'] is None):
            inchik = r['PropertyTable']['Properties'][0]['InChIKey']
        else:
            inchik = "Nah"
        #title = r['PropertyTable']['Properties'][0]['Title']
    return csmiles, cid, inchik


def smiles_list(file):
    inchi_l = []
    smile_l = []
    cid_l = []
    inchik_l = []
    data = pd.read_csv(file)
    isosmile = data["smiles"].values
    for i, smiles in enumerate(isosmile):
        s, i, u, inc = get_info_from_isosmiles(smiles)
        inchi_l.append(i)
        smile_l.append(s)
        cid_l.append(u)
        inchik_l.append(inc)
        time.sleep(1)
        print(datetime.datetime.now().strftime("%H:%M:%S"))
    data["InChiKey2"] = inchik_l
    data["InChI2"] = inchi_l
    data["SMILES_new"] = smile_l
    data["cid"] = cid_l
    return data

def inchi_list(file):
    inchi_l = []
    smile_l = []
    cid_l = []
    inchik_l = []
    data = pd.read_csv(file, header=0)
    inchi = data["inchi"].values
    for i, inchis in enumerate(inchi):
        s, u, inc = get_info_from_inch(inchis)
        inchi_l.append(inchis)
        smile_l.append(s)
        cid_l.append(u)
        inchik_l.append(inc)
        time.sleep(1)
        print(datetime.datetime.now().strftime("%H:%M:%S"))
    data["InChiKey2"] = inchik_l
    data["InChI2"] = inchi_l
    data["SMILES_new"] = smile_l
    data["cid"] = cid_l
    return data



##### For InChI Search #####

# make sure the column header for InChI is inchi and the column header for isometric smiles is smiles
file = "/Users/yliao13/Desktop/metabolights_studies/MTBLS1301/m_MTBLS1301_LC-MS_negative_hilic_metabolite_profiling_v2_maf.csv"
inchi_list(file).to_csv("/Users/yliao13/Desktop/metabolights_studies/MTBLS1301/inchi_key_search.csv")
# smiles_list(file).to_csv("")
