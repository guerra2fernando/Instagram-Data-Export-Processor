# Instagram Data Export Processor

This script processes Instagram data exports, updating file metadata and EXIF data based on the information provided in the export's HTML files.

## Features
- Processes various types of Instagram content (posts, stories, IGTV, reels, etc.)
- Updates file creation and modification dates
- Updates EXIF data for image files
- Cross-platform compatibility (Windows and Unix-based systems)

## Requirements
- Python 3.7+
- Dependencies listed in `requirements.txt`

## Installation
1. Clone this repository:
git clone [https://github.com/guerra2fernando/Instagram-Data-Export-Processor.git](https://github.com/guerra2fernando/Instagram-Data-Export-Processor.git)
cd Instagram-Data-Export-Processor

2. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

3. Install the required dependencies:
pip install -r requirements.txt


## Usage
Run the script with the following command:
python main.py /path/to/instagram/export [--config CONFIG_FILE] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

- `/path/to/instagram/export`: The base directory of your Instagram data export
- `--config`: Path to a custom configuration file (default: config.yaml)
- `--log-level`: Set the logging level (default: INFO)

## Configuration

You can customize the script's behavior by modifying the `config.yaml` file. This file contains settings for HTML file mappings, directory structures, and logging levels.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
