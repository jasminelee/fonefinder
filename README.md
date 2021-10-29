# FoneFinder
Python wrapper for the fonefinder website. Get the following information from a phone number: city, state, carrier, 
telco type.

## Usage
Run `python3 -m pip install -r requirements.txt` and then in your project, 
```python
import fonefinder as f
print(f.FoneFinder('1234567890').info)
```

To run unit tests, `python3 -m unittest tests/test_fonefinder.py`

## TODO
Support non-US phone numbers.

DRY up unit tests.

Add PEP8 autoformatter.

Optional: support static typing.

