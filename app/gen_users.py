# Generating the SQL queries and saving them to a file

import random
import faker

# Initialize Faker to generate random data
fake = faker.Faker()

def generate_random_user():
    return {
        "phone": fake.phone_number(),
        "subscriber_mts": random.choice([True, False]),
        "tariff": fake.word(),
        "mobile_network": random.choice([True, False]),
        "home_internet": random.choice([True, False]),
        "home_tv": random.choice([True, False]),
        "home_phone": random.choice([True, False]),
        "device": fake.word(),
        "os": random.choice(["Android", "iOS", "Windows"]),
        "my_mts_app_user": random.choice([True, False]),
        "personal_cabinet_user": random.choice([True, False]),
        "mts_bank_app_user": random.choice([True, False]),
        "mts_money_app_user": random.choice([True, False]),
        "subscriptions_services_on_number": random.choice([True, False]),
        "mts_premium": random.choice([True, False]),
        "mts_cashback": random.choice([True, False]),
        "basic_defender": random.choice([True, False]),
        "defender_plus": random.choice([True, False]),
        "separate_subscription_kion": random.choice([True, False]),
        "separate_subscription_music": random.choice([True, False]),
        "separate_subscription_stroki": random.choice([True, False]),
        "debit_card_mts_bank": random.choice([True, False]),
        "credit_card_mts_bank": random.choice([True, False]),
        "debit_card_mts_money": random.choice([True, False]),
        "credit_card_mts_money": random.choice([True, False]),
        "virtual_card_mts_money": random.choice([True, False]),
    }

def generate_insert_queries(n=100):
    queries = []
    for _ in range(n):
        user_data = generate_random_user()
        columns = ", ".join(user_data.keys())
        values = ", ".join([repr(value) for value in user_data.values()])
        query = f"INSERT INTO users ({columns}) VALUES ({values});"
        queries.append(query)
    return queries

# Generate the queries
queries = generate_insert_queries(100)

# Saving the queries to a file
file_path = 'random_users.sql'
with open(file_path, 'w') as file:
    for query in queries:
        file.write(query + '\n')

file_path  # Returning the file path so it can be accessed by the user.
