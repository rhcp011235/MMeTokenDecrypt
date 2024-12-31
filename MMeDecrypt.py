import base64,subprocess , os
import hashlib
import hmac
import plistlib
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7


# Auto get the key needed
iCloudKey = subprocess.check_output("security find-generic-password -ws 'iCloud' | awk {'print $1'}", shell=True).decode("utf-8").replace("\n", "")
if iCloudKey == "":
    print("ERROR getting iCloud Decryption Key")
    sys.exit()
key = base64.b64decode(iCloudKey)


path = "/Users/rhcp/Library/Application Support/iCloud/Accounts/"
files = os.listdir(path)

# Filter out the numerical value
numerical_value = next((f for f in files if f.isdigit()), None)



dsid = numerical_value

encryped_file_path = (
    Path.home() / "Library/Application Support/iCloud/Accounts" / str(dsid)
    )

encryped_file = open(encryped_file_path, "rb").read()
HMAC_KEY = b"t9s\"lx^awe.580Gj%'ld+0LG<#9xa?>vb)-fkwb92[}"
hashed = hmac.new(HMAC_KEY, key, digestmod=hashlib.md5).digest()
cipher = Cipher(algorithms.AES(hashed), modes.CBC(b"\0" * 16))
decryptor = cipher.decryptor()
decrypted_key = decryptor.update(encryped_file) + decryptor.finalize()
unpadder = PKCS7(128).unpadder()
decrypted_key = unpadder.update(decrypted_key) + unpadder.finalize()
print(plistlib.loads(decrypted_key))
