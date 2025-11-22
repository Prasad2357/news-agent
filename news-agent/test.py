import os
from dotenv import load_dotenv
load_dotenv()
print(os.getenv("DIGEST_FROM_EMAIL"))
print(os.getenv("DIGEST_SMTP_PASSWORD"))