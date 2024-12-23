import numpy as np
from skimage.color import rgb2hsv
from skimage.exposure import histogram


def extract_hsv_features(image):
    img_hsv = (rgb2hsv(image) * 255).astype(np.uint8)

    h_hist, h_bins = histogram(img_hsv[:, :, 0], nbins=256)
    s_hist, s_bins = histogram(img_hsv[:, :, 1], nbins=256)
    v_hist, v_bins = histogram(img_hsv[:, :, 2], nbins=256)

    h_bins = h_bins.astype(np.uint8)
    s_bins = s_bins.astype(np.uint8)
    v_bins = v_bins.astype(np.uint8)

    hue = np.zeros(256, dtype=int)
    saturation = np.zeros(256, dtype=int)
    value = np.zeros(256, dtype=int)

    for i in range(h_bins.size):
        hue[h_bins[i]] = h_hist[i]

    for i in range(s_bins.size):
        saturation[s_bins[i]] = s_hist[i]

    for i in range(v_bins.size):
        value[v_bins[i]] = v_hist[i]

    histograms = hue.tolist() + saturation.tolist() + value.tolist()

    return histograms


def create_column_hsv_feature(nbins):
    labels = np.zeros(3 * nbins, dtype="<U20")
    for i in range(nbins):
        labels[i] = f"Hue_{i}"
        labels[i + 256] = f"Saturation_{i}"
        labels[i + 512] = f"Value_{i}"
    return labels
