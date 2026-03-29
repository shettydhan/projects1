"""
Generate large sample dataset for testing
Creates 2500 rows with realistic employee data
"""
import pandas as pd
import random
from datetime import datetime, timedelta

# Configuration
NUM_ROWS = 2500
OUTPUT_FILE = "large_sample_data.csv"

print(f"Generating {NUM_ROWS} rows of sample data...")

# Sample data pools
first_names = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Carol", "Kevin", "Amanda", "Brian", "Dorothy", "George", "Melissa",
    "Edward", "Deborah", "Ronald", "Stephanie", "Timothy", "Rebecca", "Jason", "Sharon",
    "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
    "Nicholas", "Shirley", "Eric", "Angela", "Jonathan", "Helen", "Stephen", "Anna",
    "Larry", "Brenda", "Justin", "Pamela", "Scott", "Nicole", "Brandon", "Emma",
    "Benjamin", "Samantha", "Samuel", "Katherine", "Raymond", "Christine", "Gregory", "Debra",
    "Frank", "Rachel", "Alexander", "Catherine", "Patrick", "Carolyn", "Jack", "Janet",
    "Dennis", "Ruth", "Jerry", "Maria", "Tyler", "Heather", "Aaron", "Diane"
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
    "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
    "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
    "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
    "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza",
    "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers"
]

departments = ["Engineering", "Marketing", "Sales", "HR", "Finance", "Operations", "IT", "Customer Support"]
cities = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", 
    "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville",
    "Fort Worth", "Columbus", "Charlotte", "San Francisco", "Indianapolis", "Seattle",
    "Denver", "Boston", "Portland", "Nashville", "Detroit", "Memphis", "Baltimore",
    "Miami", "Atlanta", "Minneapolis", "Tampa", "New Orleans", "Cleveland", "Pittsburgh"
]

# Generate data
data = []
start_date = datetime(2023, 1, 1)

for i in range(NUM_ROWS):
    # Generate employee data
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    name = f"{first_name} {last_name}"
    
    # Add some whitespace issues (5% of records)
    if random.random() < 0.05:
        name = f"  {name}  "  # Extra spaces
    
    age = random.randint(22, 65)
    email = f"{first_name.lower()}.{last_name.lower()}@company.com"
    salary = random.randint(35000, 120000)
    department = random.choice(departments)
    
    # Random date in 2023-2024
    random_days = random.randint(0, 730)
    date = start_date + timedelta(days=random_days)
    date_str = date.strftime("%Y-%m-%d")
    
    city = random.choice(cities)
    
    data.append({
        "Name": name,
        "Age": age,
        "Email": email,
        "Salary": salary,
        "Department": department,
        "Date": date_str,
        "City": city
    })

# Add some duplicates (2% of data)
num_duplicates = int(NUM_ROWS * 0.02)
for _ in range(num_duplicates):
    duplicate = random.choice(data).copy()
    data.append(duplicate)

print(f"  Added {num_duplicates} duplicate records")

# Add some empty rows (1% of data)
num_empty = int(NUM_ROWS * 0.01)
for _ in range(num_empty):
    data.insert(random.randint(0, len(data)), {
        "Name": None,
        "Age": None,
        "Email": None,
        "Salary": None,
        "Department": None,
        "Date": None,
        "City": None
    })

print(f"  Added {num_empty} empty records")

# Shuffle data
random.shuffle(data)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv(OUTPUT_FILE, index=False)

print(f"\n✅ Generated {OUTPUT_FILE}")
print(f"📊 Total rows: {len(df)}")
print(f"📊 Expected after cleaning: ~{NUM_ROWS} rows")
print(f"📊 Duplicates to remove: ~{num_duplicates}")
print(f"📊 Empty rows to remove: ~{num_empty}")
print(f"\nFile location: {OUTPUT_FILE}")
print("\n🚀 Ready to upload to dashboard!")
