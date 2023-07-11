import requests
import time

# Function to fetch card info from the API
def fetch_card_info(name):
    url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('data', [])[0].get('card_sets', [])
    return []

# Function to match SET with set_name and return set_code and set_rarity
def match_set_info(card_sets, set_name):
    for card_set in card_sets:
        if card_set['set_name'] == set_name:
            return card_set['set_code'], card_set['set_rarity']
    return None, None

# Load the TXT file
filename = 'cards.txt'  # Replace with your TXT file path

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
        name, set_name = line.strip().split('^')
        if limiter.get_token():
            try:
                card_sets = fetch_card_info(name)
                set_code, set_rarity = match_set_info(card_sets, set_name)
                if set_code and set_rarity:
                    # print(f"Card: {name}, Set: {set_name}, Set Code: {set_code}, Set Rarity: {set_rarity}")
                    print(f"{set_rarity},{set_code}")
                else:
                    print(f"No matching set found for Card: {name}, Set: {set_name}")
            except Exception as e:
                print(f"An error occurred while processing line {line_number}: {str(e)}")
        else:
            print("Rate limit exceeded. Waiting for tokens to refill...")
            time.sleep(0.05)  # Wait for 0.05 seconds to allow tokens to refill
