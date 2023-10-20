import numpy as np
import mne
import lab2
import time

ELECTRODE_NAMES = ['FP1', 'FP2', 'C3', 'C4', 'P7', 'P8', 'O1', 'O2']
ELECTRODE_MONTAGE = {
    "FP1": np.array([-3.022797, 10.470795, 7.084885]),
    "FP2": np.array([2.276825, 10.519913, 7.147003]),
    "C3": np.array([-7.339218, -0.774994, 11.782791]),
    "C4": np.array([6.977783, -1.116196, 12.059814]),
    "P7": np.array([-7.177689, -5.466278, 3.646164]),
    "P8": np.array([7.306992, -5.374619, 3.843689]),
    "O1": np.array([-2.681717, -9.658279, 3.634674]),
    "O2": np.array([2.647095, -9.638092, 3.818619])
}

BAND_START = 0.1
BAND_STOP = 120


def get_eeg_as_numpy_array(data_df):
    """ Returns a numpy array of dimension (# of EEG channels) x
    (# of samples), containing only EEG channel data present in
    <data_df>. The order of the rows is in ascending numeric order
    found in the initial file ordering:

        EEG Channel 1, 2, ... (# of channels)

    data_df: a pandas dataframe, with format as defined by the return
    value of lab2.load_recording_file
    """
    column_names = [name for name in data_df.columns if lab2.is_eeg(name) ]
    return np.transpose(np.array(data_df.loc[:, column_names]))

def construct_mne(data_df):
    """ Returns an MNE Raw object, consisting of lab2.NUM_CHANNELS
    channels of EEG data.

    data_df: a pandas dataframe, with format as defined by the return
    value of lab2.load_recording_file
    """

    mneInfo = mne.create_info(ch_names=ELECTRODE_NAMES, sfreq=lab2.SAMPLE_RATE, ch_types="eeg")
    raw = mne.io.RawArray(get_eeg_as_numpy_array(data_df), mneInfo)
    montage = mne.channels.make_dig_montage(ch_pos=ELECTRODE_MONTAGE, coord_frame='head')
    raw.set_montage(montage)

    return raw


def show_psd(data_mne, fmin=0, fmax=np.inf):
    """ Plots the power spectral density of the EEG signals in
    <data_mne>, limiting the range of the horizontal axis of the plot to
    [fmin, fmax].

    data_mne: MNE Raw object
    fmin: lower end of horizontal axis range
    fmax: upper end of horizontal axis range
    """
    spectrum = data_mne.compute_psd(fmin=fmin, fmax=fmax)
    spectrum.plot()


def filter_band_pass(data_mne, band_start=BAND_START, band_stop=BAND_STOP):
    """ Mutates data_mne, applying a band-pass filter
    with band defined by band_start and band_stop, where
    band_start < band_stop.

    data_mne: MNE Raw object
    """
    return data_mne.filter(l_freq=band_start, h_freq=band_stop)


def filter_notch_60(data_mne):
    """ Mutates data_mne, applying a notch filter
    to remove 60 Hz electrical noise

    data_mne: MNE Raw object
    """
    return data_mne.notch_filter(freqs=60)


if __name__ == "__main__":
    data_df = lab2.load_recording_file("eyes_closed_1.txt")
    data_mne = construct_mne(data_df)
    filtered_data_mne = filter_band_pass(data_mne, 0, 40)
    notched_data_mne = filter_notch_60(data_mne)
    show_psd(filtered_data_mne)

    
    data_mne.plot(block=True) # Must plot another graph because vanilla plot does not have block parameter 

    # get_eeg_as_numpy_array(data_df)

    # print(get_eeg_as_numpy_array(data_df))
    
    # TODO: add code here to show power spectral density plots