from urllib import response
import CryptUtil
import SQLiteUtil

if __name__ == '__main__':
    # CryptUtil.RSAKeyPairFilesGenerator()
    # SQLiteUtil.createNewDatabase()
    # SQLiteUtil.insertTrade("AAA","BBB")
    publicKeyBase64=CryptUtil.bytesToBase64String(CryptUtil.readBytes("PublicKey.pem"))
    print(publicKeyBase64)