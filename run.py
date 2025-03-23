import time
import numpy as np
import RPi.GPIO as GPIO
from mindrove.board_shim import BoardShim, MindRoveInputParams, BoardIds, MindroveConfigMode
from pylsl import StreamInfo, StreamOutlet

# GPIO Configuration
GPIO.setmode(GPIO.BCM)
TRIGGER_PIN = 18
GPIO.setup(TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialize MindRove board
BoardShim.enable_dev_board_logger()
params = MindRoveInputParams()
board_id = BoardIds.MINDROVE_WIFI_BOARD
board_shim = BoardShim(board_id, params)
board_shim.prepare_session()
board_shim.start_stream()

# EEG/EMG (500Hz) LSL outlet
eeg_channels = BoardShim.get_eeg_channels(board_id)
beep_channel = [19]
eeg_info = StreamInfo('MindRove_EEG', 'EEG', len(eeg_channels) + 1, 500, 'float32', 'eeg_stream')
eeg_outlet = StreamOutlet(eeg_info)

# IMU (50Hz) LSL outlet
accel_channels = BoardShim.get_accel_channels(board_id)
gyro_channels = BoardShim.get_gyro_channels(board_id)
imu_channels = accel_channels + gyro_channels
imu_info = StreamInfo('MindRove_IMU', 'IMU', len(imu_channels), 50, 'float32', 'imu_stream')
imu_outlet = StreamOutlet(imu_info)

# Data handling
imu_interval = 1 / 50
eeg_interval = 1 / 500
last_imu_time = time.time()
last_eeg_time = time.time()

try:
    while True:
        # Check GPIO Trigger
        if GPIO.input(TRIGGER_PIN) == GPIO.HIGH:
            print("GPIO Trigger Received!")
            board_shim.config_board(MindroveConfigMode.BEEP)

        current_time = time.time()
        board_data_count = board_shim.get_board_data_count()
        
        if board_data_count > 0:
            data = board_shim.get_current_board_data(board_data_count)
            num_samples = data.shape[1]
            
            for i in range(num_samples):
                sample = data[:, i]

                # Stream EEG at ~500Hz
                if current_time - last_eeg_time >= eeg_interval:
                    eeg_sample = sample[eeg_channels + beep_channel]
                    eeg_outlet.push_sample(eeg_sample.tolist())
                    last_eeg_time = current_time

                # Stream IMU at ~50Hz
                if current_time - last_imu_time >= imu_interval:
                    imu_sample = sample[imu_channels]
                    imu_outlet.push_sample(imu_sample.tolist())
                    last_imu_time = current_time

                current_time = time.time()

except KeyboardInterrupt:
    print("Stopping session...")

finally:
    board_shim.stop_stream()
    board_shim.release_session()
    GPIO.cleanup()
