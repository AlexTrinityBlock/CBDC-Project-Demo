import CryptUtil
import AccountUtil
import CurrencyUtil
import SQLiteUtil
import VerifyUtil
import json

if __name__ == '__main__':
    hiddenUserInfo=json.dumps(["o9hvXJCmKBDrokM0f9Lukj7nrGHDAkmIGMIZ", "AWMxZhoCQAIZDUoRWWNwWn9dXS1IMH94WgV0fwQvMlgJUUl4", "ZVsHRQUBQQN1EnQHAl98CHpoeVdgUlNkTFFBWmY5DXwtVHcD", "d2cGQFAATE95JkkLc2wDdV94a1hzDG8dXCJVaAcZVVADdkBQ", "fYT2OJoaq4kzDVn4CgJi8R2puAk4UVz4J1d9", "fEysjC6i9NzIh5gyPg2K4Xg9Xl2JKgV8IAl0", "Qhih5Dme68XDr14CRnCMlDvjM3zOM0ptBryd", "hf67gMH0ZMSJedMJmC2SfDeV73aTyKmLFePV", "DI98GOezA631OkZ5CTEChw6T2vyYlwNqSVEM", "J24ltAtCKL1ZKDsJddXZWxobBMzmPfrOu3tf"])
    print(VerifyUtil.findUserInfoFromHiddenInfoByCurrency("5d37e4ff-9549-4569-9fb5-1d35e5801c3a",hiddenUserInfo))