from numpy import sum, max


def tic(scan):
    return sum(scan.intensity_array)


def max_intensity(scan):
    return max(scan.intensity_array)
