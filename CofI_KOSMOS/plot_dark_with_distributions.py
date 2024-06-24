# Making all necessary imports.
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import poisson
__all__ = ['plot_dark_with_distributions']

def plot_dark_with_distributions(image, rn, dark_rate,
                                 n_images = 1,
                                 exposure = 1,
                                 gain = 1,
                                 show_poisson = True,
                                 show_gaussian = True):
    """
    Plot the distribution of dark pixel values, optionally overplotting the expected Poisson and
    normal distributions corresponding to dark current only or read noise only.

    Parameters:

    image: numpy array
    Dark frame to histogram.

    rn: float
    The read noise in electrons.

    dark_rate: float
    The dark current in electrons/sec/pixel.

    n_images: float (optional), default is 1
    If the image is formed from the average of some number of dark frames then
    the resulting Poisson distribution depends on the number of images as does the
    expected standard deviation of the Gaussian.

    exposure: float
    Exposure time in seconds.

    gain: float (optional), default is 1
    Gain of the camera in electron/ADU.

    show_poisson: bool (optional), default is True
    If True, overplot a Poisson distribution with mean equal to the expected dark
    counts for the number of images.

    show_gaussian: bool (optional), default is True
    If True, overplot a normal distribution with mean equal to the expected dark
    counts and standard deviation equal to the read noise, scaled as appropiate for
    the number of images.

    Returns:
    Histogram of dark pixel values with (optional) Poisson and/or Gaussian distribution fitted.

    """
    # Plotting the histogram of dark pixel values.
    hist = plt.hist(image.flatten(), bins = 100, align = 'mid', range = (-50,200),
                 density = True, label = "Dark frame");
    # Computing/setting necessary inputs/data for Poisson distribution.
    expected_mean_dark = dark_rate * exposure / gain
    pois = stats.poisson(expected_mean_dark - 3 * n_images)
    pois_x = np.arange(0, 200, 5)
    new_area = np.sum(1 / n_images * pois.pmf(pois_x))
    # If desired, plot Poisson distribution.
    if show_poisson:
        plt.plot(pois_x / n_images, pois.pmf(pois_x) / new_area,
                 label = "Poisson distribution, mean of {:5.2f} counts".format(expected_mean_dark))
    # If desired, plot Gaussian distribution.
    if show_gaussian:
        # The expected width of the Gaussian depends on the number of images.
        expected_scale = rn / gain * np.sqrt(n_images)
        # Mean value is same as for the Poisson distribution.
        expected_mean = expected_mean_dark * n_images
        gauss = stats.norm(loc=expected_mean - 3, scale=expected_scale + 3)
        gauss_x = np.linspace(expected_mean - 3 * expected_scale + 3,
                              expected_mean + 3 * expected_scale + 3,
                              num = 100)
        plt.plot(gauss_x / n_images, gauss.pdf(gauss_x) * n_images, label='Gaussian, standard dev is read noise in counts')
    # Set desired plot features.
    plt.xlabel("Dark counts in {} sec exposure".format(exposure))
    plt.ylabel("Fraction of pixels (area normalized to 1)")
    plt.grid()
    plt.legend()
