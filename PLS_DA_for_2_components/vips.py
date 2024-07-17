# Author: Eric Liao
# August 2021

import numpy as np


class vips:
    def vips(model):
        t = model.x_scores_
        w = model.x_weights_
        q = model.y_loadings_

        # p - number of variables, h - number of LV
        p, h = w.shape
        vips = np.zeros((p,))

        # SS(bh * th) the percentage of y explained by the h-th latent variable
        s = np.diag(t.T @ t @ q.T @ q).reshape(h, -1)
        total_s = np.sum(s)
        for i in range(p):
            weight = np.array(
                [(w[i, j] / np.linalg.norm(w[:, j])) ** 2 for j in range(h)]
            )
            vips[i] = np.sqrt(p * (s.T @ weight) / total_s)
        return vips
