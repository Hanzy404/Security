import requests
import json

UIDPASS_FILE = "uidpass.json"
TOKEN_FILE = "tokens.json"

# UPDATE URL YANG MASIH HIDUP
API_URLS = [
    "https://api.ff-token-generator.com/token",
    "https://ff-token-maker.vercel.app/token",
    "https://token-generator-ff.up.railway.app/token"
]

def read_uidpass():
    with open(UIDPASS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_token(uid, password):
    for api in API_URLS:
        try:
            url = f"{api}?uid={uid}&password={password}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            token = data.get("token") or data.get("access_token")
            if token:
                print(f"✅ Token found from {api}")
                return token
        except:
            continue
    print(f"❌ No token for UID {uid}")
    return None

def update_token_file(token_list):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(token_list, f, ensure_ascii=False, indent=4)

def main():
    uidpass_list = read_uidpass()
    new_tokens = []
    
    for item in uidpass_list:
        token = fetch_token(item["uid"], item["password"])
        if token:
            new_tokens.append({"token": token})
    
    if new_tokens:
        update_token_file(new_tokens)
        print(f"✅ tokens.json updated with {len(new_tokens)} tokens")
    else:
        print("❌ No tokens updated. API might be down.")

if __name__ == "__main__":
    main()
