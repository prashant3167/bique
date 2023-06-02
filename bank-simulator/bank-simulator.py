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
# BANK = 'BNP PARIBAS'

print(os.getcwd())
home_dir = os.path.expanduser('~')
file_path = os.path.join(os.getcwd(), 'accounts.json')

# Collecting the accounts belonging to the specific bank
with open(file_path, 'r') as f:
    all_accounts = json.load(f)

result_dict = {}
last_tr = {}
for entry in all_accounts:
    id_value = entry['id']
    accounts_dict = {}
    for account in entry['accounts']:
        iban_value = account['iban']
        amount_value = account.get('amount', None)  # If 'amount' key doesn't exist, return None
        accounts_dict[iban_value] = amount_value
        last_tr[iban_value] = datetime(2022, 1, 1)
    result_dict[id_value] = accounts_dict

# Print the resulting dictionary
print(result_dict)


# Print the final JSON data
# print(final_json_str)


CATEGORIES = ["groceries", "entertainment", "shopping", "utilities", "travel", "food delivery", "transfer", "income", "refund", "other"]
ct = {
    'groceries': {'min': 0.5, 'max': 100.0},
    'entertainment': {'min': 10, 'max': 120},
    'shopping': {'min': 1, 'max': 100},
    'utilities': {'min': 0.8, 'max': 100},
    'travel': {'min': 10, 'max': 800},
    'food delivery': {'min': 5, 'max': 40},
    'transfer': {'min': 20, 'max': 200},
    'income': {'min': 80, 'max': 1000},
    'refund': {'min': 10, 'max': 300},
    'other': {'min': 1, 'max': 200}
}
# Generate a random transaction object
def generate_transaction(user_name,account,bank):
    transaction = {}
    balance = result_dict[user_name][account]
    transaction['id'] = str(uuid.uuid4())
    delta = end_date - start_date
    random_second = random.randint(60, 2000)
    tr_date = last_tr[account] + timedelta(minutes=random_second)
    last_tr[account] = tr_date
    transaction['date'] = str(tr_date)
    transaction['bookingDateTime'] = transaction['date']
    transaction['valueDateTime'] = str(tr_date + timedelta(hours=6))
    transaction['status'] = "BOOKED"
    transaction['balance'] = {
        'type': 'INTERIM_BOOKED',
        'balanceAmount': {'amount': balance, 'currency': 'Euro'}
    }
    if balance<0:
        transaction['description'] = random.choice(["income", "refund"] )
    else:
        transaction['description'] = random.choice(CATEGORIES)
    transaction['transactionInformation'] = [transaction['description']]
    amount = round(random.uniform(ct[transaction['description']]['min'], min(balance / 2,ct[transaction['description']]['max'])), 2)
    transaction['amount'] = amount if transaction['description'] in ["income", "refund"] else -amount
    transaction['currency'] = transaction['balance']['balanceAmount']['currency']
    transaction['transactionAmount'] = {'amount': transaction['amount'], 'currency': transaction['currency']}

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

    transaction['isoBankTransactionCode'] = {
        'domainCode': {'code': 'Payments', 'name': 'PMNT'},
        'familyCode': {},
        'subFamilyCode': {'code': 'DMCT', 'name': 'Domestic Credit Transfer'}
    }

    if transaction['amount'] < 0:
        transaction['isoBankTransactionCode']['familyCode'].update({'code': 'ICDT', 'name': 'Issued Credit Transfers'})
    else:
        transaction['isoBankTransactionCode']['familyCode'].update({'code': 'RCDT', 'name': 'Received Credit Transfers'})

    transaction['proprietaryBankTransactionCode'] = {'code': '', 'issuer': bank} ### Issuer is the name of the bank and for the code multiple values are possible: CARD_PAYMENT, TRANSFER, INCOME, REFUND, OTHER
    description_mapping = {
    "transfer": "TRANSFER",
    "income": "INCOME",
    "refund": "REFUND",
    "other": "OTHER"
}

    transaction['proprietaryBankTransactionCode']['code'] = description_mapping.get(transaction['description'], "CARD_PAYMENT")
    result_dict[user_name][account] = balance+transaction['amount']

    return transaction

# Generate a list of random transactions
def generate_transactions(user_name,account, num_transactions):
    # BALANCE = round(random.uniform(MIN_AMOUNT, MAX_AMOUNT),2) 
    
    transactions = []
    for i in range(num_transactions):
        transaction = generate_transaction(user_name,account["iban"],account["bank"])
        transactions.append(transaction)
        # BALANCE = BALANCE + transaction['amount']
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

try:
    if __name__ == '__main__':
        # for account in ACCOUNTS:
        for i in range(1000):
            individual_person = random.choice(all_accounts)
            # print(individual_data)
            individual_account = random.choice(individual_person["accounts"])
            transactions = generate_transactions(individual_person["id"],individual_account, 20)
            
            # print(transactions)
            send_requests(transactions)
            json_data = json.dumps(transactions, indent=4)
            # print(json_data)
except KeyboardInterrupt:
    final_json = []
    for entry in all_accounts:
        id_value = entry['id']
        accounts = []
        if id_value in result_dict:
            for account in entry['accounts']:
                iban_value = account['iban']
                amount_value = result_dict[id_value].get(iban_value)
                account_dict = {
                    "iban": iban_value,
                    "aba": account['aba'],
                    "bank": account['bank']
                }
                if amount_value is not None:
                    account_dict['amount'] = amount_value
                accounts.append(account_dict)
        else:
            accounts = entry['accounts']
        final_json.append({
            "name": entry['name'],
            "id": id_value,
            "accounts": accounts
        })

    # Convert final JSON to string
    final_json_str = json.dumps(final_json, indent=4)
    print(final_json_str)
    print("Ctrl+C pressed. Exiting...")
        
    # print(json_data)



final_json = []
for entry in all_accounts:
    id_value = entry['id']
    accounts = []
    if id_value in result_dict:
        for account in entry['accounts']:
            iban_value = account['iban']
            amount_value = result_dict[id_value].get(iban_value)
            account_dict = {
                "iban": iban_value,
                "aba": account['aba'],
                "bank": account['bank']
            }
            if amount_value is not None:
                account_dict['amount'] = amount_value
            accounts.append(account_dict)
    else:
        accounts = entry['accounts']
    final_json.append({
        "name": entry['name'],
        "id": id_value,
        "accounts": accounts
    })

# Convert final JSON to string
final_json_str = json.dumps(final_json, indent=4)
print(final_json_str)
print(last_tr)