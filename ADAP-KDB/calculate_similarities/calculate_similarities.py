import pandas as pd
import pickle

from multiprocessing import Manager, Pool, cpu_count
from spectrum import Spectrum
from typing import List


class Match:
    def __init__(self, query_spectrum: Spectrum, match_spectrum: Spectrum, score: float):
        self.query_spectrum = query_spectrum
        self.match_spectrum = match_spectrum
        self.score = score


def match_spectrum(query_spectrum: Spectrum, spectra: List[Spectrum], progress, queue,
                   score_threshold=0.1):
    # print('Calculating similarities for spectrum {:d}'.format(query_spectrum.spectrum_id))
    for spectrum in spectra:
        score = query_spectrum.match(spectrum)
        if score > score_threshold:
            line = '{:d},{:d},{:.9f}'.format(query_spectrum.spectrum_id, spectrum.spectrum_id, score)
            queue.put(line)
            # matches.append(Match(query_spectrum, spectrum, score))
    progress.value += 1
    print('Progress: {:.0f}%'.format(100 * progress.value / len(spectra)))

    return None


def listener(queue):
    """Listens to the messages on the queue and writes to a file"""

    with open('data/matches_low-res_2021-04-14.csv', 'w') as f:
        f.write('QuerySpectrumId,MatchSpectrumId,Score\n')
        while True:
            message = queue.get()
            if message == 'kill':
                break
            f.write(str(message) + '\n')
            f.flush()


def calculate_similarities(spectra: List[Spectrum]):
    manager = Manager()

    # matches = manager.list()
    queue = manager.Queue()
    progress = manager.Value('i', 0)

    num_cpu = cpu_count()
    print('Number of CPUs: {:d}\n'.format(num_cpu))
    pool = Pool(processes=num_cpu)

    # Start the listener
    pool.apply_async(listener, (queue,))

    jobs = []
    for spectrum in spectra:
        job = pool.apply_async(match_spectrum, (spectrum,), kwds={
            'spectra': spectra,
            'queue': queue,
            'progress': progress,
            'score_threshold': 0.1})
        jobs.append(job)

    # Wait until all the computational jobs are completed
    for job in jobs:
        job.get()

    # Stop the listener and close the pool
    queue.put('kill')
    pool.close()
    pool.join()


def create_dataframe(matches: List[Match]) -> pd.DataFrame:
    query_spectrum_ids = [m.query_spectrum.spectrum_id for m in matches]
    match_spectrum_ids = [m.match_spectrum.spectrum_id for m in matches]
    scores = [m.score for m in matches]
    return pd.DataFrame(data={
        'QuerySpectrumId': query_spectrum_ids,
        'MatchSpectrumId': match_spectrum_ids,
        'Score': scores
    })


if __name__ == '__main__':
    spectra = pickle.load(open('data/spectra_low-res_2021-04-14.p', 'rb'))
    print('Calculating similarities...')
    calculate_similarities(spectra)
    # df = create_dataframe(matches)
    # df.to_csv('data/matches.csv', index=False)
