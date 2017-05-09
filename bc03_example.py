import numpy as np
from spectres import spectres
import matplotlib.pyplot as plt


# Load up the wavelength values the models are sampled at
model_wavs = np.genfromtxt("bc2003_hr_stelib_m62_chab_ssp.ised_ASCII", skip_header=6, skip_footer=233, usecols=np.arange(1, 6918, dtype="int"))

# Load up the model grid, the first axis must run over wavelength, the second may contain different spectra to be resampled
model_grid= np.genfromtxt("bc2003_hr_stelib_m62_chab_ssp.ised_ASCII", skip_header=7, skip_footer=12, usecols=np.arange(1, 6918, dtype="int")).T

# Specify the wavelength sampling to be applied to the spectrum or spectra
regrid = np.arange(3000., 5000., 5.)

# Call the spectres function to resample the input spectrum or spectra to the new wavelength grid
model_resampled_5A = spectres(model_wavs, model_grid, regrid)

# Resample to a lower resolution
model_resampled_10A = spectres(model_wavs, model_grid, np.arange(3000., 5000., 10.))

# Load up the age values for each of the models we have resampled
model_ages = np.genfromtxt("bc2003_hr_stelib_m62_chab_ssp.ised_ASCII", skip_header=0, skip_footer=239)[1:]

# Find the index of the column most closely corresponding to a 1Gyr old burst of star formation
col_1gyr = np.argmin(np.abs(model_ages - 10**9))


# Plotting code:
plt.figure(figsize=(12,6))

# Plot the spectrum at its original sampling
plt.plot(model_wavs, model_grid[:,col_1gyr] +  1.0*np.max(model_resampled_5A[:,col_1gyr]), color="blue", label="Original")

# Plot the spectrum on the new wavelength grid
plt.plot(regrid, model_resampled_5A[:,col_1gyr] +  0.5*np.max(model_resampled_5A[:,col_1gyr]), color="red", label="5 $\mathrm{\AA}$ sampling")

# Plot the spectrum on a lower resolution
plt.plot(np.arange(3000., 5000., 10.), model_resampled_10A[:,col_1gyr], color="green", label="10 $\mathrm{\AA}$ sampling")

plt.xlim(3000, 5000)
plt.ylim(0, 0.00045)

plt.xlabel("Wavelength $\mathrm{(\AA)}$")
plt.ylabel("Flux (arb. units)")
plt.legend(loc=4)
plt.show()
