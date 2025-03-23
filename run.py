import time
import numpy as np
from mindrove.board_shim import BoardShim, MindRoveInputParams, BoardIds
from pylsl import StreamInfo, StreamOutlet  # LSL import

# Initialize the board
BoardShim.enable_dev_board_logger()
params = MindRoveInputParams()
board_id = BoardIds.MINDROVE_WIFI_BOARD
board_shim = BoardShim(board_id, params)
board_shim.prepare_session()
board_shim.start_stream()

# Lab Streaming Layer setup
lsl_info = StreamInfo('MindRoveStream', 'EEG', 16, 500, 'double64', 'myuid34234')
lsl_outlet = StreamOutlet(lsl_info)

# Get channel indices
eeg_channels = BoardShim.get_eeg_channels(board_id)
accel_channels = BoardShim.get_accel_channels(board_id)
gyro_channels = BoardShim.get_gyro_channels(board_id)
timestamp_channel = BoardShim.get_timestamp_channel(board_id)
beep_channel = [19]

num_points = 2000
last_timestamp = -np.inf  # initially set to negative infinity to ensure all data is streamed first

try:
    while True:
        if board_shim.get_board_data_count() >= num_points:
            data = board_shim.get_current_board_data(num_points)
            # print(data.shape)
            # Extract timestamps
            timestamps = data[timestamp_channel]

            # Find indices of new timestamps
            new_data_indices = np.where(timestamps > last_timestamp)[0]

            if len(new_data_indices) == 0:
                # No new data since last timestamp
                continue

            # Slice data starting from the first new timestamp
            changed_data = data[:, new_data_indices]
            print(changed_data.shape)
            # Stream the new data to LSL
            for row in changed_data.T:
                #print(row[27])
                sample = row[[timestamp_channel]+ eeg_channels + gyro_channels + accel_channels + beep_channel].tolist()
                print(sample)
                lsl_outlet.push_sample(sample)
                #print("EEG Sample:", row[[timestamp_channel]+ eeg_channels])

            # Update the last timestamp
            last_timestamp = timestamps[new_data_indices[-1]]

        time.sleep(0.002)

except KeyboardInterrupt:
    print("Stopping the session...")
finally:
    board_shim.stop_stream()
    board_shim.release_session()
