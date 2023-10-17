# partiful-analytics

because partiful won't give me a fucking API

https://twitter.com/partiful/status/1623361004326293514?lang=en


## setup

### scrape data
- chrome debugger tools to get `/getGuestsV2`
- ```curl ... > YEAR.json```

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
