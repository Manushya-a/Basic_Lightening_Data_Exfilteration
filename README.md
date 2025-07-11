# Lightning Data Exfilteration

A Python script that connects to a WebSocket server to collect lightning strike data and outputs it in various formats (console log, Excel file, or Google Sheet).

## Features

- Real-time lightning data collection via WebSocket
- Multiple output modes:
  - **Log Mode**: Display data in the console
  - **Excel Mode**: Save data to a local Excel file
  - **Google Sheet Mode**: Upload data to a Google Spreadsheet
- Color-coded console output for better readability
- Asynchronous data fetching for efficient performance

## Prerequisites

- Python 3.7+
- Google API credentials (for Google Sheet mode)
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Manushya-a/Lightening_Data_Exfilteration.git
   cd lightning-data-collector
   ```

2. Install the required packages:
   ```bash
   pip3 install -r requirements.txt
   ```

3. For Google Sheet mode:
    - For an elaborate explaination of steps head on to GSheet.md, which will provide a comprehensive stepwise guide.

## Usage

```bash
python3 main.py [mode] [number]
```

### Modes:
- `-log`: Output data to console
- `-excel`: Save data to Excel file
- `-gsheet`: Upload data to Google Sheet

### Arguments:
- `number`: Number of lightning strike events to collect

### Examples:

1. Display 10 lightning strikes in console:
   ```bash
   python3 main.py -log 10
   ```

2. Save 5 lightning strikes to Excel:
   ```bash
   python3 main.py -excel 5
   ```

3. Upload 20 lightning strikes to Google Sheet:
   ```bash
   python3 main.py -gsheet 20
   ```

## Configuration

For Google Sheet mode, you need to:
1. Replace `"Link-to-your-google-spreadsheet"` in the code with your actual Google Sheet ID (Line no. 132)
2. Ensure your `credentials.json` file is in the project directory
3. Ensure you input the target's websocket url (Line no. 184)

## Output Format

The collected data includes:
- Latitude and longitude of strike
- Date and time
- Station information
- Altitude
- MDS (Maximum Detection Sensitivity)
- MCG (Maximum Cloud-to-Ground)
- Region
- Delay

## Code Structure

The main components of the code are:

1. **Color Definitions** (`bcolors` class):
   - Provides colored console output using ANSI escape codes

2. **Data Processing Functions**:
   - `flatten()`: Converts JSON objects to list format
   - `time_formater()`: Converts Unix timestamp to readable format
   - `decode()`: Decodes the WebSocket message data

3. **Output Modes**:
   - `log_mode()`: Prints data to console
   - `excel_mode()`: Saves data to Excel file
   - `gsheet_mode()`: Uploads data to Google Sheet

4. **Core Functions**:
   - `fetch_data()`: Asynchronously collects data from WebSocket
   - `main()`: Handles command-line arguments and execution flow

## Dependencies

Listed in `requirements.txt`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

## Known Issues

- Time formatting in Excel output may need adjustment
- Google Sheet mode has rate limits (0.75s delay between updates)

## Support

For questions or issues, please open an issue in the GitHub repository.

---

*This project was developed only for educational purposes and demonstrates WebSocket communication, async programming, and data processing in Python.*
