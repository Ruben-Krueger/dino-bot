# Chrome Dino Game Automation

This script uses Selenium WebDriver to automatically play the Chrome Dino game at chromedino.com.

## Prerequisites

- Python 3.x
- Chrome browser installed
- ChromeDriver (compatible with your Chrome version)

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Make sure you have ChromeDriver installed and in your system PATH.

## Running the Script

Simply run:
```bash
python dino_player.py
```

## How it Works

The script:
1. Opens chromedino.com in a Chrome browser
2. Starts the game by pressing spacebar
3. Continuously monitors the game screen for obstacles
4. Makes the dino jump when obstacles are detected

## Notes

- The script uses image processing to detect obstacles
- You may need to adjust the obstacle detection region and threshold based on your screen resolution
- Press Ctrl+C in the terminal to stop the script 