# mm-to-mw2
MacMoney to MoneyWiz2 Converter

Insipired by https://github.com/chitsaou/macmoney-to-moneywiz, this tools it for converting MacMoney database (`*.plist`) into MoneyWiz2-importable file (`*.csv`).

## Prerequisite

- Python 3.6
- Identify MacMoney database location (default in `./Library/Application Support/MacMoney/`)

## How-To

1. Clone repo or download files
2. Modify `CATEGORY_MAP` in `mm-to-mw2.py` to add missing MacMoney categories
3. Run the script with:
```bash
$ python3.6 mm-to-mw.py "./Library/Application Support/MacMoney/default.plist"
MacMoney database successfully converted into ~/Downloads/default.csv

Please manually create the following account(s) in MoneyWiz2 before import:

Account Name	Opening Balance
-------------------------------
現金        	0
銀行存款      	0
應收帳款      	0
信用卡       	0
貸款        	0
```

## CLI Usage

```bash
usage: mm-to-mw.py [-h] PLIST [OUTPUT]

positional arguments:
  PLIST       input path to MacMoney database in .plist format
  OUTPUT      output path to .csv file for MoneyWiz2, default to ~/Downloads/
              folder

optional arguments:
  -h, --help  show this help message and exit
```
