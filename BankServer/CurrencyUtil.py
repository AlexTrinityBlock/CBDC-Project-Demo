import uuid

def newCurrency():
    return str(uuid.uuid4())

def saveCurrencyToBankSQL():
    return