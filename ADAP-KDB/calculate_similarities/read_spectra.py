import numpy as np
import pandas as pd
import pickle

from spectrum import Spectrum
from typing import List


def read_spectra_from_csv(filename: str) -> List[Spectrum]:
    """Reads spectra from CSV file"""
    data = pd.read_csv(filename, header=0)
    spectrum_ids = np.unique(data['SpectrumId'].values)
    spectra = []
    progress_step = int(len(spectrum_ids) / 100)
    for i, spectrum_id in enumerate(spectrum_ids):
        mz_values = data.loc[data.SpectrumId == spectrum_id, 'Mz'].values
        intensities = data.loc[data.SpectrumId == spectrum_id, 'Intensity'].values
        spectra.append(Spectrum(spectrum_id, mz_values, intensities))
        if i % progress_step == 0:
            print('Progress: {:.0f}%'.format(100 * i / len(spectrum_ids)))
    return spectra


def read_spectra_from_msp(filename: str) -> List[Spectrum]:
    spectra = []
    name = None
    mz_values = []
    intensities = []
    index = 0
    for line in open(filename):
        line = line.strip()
        if len(line) > 0:
            if ':' in line:
                key, value = line.split(':', 1)
                if key.strip() == 'Name':
                    name = value.strip()
            else:
                mz, intensity = map(float, line.split(' ', 1))
                mz_values.append(mz)
                intensities.append(intensity)
        else:
            index += 1
            spectrum = Spectrum(index, mz_values, intensities)
            spectrum.name = name
            spectra.append(spectrum)

            name = None
            mz_values = []
            intensities = []

    return spectra


if __name__ == '__main__':
    spectra = read_spectra_from_csv('data/peaks_high-res_2021-04-14.csv')
    pickle.dump(spectra, open('data/spectra_high-res_2021-04-14.p', 'wb'))
