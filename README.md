# partiful-analytics

because partiful won't give me a fucking API

<img width="100%" alt="Screen Shot 2023-10-16 at 9 22 45 PM" src="https://github.com/cooltoast/partiful-analytics/assets/3195381/4ad43eea-3899-4076-9c1c-5da47d1c2980">
- https://twitter.com/partiful/status/1623361004326293514

## setup

### scrape data
- open partiful.com
- use chrome debugger tools to get `/getGuestsV2` output
- save output to `YEAR.json`

### installation
```
pyenv virtualenv <version> partiful
pyenv activate partiful
pip install -r requirements.txt
```

## run
```
python analyze.py
```
