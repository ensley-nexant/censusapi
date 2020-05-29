# Census API

## Setup

First, sign up for an API key [on the Census developer page](https://www.census.gov/developers/).
Once you have received your key, save it in a file named `.env` and place it in
the root directory of this project. The file's contents should look like this:

```
CENSUS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Then, install the requirements listed in `requirements.txt`.

## Usage

To pull the median household incomes of every census tract in Illinois and 
save the results in `income.csv`, run

```python
from census import api

median_income_il = api.ACSDataset()
median_income_il.load('B19013_001E', geography='tract', state='17')
median_income_il.to_csv('income.csv')
```

For more details, see `notebooks/test_api.ipynb`.