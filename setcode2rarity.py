import requests
import time

# Function to fetch card set info from the API
def fetch_card_set_info(set_code):
    url = f"https://db.ygoprodeck.com/api/v7/cardsetsinfo.php?setcode={set_code}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    return {}

# Load the TXT file
filename = 'codes.txt'  # Replace with your TXT file path

# RateLimiter class to limit requests per second
class RateLimiter:
    def __init__(self, rate_limit):
        self.rate_limit = rate_limit
        self.tokens = self.rate_limit
        self.last_refill_time = time.time()

    def get_token(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_refill_time
        self.tokens = min(self.rate_limit, self.tokens + elapsed_time * self.rate_limit)
        self.last_refill_time = current_time
        return self.tokens >= 1

# Create a rate limiter with a limit of 20 requests per second
limiter = RateLimiter(20)

with open(filename, 'r') as file:
    for line_number, line in enumerate(file, start=1):
        set_code = line.strip()  # Remove leading/trailing whitespaces
        if limiter.get_token():
            try:
                card_set_info = fetch_card_set_info(set_code)
                if card_set_info:
                    set_name = card_set_info.get('set_name')
                    set_rarity = card_set_info.get('set_rarity')
                    if set_name and set_rarity:
                        print(f"{set_rarity},{set_name}")
                    else:
                        print(f"No matching set found for Set Code: {set_code}")
                else:
                    print(f"No data found for Set Code: {set_code}")
            except Exception as e:
                print(f"An error occurred while processing line {line_number}: {str(e)}")
        else:
            print("Rate limit exceeded. Waiting for tokens to refill...")
            time.sleep(0.05)  # Wait for 0.05 seconds to allow tokens to refill
