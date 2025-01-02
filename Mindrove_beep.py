import mindrove
from mindrove.board_shim import BoardShim, MindRoveInputParams, BoardIds,  MindroveConfigMode
from mindrove.data_filter import DataFilter, FilterTypes, AggOperations

#params = MindRoveInputParams()

#board_shim = BoardShim(BoardIds.MINDROVE_WIFI_BOARD, params)
#board_shim.prepare_session()
#board_shim.start_stream()

print(MindroveConfigMode.BEEP)
#board_shim.config_board(MindroveConfigMode.BEEP) # // send synchronization signal / trigger

#board_shim.config_board(MindroveConfigMode.IMP_MODE)# // switch to impedance mode

#board_shim.config_board(MindroveConfigMode.EEG_MODE)# // switch to eeg mode