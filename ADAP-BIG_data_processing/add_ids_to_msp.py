import argparse
import pandas as pd


def find_identity(data, name):
    """Search the table data for the row matching the given name, and return the identity"""

    if "Unknown" not in data.columns:
        return None

    filtered_data = data[data["Unknown"].str.startswith(name)]
    if len(filtered_data) == 0:
        return None

    records = filtered_data.to_dict(orient="records")
    return records[0]


def get_name(row: pd.Series) -> str:
    name = row.get("Name")
    if name is not None:
        return name
    return row["Peptide"]


def get_score(row: pd.Series) -> str:
    score = row.get("MF")
    if score is not None:
        return score
    return row["Score"]


def add_ids_to_msp(msp_filename, tsv_filename, out_filename):
    """Adds the identification results from .tsv file into .msp file"""

    tsv_data = pd.read_csv(
        tsv_filename, sep="\t", header=0, skipfooter=2, skiprows=3, engine="python"
    )

    out_file = open(out_filename, "w+")
    for line in open(msp_filename):
        overwritten = False
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key.lower() == "name":
                identity = find_identity(tsv_data, value)
                if identity is not None:
                    out_file.write("Name: {}\n".format(get_name(identity)))
                    out_file.write("Matching Score: {}\n".format(get_score(identity)))
                    out_file.write("Mass: {}\n".format(identity["Mass"]))
                    out_file.write("Formula: {}\n".format(identity["Formula"]))
                    out_file.write("NIST Id: {}\n".format(identity["Id"]))
                    out_file.write("CASNO: {}\n".format(identity["CAS"]))
                    out_file.write("INCHI_KEY: {}\n".format(identity["InChIKey"]))
                    if "Prec.Type" in identity is not None:
                        out_file.write(
                            "Precursor_type: {}\n".format(identity["Prec.Type"])
                        )
                    else:
                        out_file.write("Precursor_type: {}\n".format(""))
                else:
                    out_file.write("Name: Unknown\n")
                out_file.write("Original Name: {}\n".format(value))
                overwritten = True
        if not overwritten:
            out_file.write(line + "\n")
    out_file.close()


def main():
    parser = argparse.ArgumentParser(
        description="Adds the identification results from .tsv file into .msp file"
    )
    parser.add_argument(
        "--msp_file", help=".msp file containing mass spectra", required=True
    )
    parser.add_argument(
        "--tsv_file", help=".tsv file containing identification", required=True
    )
    parser.add_argument("--out_file", help="Output file", required=True)

    args = parser.parse_args()
    add_ids_to_msp(args.msp_file, args.tsv_file, args.out_file)


if __name__ == "__main__":
    main()
