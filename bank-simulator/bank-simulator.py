import json
import random
from datetime import date, datetime, timedelta
import os
import uuid

# Set up some constants for generating the data
ACCOUNTS = []
MIN_AMOUNT = 1000.0
MAX_AMOUNT = 100000.0
start_date = datetime(2015, 1, 1)
end_date = datetime(2023, 3, 31)
# BANK = 'BNP PARIBAS'
all_data_last = [{ "maxDate" : "2019-07-16 01:07:00", "source" : "ES82BRNV50362515161643", "username" : "601112289563", "bank" : "CAXIFY" },
{ "maxDate" : "2020-11-08 19:36:00", "source" : "ES96IYEG91874376557670", "username" : "79991717339", "bank" : "Revolut" },
{ "maxDate" : "2020-01-24 02:12:00", "source" : "ES15PMJF76077940962764", "username" : "923356081155", "bank" : "Revolut" },
{ "maxDate" : "2021-01-10 06:55:00", "source" : "ES37BTHI66142921389526", "username" : "2349096989688", "bank" : "CAXIFY" },
{ "maxDate" : "2020-04-02 22:21:00", "source" : "ES40YJZV47112222025735", "username" : "4407856777592", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2020-10-04 23:56:00", "source" : "ES36FCTS64658750643608", "username" : "381603212015", "bank" : "CAXIFY" },
{ "maxDate" : "2020-05-04 20:00:00", "source" : "ES71SGEO34917464726554", "username" : "522224464882", "bank" : "Revolut" },
{ "maxDate" : "2019-12-22 17:53:00", "source" : "ES77NJQE77047041012170", "username" : "527774420427", "bank" : "CAXIFY" },
{ "maxDate" : "2019-11-08 08:28:00", "source" : "ES42XHWG72122874552101", "username" : "923318942708", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2022-05-13 21:53:00", "source" : "ES71NOAJ71220223724423", "username" : "998900144775", "bank" : "CAXIFY" },
{ "maxDate" : "2021-05-12 09:41:00", "source" : "ES13QIUR81022149639616", "username" : "34655177477", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2020-10-21 16:34:00", "source" : "ES07VMCF08045263509013", "username" : "79037361629", "bank" : "Revolut" },
{ "maxDate" : "2019-12-25 20:02:00", "source" : "ES90UCJB46821283216081", "username" : "923318942708", "bank" : "CAXIFY" },
{ "maxDate" : "2019-12-11 01:52:00", "source" : "ES94MGOX24383485209294", "username" : "522224464882", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2022-09-05 16:22:00", "source" : "ES88CCPI11345836728456", "username" : "6285716186264", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2020-08-01 06:57:00", "source" : "ES59AAGT22664585788290", "username" : "97333894773", "bank" : "CAXIFY" },
{ "maxDate" : "2020-11-11 23:15:00", "source" : "ES48ROFG41777104049405", "username" : "972599283598", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2020-04-08 14:10:00", "source" : "ES26WZJF60652375702196", "username" : "522224464882", "bank" : "Revolut" },
{ "maxDate" : "2020-06-15 01:49:00", "source" : "ES18BZVP64089987860702", "username" : "381691712999", "bank" : "CAXIFY" },
{ "maxDate" : "2020-03-12 16:43:00", "source" : "ES50PNXR90722758581112", "username" : "923356081155", "bank" : "Revolut" },
{ "maxDate" : "2020-11-23 13:07:00", "source" : "ES02JHOP23942038749660", "username" : "972599283598", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2020-02-09 05:18:00", "source" : "ES51HUSE74479811018646", "username" : "573022513712", "bank" : "Revolut" },
{ "maxDate" : "2019-11-28 23:34:00", "source" : "ES38MQAZ97473816310151", "username" : "527774420427", "bank" : "CAXIFY" },
{ "maxDate" : "2020-09-05 16:18:00", "source" : "ES86EHAN74451586919070", "username" : "919920866202", "bank" : "Revolut" },
{ "maxDate" : "2020-05-26 01:00:00", "source" : "ES10CZMY52089344286339", "username" : "8618523459562", "bank" : "CAXIFY" },
{ "maxDate" : "2020-12-17 05:03:00", "source" : "ES45VAET34604305920487", "username" : "8618523459562", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2020-04-10 14:10:00", "source" : "ES06WFGU72983192679063", "username" : "34671295311", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2022-05-28 22:20:00", "source" : "ES48TVAT92082523971182", "username" : "94711937271", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2020-08-02 02:27:00", "source" : "ES85ASPZ17863114875062", "username" : "79991717339", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2020-01-01 13:06:00", "source" : "ES47KNCP50924250080985", "username" : "923318942708", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2022-08-10 03:15:00", "source" : "ES07BRTX96146666164355", "username" : "491746890263", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2020-09-26 06:40:00", "source" : "ES17WJIZ77984516215419", "username" : "381603212015", "bank" : "CAXIFY" },
{ "maxDate" : "2020-12-21 19:37:00", "source" : "ES60NIFE43775832526006", "username" : "79037361629", "bank" : "Revolut" },
{ "maxDate" : "2020-05-10 12:52:00", "source" : "ES31FXLT47899970226923", "username" : "34671295311", "bank" : "CAXIFY" },
{ "maxDate" : "2020-11-12 17:53:00", "source" : "ES97QOCE75072324547599", "username" : "2349096989688", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2020-05-11 13:46:00", "source" : "ES65OGJR97362838925428", "username" : "355673879824", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2022-11-03 02:28:00", "source" : "ES28XQDZ32700977223703", "username" : "96181838392", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2020-03-06 01:42:00", "source" : "ES20NYZY95100092390963", "username" : "355673879824", "bank" : "Revolut" },
{ "maxDate" : "2020-03-28 12:41:00", "source" : "ES54YDKA34088475960103", "username" : "355673879824", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2020-01-04 03:05:00", "source" : "ES21FMON17941820870111", "username" : "381691712999", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2021-05-04 18:21:00", "source" : "ES03GWNO51408147941807", "username" : "97333894773", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2020-07-09 14:39:00", "source" : "ES53NSTK48798834643638", "username" : "527774420427", "bank" : "Revolut" },
{ "maxDate" : "2019-12-15 00:43:00", "source" : "ES82XTWJ12432219269784", "username" : "381691712999", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2020-01-31 21:35:00", "source" : "ES18IAHB34005653831616", "username" : "923318942708", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2020-09-19 06:46:00", "source" : "ES25ANSP48014967799833", "username" : "919920866202", "bank" : "BNP PARIBAS" },
{ "maxDate" : "2020-08-18 20:21:00", "source" : "ES37LZNC68377459218865", "username" : "923356081155", "bank" : "CAXIFY" },
{ "maxDate" : "2019-12-11 11:40:00", "source" : "ES80VTMK41090431522919", "username" : "34671295311", "bank" : "CAXIFY" }]

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
        last_tr[iban_value] = datetime(2019, 1, 1)
    result_dict[id_value] = accounts_dict

# Print the resulting dictionary
# print(result_dict)


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
def generate_transaction(user_name,account,bank,last_transaction):
    transaction = {}
    balance = result_dict[user_name][account]
    transaction['id'] = str(uuid.uuid4())
    delta = end_date - start_date
    random_second = random.randint(10, 300)
    tr_date = last_tr[account] + timedelta(minutes=random_second)
    last_tr[account] = tr_date
    transaction['source'] = account
    transaction['username'] = user_name
    transaction['date'] = str(tr_date)
    transaction['bookingDateTime'] = transaction['date']
    transaction['valueDateTime'] = str(tr_date + timedelta(hours=6))
    transaction['status'] = "BOOKED"
    transaction['balance'] = {
        'type': 'INTERIM_BOOKED',
        'balanceAmount': {'amount': balance, 'currency': 'Euro'}
    }
    if balance<10:
        transaction['description'] = random.choice(["income", "refund"] )
    else:
        transaction['description'] = random.choice(CATEGORIES)
    transaction['transactionInformation'] = [transaction['description']]
    amount = round(random.uniform(ct[transaction['description']]['min'], ct[transaction['description']]['max']), 2)
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
    # print(balac)
    transaction['proprietaryBankTransactionCode']['code'] = description_mapping.get(transaction['description'], "CARD_PAYMENT")
    result_dict[user_name][account] = balance+transaction['amount']

    return tr_date,transaction

# Generate a list of random transactions
def generate_transactions(user_name,account, last_transaction,bank):
    # BALANCE = round(random.uniform(MIN_AMOUNT, MAX_AMOUNT),2) 
    datetime_obj = datetime.strptime(last_transaction, "%Y-%m-%d %H:%M:%S")
    transactions = []
    # for i in range(num_transactions):
    last_day = datetime(2023,6,1)
    while datetime_obj < last_day:
        datetime_obj,transaction = generate_transaction(user_name,account,bank,datetime_obj)
        if transaction:
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
        for i in range(20000):
            individual_person = random.choice(all_accounts)
            # print(individual_data)
            individual_account = random.choice(individual_person["accounts"])
            transactions = generate_transactions(individual_person["id"],individual_account, 100)
            
            # print(transactions)
            send_requests(transactions)
            # json_data = json.dumps(transactions, indent=4)
            # from pprint import pprint
            # pprint(json_data)
            # input()
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
    with open("final_accounts.json", "w+") as f:
        f.write(final_json_str)
    # print(final_json_str)
    print('Last transaction')
    print(last_tr)
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
with open("final_accounts.json", "w+") as f:
    f.write(final_json_str)
# print(final_json_str)
print('Last transaction')
print(last_tr)
