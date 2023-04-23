import json
import random
from datetime import date, datetime, timedelta
import os
import uuid

# Set up some constants for generating the data
ACCOUNTS = []
MIN_AMOUNT = 1000.0
MAX_AMOUNT = 100000.0
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 3, 31)
BANK = 'BNP PARIBAS'

print(os.getcwd())
home_dir = os.path.expanduser('~')
file_path = os.path.join(os.getcwd(), 'accounts.json')

# Collecting the accounts belonging to the specific bank
with open(file_path, 'r') as f:
    all_accounts = json.load(f)
    for acc in all_accounts:
        for bank in acc['accounts']:
            if bank['bank'] == BANK:
                acc_info = {'name':acc['name'], 'id':acc['id'], 'accounts':bank}
                ACCOUNTS.append(acc_info)

CATEGORIES = ["groceries", "entertainment", "shopping", "utilities", "travel", "food delivery", "transfer", "income", "refund", "other"]

# Generate a random transaction object
def generate_transaction(user_name, balance):
    transaction = {}
    transaction['id'] = str(uuid.uuid4())
    delta = end_date - start_date
    random_second = random.randint(0, delta.total_seconds())
    tr_date = start_date + timedelta(seconds=random_second)
    transaction['date'] = str(tr_date)
    transaction['bookingDateTime'] = transaction['date']
    transaction['valueDateTime'] = str(tr_date + timedelta(hours = 6))
    transaction['status'] = "BOOKED"
    transaction['balance'] = {'type' : 'INTERIM_BOOKED', 'balanceAmount' : {'amount': balance, 'currency': 'Euro'}}
    transaction['amount'] = round(random.uniform(balance/-2, balance/2),2) ### when generating the data, we need to take into consideration whether it is debited or credited (in this case we also need to check if it is less than the balance) because this affects the family code
    transaction['currency'] =  transaction['balance']['balanceAmount']['currency']
    transaction['transactionAmount']= {'amount':transaction['amount'], 'currency':transaction['currency']}
    transaction['description'] = random.choice(CATEGORIES)
    transaction['transactionInformation'] = [transaction['description']]
    """
    For the family code, there are two potential values:
    'code':'ICDT'
    'name': 'Issued Credit Transfers' 
    If the amount is negative (withdrawal or payment from the account)
    OR
    'code':'RCDT'
    'name': 'Received Credit Transfers'
    If the amount is positive (deposit or payment to the account)
    """
    transaction['isoBankTransactionCode'] = {'domainCode':{'code': 'Payments', 'name':'PMNT'}, 'familyCode':{'code': '', 'name': ''}, 'subFamilyCode':{'code':'DMCT', 'name':'Domestic Credit Transfer'}}
    if transaction['amount'] < 0:
        transaction['isoBankTransactionCode']['familyCode']['code'] = 'ICDT'
        transaction['isoBankTransactionCode']['familyCode']['name'] = 'Issued Credit Transfers'
    else:
        transaction['isoBankTransactionCode']['familyCode']['code'] = 'RCDT'
        transaction['isoBankTransactionCode']['familyCode']['name'] = 'Received Credit Transfers'  
    transaction['proprietaryBankTransactionCode'] = {'code': '', 'issuer':BANK} ### Issuer is the name of the bank and for the code multiple values are possible: CARD_PAYMENT, TRANSFER, INCOME, REFUND, OTHER
    if transaction['description'] == "transfer":
        transaction['proprietaryBankTransactionCode']['code'] = "TRANSFER"
    elif transaction['description'] == "income":
        transaction['proprietaryBankTransactionCode']['code'] = "INCOME"
    elif transaction['description'] == "refund":
        transaction['proprietaryBankTransactionCode']['code'] = "REFUND"
    elif transaction['description'] == "other":
        transaction['proprietaryBankTransactionCode']['code'] = "OTHER"
    else:
        transaction['proprietaryBankTransactionCode']['code'] = "CARD_PAYMENT"

    return transaction

# Generate a list of random transactions
def generate_transactions(user_name, num_transactions):
    BALANCE = round(random.uniform(MIN_AMOUNT, MAX_AMOUNT),2) 
    transactions = []
    for i in range(num_transactions):
        transaction = generate_transaction(user_name, BALANCE)
        transactions.append(transaction)
        BALANCE = BALANCE + transaction['amount']
    return transactions



import requests
import json
reqUrl = "http://10.4.41.51:8000/ingest/bank"

headersList = {
 "Accept": "*/*",
 "User-Agent": "Thunder Client (https://www.thunderclient.com)",
 "Content-Type": "application/json" 
}

def send_requests(data):
    for j,i in enumerate(data):

        payload = json.dumps(i)
        response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
        # print(response.text)

# Generate some sample transactions and output them in JSON format

if __name__ == '__main__':
    for account in ACCOUNTS:
        transactions = generate_transactions(account['name'], 1234)
        send_requests(transactions)
        json_data = json.dumps(transactions, indent=4)
    
    # print(json_data)


