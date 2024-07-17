import matplotlib.pyplot as plt
import multiprocessing
import numpy as np
import pandas as pd
import pickle

from functools import partial
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform
from sklearn.cluster import DBSCAN
from sklearn.metrics import fowlkes_mallows_score, silhouette_score
from typing import Dict, List, Tuple


plt.rcParams.update({'font.size': 6})


def get_fowlkes_mallows_score(spectrum_ids, labels, names):

    # Use only annotated spectra
    annotated_spectrum_ids = []
    annotated_labels = []
    annotated_names = []
    for spectrum_id, label in zip(spectrum_ids, labels):
        name = names[spectrum_id]
        if name.startswith('Unknown'):
            continue
        annotated_spectrum_ids.append(spectrum_id)
        annotated_labels.append(label)
        annotated_names.append(name)

    # Replays names with numbers
    unique_names = np.unique(annotated_names)
    name_ids = {}
    for i in range(len(unique_names)):
        name_ids[unique_names[i]] = i

    true_labels = [name_ids[name] for name in annotated_names]

    return fowlkes_mallows_score(true_labels, annotated_labels)


def get_spectrum_names(filename):

    print('Reading names of the spectra...')

    spectra = pd.read_csv(filename, header=0)

    # Read names of the spectra
    names = {}
    for _, row in spectra.iterrows():
        names[row['Id']] = row['Name']

    return names


def get_linkage(filename, spectrum_names):

    print('Reading similarities of the spectra...')

    # # Read similarity scores
    # matches = pd.read_csv(filename, header=0)
    #
    # # Collect all spectrum id's
    # spectrum_ids = set([])
    # progress_step = int(len(matches) / 100)
    # for i, row in matches.iterrows():
    #
    #     spectrum_ids.add(row['QuerySpectrumId'])
    #     spectrum_ids.add(row['MatchSpectrumId'])
    #
    #     if i % progress_step == 0:
    #         print('Progress: {:.0f}%'.format(100 * i / len(matches)))
    #
    # spectrum_ids = [i for i in spectrum_ids if i in spectrum_names.keys()]
    # np.save('data/spectrum_ids.npy', spectrum_ids)
    # num_spectra = len(spectrum_ids)
    #
    # # Create a map from spectrum id to spectrum index from 0 to num_spectra
    # spectrum_id_to_index_map = {}
    # for i in range(num_spectra):
    #     spectrum_id_to_index_map[spectrum_ids[i]] = i
    #
    # # Create a distance matrix
    # distance_matrix = np.ones((num_spectra, num_spectra))
    # progress_step = int(len(matches) / 100)
    # for i, row in matches.iterrows():
    #     try:
    #         query_spectrum_index = spectrum_id_to_index_map[row['QuerySpectrumId']]
    #         match_spectrum_index = spectrum_id_to_index_map[row['MatchSpectrumId']]
    #     except KeyError:
    #         continue
    #
    #     distance = max(1.0 - row['Score'], 0.0)
    #     distance_matrix[query_spectrum_index, match_spectrum_index] = distance
    #     distance_matrix[match_spectrum_index, query_spectrum_index] = distance
    #
    #     if i % progress_step == 0:
    #         print('Progress: {:.0f}%'.format(100 * i / len(matches)))
    #
    # for i in range(num_spectra):
    #     distance_matrix[i, i] = 0.0
    #
    # np.save('data/distance_matrix.npy', distance_matrix)

    spectrum_ids = np.load('data/spectrum_ids_low-res_2021-04-14.npy')
    distance_matrix = np.load('data/distance_matrix_low-res_2021-04-14.npy')

    print(distance_matrix.shape)

    condensed_distance_matrix = squareform(distance_matrix, force='tovector')

    print(condensed_distance_matrix.shape)

    # Perform clustering
    link = linkage(condensed_distance_matrix, method='complete')
    pickle.dump(link, open('data/complete-linkage_low-res.p', 'wb'))
    link = linkage(condensed_distance_matrix, method='single')
    pickle.dump(link, open('data/single-linkage_low-res.p', 'wb'))
    link = linkage(condensed_distance_matrix, method='average')
    pickle.dump(link, open('data/average-linkage_low-res.p', 'wb'))
    link = linkage(condensed_distance_matrix, method='ward')
    pickle.dump(link, open('data/ward-linkage_low-res.p', 'wb'))
    # link = pickle.load(open('data/link.p', 'rb'))

    return spectrum_ids, link, distance_matrix, condensed_distance_matrix


def hierarchical_clustering(distance_matrix: np.ndarray, spectrum_ids: np.ndarray, spectrum_names,
                            linkage, t: float, fm_scores: List[float], sizes: List[float]):

    # print(eps, min_samples)

    labels = fcluster(linkage, t, criterion='distance')

    fm_score = get_fowlkes_mallows_score(spectrum_ids, labels, spectrum_names)
    fm_scores.append(fm_score)

    size = len(np.unique(labels))
    sizes.append(size)


