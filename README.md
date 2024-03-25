# Asynchronous Crypto Trading Bot

This automated cryptocurrency trading bot executes trades on the Binance platform based on trading signals derived from color patterns observed in a specific video stream. The bot is designed with Python, utilizing asynchronous programming paradigms to efficiently process video frames and interact with the Binance API for trading actions.

## Project Structure

The project is organized into two main components:

- **`signal_processor.py`**: This script is responsible for capturing video frames, processing the images to detect specific color patterns, and determining trading signals ("BUY" or "SELL").
- **`trader.py`**: Utilizes the trading signals provided by `signal_processor.py` to execute trades on the Binance platform according to the identified signals.

## Prerequisites

Before you begin, ensure you have the following:

- Python 3.8 or newer.
- An active Binance account with generated API keys.
- The following Python libraries installed: `python-binance`, `opencv-python`, `Pillow`, `numpy`.

## Setup and Installation

1. **Clone the repository:**
```python
git clone https://github.com/sande5h/API_BINANCE_TEST.git

```

2. **Install the required dependencies:**
pip install python-binance opencv-python pillow numpy


3. **Configure your Binance API keys and other settings in a `config.py` file:**
Create a `config.py` in the project root directory with the following content, replacing placeholder values with your actual data:
```python
API_KEY = "your_binance_api_key"
API_SECRET = "your_binance_api_secret"
VIDEO_LINK = "https://www.youtube.com/link"
SYMBOL = 'BTCUSDT' #change as needed
Crypto = 'BTC'
```
## Usage Instructions

### Signal Processing Test:

This for the testing of the binance_api and is use in placeholder for the actual signal generator. Make your own as i am not really sure i am permit to share the trading signal channel. the signal_processor.py shoul just return 'BUY','SELL','NONE'

To test signal detection independently, run `signal_processor.py`:
```bash
python signal_processor.py
```

This script captures a frame from the video stream, analyzes it for predefined color patterns, and prints the detected trading signal.

### Starting the Trading Bot:
Execute `trader.py` to start the trading bot:

```bash
python trader.py
````
Ensure signal_processor.py is accessible from trader.py for importing. The trading bot will use the signals detected to perform trades on the Binance platform.

### Disclaimer
This project is intended for educational purposes only and should be used with caution. Test your strategy with a demo account before applying real funds. The creator is not liable for any financial losses incurred from using this bot.

### Contributing
Contributions to this project are welcome! Feel free to fork the repository, make improvements or fix bugs, and submit a pull request with your changes.

### License
General use
