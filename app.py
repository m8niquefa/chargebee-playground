import os
from dotenv import load_dotenv

load_dotenv()

CHARGE_BEE_API_KEY = os.environ.get("CHARGE_BEE_API_KEY")
CHARGE_BEE_URL = os.environ.get("CHARGE_BEE_URL")


if CHARGE_BEE_API_KEY is None:
    print("Environment variable CHARGE_BEE_API_KEY not found")
    exit()


if CHARGE_BEE_URL is None:
    print("Environment variable CHARGE_BEE_URL not found")
    exit()

print(CHARGE_BEE_API_KEY)
print(CHARGE_BEE_URL)