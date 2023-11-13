import time
from brainflow import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, WindowOperations, DetrendOperations
import numpy as np
def calculate_alpha_beta_ratio(port='COM4'):
    boardID = BoardIds.CYTON_BOARD
    boardDescr = BoardShim.get_board_descr()
    sampleRate = int(boardDescr['sampling_rate'])
    params = BrainFlowInputParams()
    params.serial_port =  port
    board = BoardShim(boardID, params)
    board.prepare_session()
    board.start_stream()

    power_of_two = DataFilter.get_nearest_power_of_two(sampleRate)
    time.sleep(2)
    data = board.get_board_data()
    channels = data['eeg_channels']
    ratio = np.zeros(len(channels))

    for count, channel in enumerate(channels):
        datafilter = DataFilter.detrend(data[channel], DetrendOperations.LINEAR.value)
        spectrum = datafilter.get_psd_welch(data[channel], power_of_two, power_of_two/2, sampleRate, WindowOperations.HANNING.value)
        alpha = datafilter.get_band_power(spectrum, 7., 13.)
        beta = datafilter.get_band_power(spectrum, 14., 30.)
        ratio[count] = beta/alpha
    
    if board.is_prepared():
        board.release_session()
    return np.mean(ratio)

if __name__ == "__main__":
    try:
        while True:
            ratio = calculate_alpha_beta_ratio()
            print(f"alpha/beta ratio: {ratio}")
    except:
        quit()