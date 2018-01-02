#!/usr/bin/env python3
import plistlib
import csv
import os
import argparse


CATEGORY_MAP = {
    '': '',

    # default MacMoney categories
    '餐飲費': 'Food & Dining > Other',
    '餐飲費 > 早餐': 'Food & Dining > Dining/Eating Out',
    '餐飲費 > 午餐': 'Food & Dining > Dining/Eating Out',
    '餐飲費 > 晚餐': 'Food & Dining > Dining/Eating Out',
    '交通費': 'Automobile > Other',
    '服裝費': 'Clothing > Clothes',
    '其他支出': 'Other',
    '薪資': 'Salary & Wages',
    '利息收入': 'Other',
    '其他收入': 'Other',
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('plist', metavar='PLIST', type=str, nargs=1, help='input path to MacMoney database in .plist format')
    parser.add_argument('output', metavar='OUTPUT', type=str, nargs='?', help='output path to .csv file for MoneyWiz2, default to ~/Downloads/ folder', default=None)
    args = parser.parse_args()
    return args.plist[0], args.output


def main(plist_path, output_path):
    csv_path = os.path.join(os.path.expanduser('~'), 'Downloads', f'{os.path.splitext(os.path.basename(plist_path))[0]}.csv') if output_path is None else output_path
    missing_categories = []

    # reading MacMoney plist database
    with open(plist_path, 'rb') as plist:
        raw = plistlib.load(plist)

        # opening MoneyWiz2-favored csv file for writing
        with open(csv_path, 'w', newline='') as csvfile:
            # MoneyWiz2-favored starting lines
            csvfile.write('sep=,\n')
            csvfile.write('"Account","Transfers","Description","Payee","Category","Date","Incomes","Expenses"\n')

            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

            for transaction in raw['MainData']:
                account = ''
                transfer = ''
                description = transaction['Note2'].replace('\n', '; ').replace(',', '; ')
                category = ''
                date = transaction['Date'].strftime('%F')
                incomes = ''
                expenses = ''
                payee = ''

                if transaction['Account1'].startswith('A-') or transaction['Account1'].startswith('L-'):
                    # transfer: Account2 transfer to Account1
                    account = transaction['Account2'].split('-')[1]
                    transfer = transaction['Account1'].split('-')[1]
                    expenses = transaction['Amount']

                    if transaction['Account1'].startswith('L-') and transaction['Account2'].startswith('L-'):
                        account, transfer = transfer, account

                    if not description:
                        # add default description if empty
                        if transaction['Account1'].startswith('A-') and transaction['Account2'].startswith('A-'):
                            description = f'transfer from {account} to {transfer}'
                        if transaction['Account1'].startswith('L-') and transaction['Account2'].startswith('L-'):
                            description = f'transfer from {account} to {transfer}'
                        if transaction['Account1'].startswith('L-') and transaction['Account2'].startswith('A-') or \
                                transaction['Account1'].startswith('A-') and transaction['Account2'].startswith('L-'):
                            description = f'pay debt with {account}'

                if transaction['Account1'].startswith('E-'):
                    # expense: Account2 pay to category Account1
                    account = transaction['Account2'].split('-')[1]
                    category = transaction['Account1'].split('-')[1]
                    if transaction['Note1']:
                        category = f"{category} > {transaction['Note1']}"
                    expenses = transaction['Amount']

                if transaction['Account1'].startswith('I-'):
                    # income: payee Account1 pay to Account2
                    payee = transaction['Account1'].split('-')[1]
                    account = transaction['Account2'].split('-')[1]
                    incomes = transaction['Amount']
                    category = transaction['Account1'].split('-')[1]
                    if transaction['Note1']:
                        category = f"{category} > {transaction['Note1']}"

                try:
                    csvwriter.writerow([account, transfer, description, payee, CATEGORY_MAP[category], date, incomes, expenses])
                except KeyError:
                    if category not in missing_categories:
                        missing_categories.append(category)
                    else:
                        raise

    if missing_categories:
        print('Please add the following MacMoney categories with correspondig MoneyWiz2 category into CATEGORY_MAP:')
        for category in missing_categories:
            print(f'- {category}')
    else:
        print(f'MacMoney database successfully converted into {csv_path}\n')

        print('Please manually create the following account(s) in MoneyWiz2 before import:\n')
        print(f'Account Name\tOpening Balance')
        print('-------------------------------')
        for account in raw['Accounts']:
            if account['Type'] in ('A-', 'L-'):
                print(f'{account["Name"]:10}\t{account["Amount"]}')


if __name__ == '__main__':
    main(*parse_args())
