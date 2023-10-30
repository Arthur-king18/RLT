# RLT

## Install dependencies

```
pip install poetry
```
```
poetry shell && poetry install
```

## Run

```python
python3 main.py
```

# Json filter

``` python
class IsJsonRequest(Filter):
    async def check(self, message: types.Message) -> bool:
        return message.text.startswith("{") and message.text.endswith("}")
```
## Use

``` python
@dp.message_handler(IsJsonRequest())
async def aggregation_handler(message: types.Message):
```