def calculate_scores():
    spectrum_names = get_spectrum_names('data/spectra_low-res_2021-04-14.csv')
    spectrum_ids, link, distance_matrix, condensed_distance_matrix = get_linkage('data/matches_low-res_2021-04-14.csv', spectrum_names)

    complete_linkage = pickle.load(open('data/complete-linkage_low-res.p', 'rb'))
    single_linkage = pickle.load(open('data/single-linkage_low-res.p', 'rb'))
    average_linkage = pickle.load(open('data/average-linkage_low-res.p', 'rb'))
    ward_linkage = pickle.load(open('data/ward-linkage_low-res.p', 'rb'))

    fm_scores1 = []
    fm_scores2 = []
    fm_scores3 = []
    fm_scores4 = []
    sizes1 = []
    sizes2 = []
    sizes3 = []
    sizes4 = []

    thresholds = np.linspace(0.01, 0.9, 100)
    for t in thresholds:
        print('Threshold: {:f}'.format(t))
        hierarchical_clustering(distance_matrix, spectrum_ids, spectrum_names, complete_linkage, t,fm_scores1, sizes1)
        hierarchical_clustering(distance_matrix, spectrum_ids, spectrum_names, single_linkage, t, fm_scores2, sizes2)
        hierarchical_clustering(distance_matrix, spectrum_ids, spectrum_names, average_linkage, t, fm_scores3, sizes3)
        hierarchical_clustering(distance_matrix, spectrum_ids, spectrum_names, ward_linkage, t, fm_scores4, sizes4)

    pickle.dump({
        'thresholds': thresholds,
        'fm_scores1': fm_scores1,
        'fm_scores2': fm_scores2,
        'fm_scores3': fm_scores3,
        'fm_scores4': fm_scores4,
        'sizes1': sizes1,
        'sizes2': sizes2,
        'sizes3': sizes3,
        'sizes4': sizes4
    }, open('data/hierarchical_low-res_scores.p', 'wb'))


def read_score() -> Dict[str, List]:
    return pickle.load(open('data/hierarchical_low-res_scores.p', 'rb'))


def main():

    print('Plotting the figure...')

    # calculate_scores()

    score_dict = read_score()
    thresholds = np.array(score_dict['thresholds'])
    fm_scores1 = score_dict['fm_scores1']
    fm_scores2 = score_dict['fm_scores2']
    fm_scores3 = score_dict['fm_scores3']
    fm_scores4 = score_dict['fm_scores4']
    sizes1 = score_dict['sizes1']
    sizes2 = score_dict['sizes2']
    sizes3 = score_dict['sizes3']
    sizes4 = score_dict['sizes4']

    fig = plt.figure(figsize=(3, 3))

    ax1 = fig.add_subplot(111)
    dbscan1_fm_handle, = ax1.plot(1 - thresholds, fm_scores1, color='blue', linestyle='solid', label='Complete linkage', linewidth=1)
    dbscan2_fm_handle, = ax1.plot(1 - thresholds, fm_scores2, color='blue', linestyle='dotted', label='Single linkage', linewidth=1)
    dbscan3_fm_handle, = ax1.plot(1 - thresholds, fm_scores3, color='blue', linestyle='dashed', label='Average linkage', linewidth=1)
    dbscan4_fm_handle, = ax1.plot(1 - thresholds, fm_scores4, color='blue', linestyle='dashdot', label='Ward linkage', linewidth=1)
    # ax1.axvline(0.8, 0, 1, linestyle='dotted', color='black')
    ax1.set_xlabel('Similarity threshold')
    ax1.set_ylabel('Fowlkes-Mallows Score')
    ax1.yaxis.label.set_color('blue')
    ax1.tick_params(axis='y', colors='blue')
    ax1.grid(linewidth=0.5)
    legend = ax1.legend(handles=[dbscan1_fm_handle, dbscan2_fm_handle, dbscan3_fm_handle, dbscan4_fm_handle], loc='lower right')
    for h in legend.legendHandles:
        h.set_color('black')

    # ax3 = fig.add_subplot(133)
    ax3 = ax1.twinx()
    ax3.plot(1 - thresholds, sizes1, color='green', linestyle='solid', linewidth=1)
    ax3.plot(1 - thresholds, sizes2, color='green', linestyle='dotted', linewidth=1)
    ax3.plot(1 - thresholds, sizes3, color='green', linestyle='dashed', linewidth=1)
    ax3.plot(1 - thresholds, sizes4, color='green', linestyle='dashdot', linewidth=1)
    ax3.set_ylabel('Number of clusters')
    ax3.ticklabel_format(axis='y', style='sci', scilimits=(0, 0), useMathText=True)
    ax3.yaxis.label.set_color('green')
    ax3.tick_params(axis='y', colors='green')

    plt.tight_layout(pad=0)
    plt.savefig('figure.png', dpi=600)
    plt.show()


if __name__ == '__main__':
    main()