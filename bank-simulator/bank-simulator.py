import json
import random
from datetime import date, datetime, timedelta

# Set up some constants for generating the data
ACCOUNTS = {'Zyad':"123456789", 'Prashant':"234567890", 'Rishika':"345678901"}
CATEGORIES = ["groceries", "entertainment", "shopping", "utilities", "travel"]
DATES = ["13-04-2023", "14-04-2023", "15-04-2023", "16-04-2023"]
MIN_AMOUNT = 1.0
MAX_AMOUNT = 100000.0


# Generate a random transaction object
def generate_transaction(user_name):
    transaction = {}
    transaction['id'] = [ACCOUNTS.get(name) for name in ACCOUNTS if name == user_name][0]
    transaction['date'] = random.choice(CATEGORIES)
    transaction['bookingDateTime'] = random.choice(DATES)
    transaction['valueDateTime'] = datetime.strftime(datetime.strptime(transaction['bookingDateTime'], "%d-%m-%Y") + timedelta(days = 1), "%d-%m-%Y")
    transaction['status'] = "BOOKED"
    transaction['amount'] = 0.0 ### when generating the data, we need to take into consideration whether it is debited or credited (in this case we also need to check if it is less than the balance) because this affects the family code
    transaction['currency'] = chr(8364) ### supposedly the euro sign
    transaction['transactionAmount']= {'amount':transaction['amount'], 'currency':transaction['currency']}
    transaction['description'] = "random description"
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
    transaction['proprietaryBankTransactionCode'] = {'code': '', 'issuer':''} ### Issuer is the name of the bank and for the code multiple values are possible: CARD_PAYMENT, TRANSFER, TOPUP, EXCHANGE, CARD_REFUND
    transaction['balance'] = {'type' : '', 'balanceAmount' : {'amount': 0.0, 'currency': ''}}
    transaction['merchant'] = {'merchantName' :'', 'merchantGroup':''} ### Information about the other party
    transaction['enrichment'] = {'categorisation': {'categories': '', 'source': ''}, 'transactionHash':{'hash': ''}, 'cleansedDescription':transaction['description']} ### 
    transaction['supplementaryData'] = {'UserComments':''} ### Transfers  description, can be general text

    return transaction

# Generate a list of random transactions
def generate_transactions(user_name, num_transactions):
    transactions = []
    for i in range(num_transactions):
        transaction = generate_transaction(user_name)
        transactions.append(transaction)
    return transactions

# Generate some sample transactions and output them in JSON format
if __name__ == '__main__':
    transactions = generate_transactions('Zyad', 1)
    json_data = json.dumps(transactions, indent=4)
    print(json_data)


# import json
# import jsonschema

# # Load the JSON file
# with open('/home/zyad/Desktop/transaction-data-zyad.json', 'r') as f:
#     data = json.load(f)

# # Extract the schema
# schema = jsonschema.Draft7Validator.schema(data)

# # Print the schema
# print(json.dumps(schema, indent=4))
