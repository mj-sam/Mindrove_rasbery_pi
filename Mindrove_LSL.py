import time
import numpy as np
from mindrove.board_shim import BoardShim, MindRoveInputParams, BoardIds, MindroveConfigMode
from pylsl import StreamInfo, StreamOutlet  # LSL import

# Initialize the board
BoardShim.enable_dev_board_logger()
params = MindRoveInputParams()
board_id = BoardIds.MINDROVE_WIFI_BOARD
board_shim = BoardShim(board_id, params)
board_shim.prepare_session()
board_shim.start_stream()

# Lab Streaming Layer setup
lsl_info = StreamInfo('MindRoveStream', 'EEG', 15, 250, 'float32', 'myuid34234')  # Adjust the channel count and rate
lsl_outlet = StreamOutlet(lsl_info)

# Get channel indices
eeg_channels = BoardShim.get_eeg_channels(board_id)
accel_channels = BoardShim.get_accel_channels(board_id)
gyro_channels = BoardShim.get_gyro_channels(board_id)
Beep_Channel = [19]
num_points = 2000

# Data variables
last_data = None

try:
    while True:
        if board_shim.get_board_data_count() >= num_points:
            data = board_shim.get_current_board_data(num_points)

            # Check if data is the same as the last batch
            if last_data is not None and np.array_equal(data, last_data):
                # If data is identical, skip this iteration
                continue

            if last_data is not None:
                # Determine the index from where the data differs
                diff_index = np.where(~np.equal(data, last_data))[1][0]  # Identify first differing index
                changed_data = data[:, diff_index:]  # Slice data from the differing index
            else:
                # If this is the first batch of data, use the entire data
                diff_index = 0
                changed_data = data

            # Stream the changed part to LSL
            for row in changed_data.T:  # LSL expects data in row-major order
                lsl_outlet.push_sample(row[eeg_channels + gyro_channels + accel_channels + Beep_Channel].tolist())
                print(row[eeg_channels])
            # Update the last_data with the current batch
            last_data = data

        time.sleep(0.01)  # Small delay to reduce CPU usage

except KeyboardInterrupt:
    print("Stopping the session...")
finally:
    board_shim.stop_stream()
    board_shim.release_session()
