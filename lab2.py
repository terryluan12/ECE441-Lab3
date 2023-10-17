import pandas as pd
import matplotlib.pyplot as plt
import os
import lab2_utils as utils

##########################################################
#  Defined constants used to load in the .txt EEG files  #
##########################################################

NUM_ROWS_TO_SKIP = 4  # header data in the .txt file
NUM_CHANNELS = 8  # number of EEG channels
EEG_CHANNEL_PREFIX = utils.NEW_EEG_CHANNEL_PREFIX  # label to help us identify columns with EEG data
SAMPLE_RATE = 250  # Sampling rate of data in Hz

DATA_DIR = "C:/Users/terry/Desktop/ECE441/ECE441-Lab3/data"  # directory containing recording files to be loaded and plotted
TIMESTAMP_STR = "timestamp"  # name of column with recording timestamps

# Used to plot EEG channels in the same colors as shown on the
# OpenBCI GUI (and also matching the wire colors connected to
# each electrode). Keys are the EEG channel, values are the hex
# code for the corresponding color.
EEG_CHANNEL_COLORS = {
    "1": "#878787",  # gray
    "2": "#a670db",  # purple
    "3": "#697de0",  # blue
    "4": "#6be069",  # green
    "5": "#e6de4e",  # yellow
    "6": "#e6954e",  # orange
    "7": "#eb4444",  # red
    "8": "#703d1f",  # brown
}


###########################################################
#  Functions to load and plot EEG data                    #
###########################################################


def load_recording_file(fname):
    """Returns a pandas dataframe that consists of all the timeseries
    data, with associated column names, from an OpenBCI GUI recording file.
    The filename of the recording file is given by <fname>.

    fname: string representing the name of the recording file to load
    """
    file_path = os.path.join(DATA_DIR, fname)
    data_df = pd.read_csv(file_path,skiprows=NUM_ROWS_TO_SKIP)

    utils.clean_eeg_dataframe(data_df)  # does some cleanup
    return data_df



def is_eeg(col_name):
    """ Returns True if the column given by <col_name> contains EEG data, and
    False otherwise.

    col_name: a string representing a column in the dataframe loaded using
    load_recording_file
    """
    return 'eeg' in col_name



def plot_eeg_data(data_df, start_time):
    """ Plots all EEG channel data found in the pandas dataframe
    <data_df> with respect to time.

    data_df: a Pandas dataframe consisting of EEG data to be plot
    """
    # creates 8 rows and 1 column of subplots
    fig, ax = plt.subplots(
        NUM_CHANNELS, 1, sharex='all', figsize=(15, 15)
    )

    # iterates through columns in the dataframe
    # TODO: your code here
    #x=[0.4 * i for i in range(data_df.rows)]

    start_dp=start_time*SAMPLE_RATE;
    x=[i * 0.4 for i in range(start_dp, len(data_df))]
    i=0
    for col_name in data_df.columns.values:
        # TODO: your code here
        # plot EEG channel 1 on the first subplot, and so on
        if(is_eeg(col_name)):
            ax[i].plot(x,data_df[col_name][start_dp:],color=EEG_CHANNEL_COLORS[str(i+1)], label="Eeg Ch" + str(i+1))
            i=i+1


    # Adding title, legends, and axes labels
    [ax[i].legend(loc="lower left", fontsize=18) for i in range(NUM_CHANNELS)]
    fig.suptitle("EEG data over time", fontsize=22)
    fig.subplots_adjust(top=0.95, bottom=0.05)
    plt.xlabel("Time (s)", fontsize=20)
    #plt.rcParams['text.usetex'] = True
    fig.text(0.06, 0.5, 'Recorded Signal ($\mu$V)', va='center', rotation='vertical', fontsize=20)
    plt.show()
    #plt.rcParams['text.usetex'] = False


if __name__ == "__main__":
    data_df = load_recording_file("eyes_open_4.txt")

    #pd.set_option('s', None)
    print(data_df)

    plot_eeg_data(data_df,2)