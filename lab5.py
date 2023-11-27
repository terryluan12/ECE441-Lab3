import numpy as np
import brainflow as bf
import time

from brainflow.data_filter import DataFilter, DetrendOperations, WindowOperations

def calculate_alpha_beta_ratio(port='COM7'):
    boardID=bf.BoardIds.CYTON_BOARD
    boardDescr = bf.BoardShim.get_board_descr(boardID)
    sampleRate=boardDescr['sampling_rate']
    int(sampleRate)

    params=bf.BrainFlowInputParams()
    params.serial_port=port
    board1=bf.BoardShim(board_id=boardID,input_params=params)

    board1.prepare_session()
    board1.start_stream()
    pwr=DataFilter.get_nearest_power_of_two(sampleRate)
    time.sleep(2)

    data=board1.get_board_data()
    #channels=boardDescr['eeg_channels']
    channels=[1,2]
    print(channels)
    alpha_beta=np.zeros(len(channels))

    for count, channel in enumerate(channels):
        #print(data[channel])
        filter=DataFilter.detrend(data[channel],DetrendOperations.LINEAR.value)
        psd=DataFilter.get_psd_welch(data[channel],pwr,pwr//2,sampleRate,WindowOperations.HANNING.value)
        alpha=DataFilter.get_band_power(psd,7.0,13.0)
        beta=DataFilter.get_band_power(psd,14.0,30.0)
        alpha_beta[count]=beta/alpha
    
    if(board1.is_prepared()):
        board1.release_session()

    return np.mean(alpha_beta)

if __name__ == "__main__":
    try:
        while True:
            alpha_beta=calculate_alpha_beta_ratio()
            print(alpha_beta)
    except KeyboardInterrupt:
        quit()


