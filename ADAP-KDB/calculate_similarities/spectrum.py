import numpy as np

from typing import ClassVar, List


class Spectrum:

    def __init__(self, spectrum_id: int, mz_values: List, intensities: List):
        self.name = ''
        self.spectrum_id = spectrum_id
        order = np.argsort(mz_values)
        self.mz_values = np.array(mz_values)[order]
        self.intensities = np.array(intensities)[order]

    def match(self, other, mz_tolerance=0.01, normalized=False) -> float:
        index1 = 0
        index2 = 0
        score = 0.0
        while index1 < len(self.mz_values) and index2 < len(other.mz_values):
            mz1 = self.mz_values[index1]
            mz2 = other.mz_values[index2]
            if mz1 < mz2 - mz_tolerance:
                index1 += 1
            elif mz2 < mz1 - mz_tolerance:
                index2 += 1
            else:
                score += np.sqrt(self.intensities[index1] * other.intensities[index2])
                index1 += 1
                index2 += 1
        score *= score

        if normalized:
            sum1 = np.sum(self.intensities)
            sum2 = np.sum(other.intensities)
            score /= sum1 * sum2

        return score
