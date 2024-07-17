import pandas as pd

df = pd.read_csv("/Users/yliao13/Desktop/Peak.csv")

df_new = pd.DataFrame(columns=df.columns)

unique_spectra = df['SpectrumId'].unique()
spectrum_intensity_dict = {}

for i in unique_spectra:
    max_intensity = df[df["SpectrumId"] == i]["Intensity"].max()
    spectrum_intensity_dict[i] = max_intensity

# pd.DataFrame.from_dict(spectrum_intensity_dict).to_csv('/Users/yliao13/Desktop/spectrum_max_Intensity_dict.csv')

for index, item in df.iterrows():
    item['Intensity'] = item['Intensity'] / spectrum_intensity_dict[item["SpectrumId"]]

df.to_csv("/Users/yliao13/Desktop/new_Peak.csv", index=False)
