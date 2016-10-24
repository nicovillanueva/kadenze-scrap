# Kadenze Scrapper

## Requirements
- Python 3
- Google Chrome or Firefox
- chromedriver (for running Chrome, duh)

`# apt install chromium-chromedriver`

## Python dependencies
- selenium
- requests
- tqdm (optional: Required for `--progress`)

`pip3 install tqdm requests selenium`

Virtualenv recommended, as usual.

(In order to install pip itself: `# apt install python3-pip`)

## Configuring
Set your credentials in lines 9 and 10. If you don't do so, you'll be prompted for them as soon as the script launches.

## Running
- `--browser`: Set which browser do you want to use to scrap. Possibles: "firefox", "chrome". Default: Chrome
- `--progress`: Show download speed. Possibles: "true", "false". Default: false

Sorry Kadenze
