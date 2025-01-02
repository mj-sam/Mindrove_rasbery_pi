// You need to import first mindrove.dll into your project by adding it to the Project's References
using mindrove;
using System.Linq; // will come in handy later

BoardShim.enable_dev_board_logger(); // enable logger when developing to catch relevant logs
MindRoveInputParams input_params = new MindRoveInputParams();
int board_id = (int)BoardIds.MINDROVE_WIFI_BOARD;
BoardShim board_shim = new BoardShim(board_id, input_params);


board_shim.prepare_session();
board_shim.start_stream();

int[] eeg_channels = BoardShim.get_eeg_channels(board_id);
int[] accel_channels = BoardShim.get_accel_channels(board_id);
int sampling_rate = BoardShim.get_sampling_rate(board_id);
int boardId = (int)BoardIds.MINDROVE_WIFI_BOARD;

// Store values from each method in variables
int samplingRate = BoardShim.get_sampling_rate(boardId);
int packageNumChannel = BoardShim.get_package_num_channel(boardId);
int markerChannel = BoardShim.get_marker_channel(boardId);
int batteryChannel = BoardShim.get_battery_channel(boardId);
int numRows = BoardShim.get_num_rows(boardId);
int timestampChannel = BoardShim.get_timestamp_channel(boardId);

string version = BoardShim.get_version();
string deviceName = BoardShim.get_device_name(boardId);
int[] eegChannels = BoardShim.get_eeg_channels(boardId);
int[] exgChannels = BoardShim.get_exg_channels(boardId);
int[] emgChannels = BoardShim.get_emg_channels(boardId);


int[] accelChannels = BoardShim.get_accel_channels(boardId);
int[] otherChannels = BoardShim.get_other_channels(boardId);
int[] resistanceChannels = BoardShim.get_resistance_channels(boardId);

int window_size = 2; // seconds
int num_points = 1000;

while (true)
{
    if (board_shim.get_board_data_count() >= num_points)
    {
        
        double[,] data = board_shim.get_board_data(num_points);
        double[][] eeg_data = eeg_channels.Select(index => Enumerable.Range(0, data.GetLength(1)).Select(colIndex => data[index, colIndex]).ToArray()).ToArray();
        double[][] accel_data = accel_channels.Select(index => Enumerable.Range(0, data.GetLength(1)).Select(colIndex => data[index, colIndex]).ToArray()).ToArray();

        // process data, or print it out
        //Console.WriteLine(data.GetLength(0));
        Console.WriteLine(data.GetLength(1));
        //Console.WriteLine(data[0, 0]);
        Console.WriteLine(data[26, 0]);

    }
}