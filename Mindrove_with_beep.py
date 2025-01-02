import time
import numpy as np
from mindrove.board_shim import BoardShim, MindRoveInputParams, BoardIds, MindroveConfigMode

# Initialize the board
BoardShim.enable_dev_board_logger()
params = MindRoveInputParams()
board_id = BoardIds.MINDROVE_WIFI_BOARD
board_shim = BoardShim(board_id, params)
board_shim.prepare_session()
board_shim.start_stream()

# Get channel indices
eeg_channels = BoardShim.get_eeg_channels(board_id)
accel_channels = BoardShim.get_accel_channels(board_id)
gyro_channels = BoardShim.get_gyro_channels(board_id)
sampling_rate = BoardShim.get_sampling_rate(board_id)
beep_channel = 19
# Data variables
num_points = 2000
data_batches = []
last_data = None
last_beep_time = time.time()

while True:
    # Send a beep signal every 30 seconds
    if time.time() - last_beep_time >= 1:
        board_shim.config_board(MindroveConfigMode.BOOP)
        board_shim.config_board(MindroveConfigMode.BEEP)
        last_beep_time = time.time()

    if board_shim.get_board_data_count() >= num_points:
        data = board_shim.get_current_board_data(num_points)

        # Check if the retrieved data is new by comparing with last_data
        if last_data is None or not np.array_equal(data, last_data):
            data_batches.append(data)  # Append only new data
            last_data = data  # Update last_data to the most recent batch

        # Extract data for specific channels if needed
        current_eeg_data = data[eeg_channels]
        current_accel_data = data[accel_channels]
        current_gyro_data = data[gyro_channels]

        # Optional: process data here

# This will run indefinitely until manually stopped.
