
`pip install pipreqs`

`pipreqs ./ --encoding=utf8 --force`

```
pip install -r requirements.txt
or
conda install --yes --file requirements.txt
```
---

`pip download -d ./packages -r requirements.txt`

```
pip install --no-index --find-links=./packages -r requirements.txt
pip install --no-index --ignore-installed --find-links=./packages -r requirements.txt
```