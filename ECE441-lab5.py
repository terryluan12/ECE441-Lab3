import time
from brainflow import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, WindowOperations, DetrendOperations
import numpy
def calculate_alpha_beta_ratio(port='COM4'):
    boardID = BoardIds.CYTON_BOARD
    boardDescr = BoardShim.get_board_descr()
    sampleRate = int(boardDescr['sampling_rate'])
    params = BrainFlowInputParams()
    params.serial_port =  port
    board = BoardShim(boardID, params)
    board.prepare_session()
    board.start_stream()

    DataFilter.get_nearest_power_of_two(sampleRate)
