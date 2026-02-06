import random
import re
import pandas as pd
from faker import Faker

fake = Faker()

# ----------------------------
# Config
# ----------------------------
CATEGORIES = [
    "Mobiles", "Electronics", "Cars", "Apartments", "Furniture",
    "Jobs", "Services", "Bikes", "Laptops", "Fashion"
]

LOCATIONS = [
    "Dubai Marina", "JLT", "Business Bay", "Deira", "Bur Dubai",
    "Al Barsha", "Downtown Dubai", "Sharjah", "Abu Dhabi", "Ajman"
]

NORMAL_TITLE_TEMPLATES = {
    "Mobiles": [
        "{brand} {model} {storage}GB {condition}",
        "{brand} {model} for sale - {condition}",
        "{brand} {model} {storage}GB - with box"
    ],
    "Cars": [
        "{year} {brand} {model} {mileage}km - {condition}",
        "{brand} {model} {year} - {condition}",
        "{year} {brand} {model} - {mileage}km"
    ],
    "Apartments": [
        "{beds}BHK in {area} | {furnishing}",
        "{beds}BR apartment in {area} - {furnishing}",
        "{beds} bedroom apartment for rent in {area}"
    ],
    "Furniture": [
        "{item} - {condition}",
        "{item} for sale - {condition}",
        "{item} - barely used"
    ],
    "Laptops": [
        "{brand} {model} {ram}GB RAM {storage}GB SSD - {condition}",
        "{brand} laptop {ram}GB/{storage}GB - {condition}",
        "{brand} {model} for sale - {condition}"
    ],
}

SPAM_WORDS = [
    "URGENT SALE", "CHEAP", "LIMITED OFFER", "100% ORIGINAL",
    "GUARANTEED", "BEST PRICE", "FREE DELIVERY", "WHATSAPP",
    "CALL NOW", "NO SCAM", "GENUINE", "PROMOTION"
]

EMOJIS = ["🔥", "💯", "✅", "📞", "⚡", "😱", "🚨", "🎉"]

BRANDS = {
    "Mobiles": ["Apple", "Samsung", "Xiaomi", "OnePlus", "Google"],
    "Cars": ["Toyota", "Nissan", "BMW", "Mercedes", "Honda", "Kia"],
    "Laptops": ["Dell", "HP", "Apple", "Lenovo", "Asus"],
    "Electronics": ["Sony", "LG", "Samsung", "JBL", "Bose"],
    "Bikes": ["Yamaha", "Honda", "Suzuki", "Kawasaki"],
    "Fashion": ["Nike", "Adidas", "Zara", "H&M"],
    "Furniture": ["Ikea", "Home Centre", "Pan Emirates"]
}

MODELS = {
    "Apple": ["iPhone 13", "iPhone 14", "iPhone 15 Pro", "iPhone 12"],
    "Samsung": ["S22", "S23 Ultra", "A54", "Note 20"],
    "Toyota": ["Corolla", "Camry", "Yaris", "Land Cruiser"],
    "Nissan": ["Altima", "Patrol", "Sunny", "X-Trail"],
    "BMW": ["X5", "3 Series", "5 Series"],
    "Dell": ["Inspiron", "XPS 13", "Latitude"],
    "HP": ["Pavilion", "Envy", "EliteBook"],
    "Apple_laptop": ["MacBook Air", "MacBook Pro"],
    "Lenovo": ["ThinkPad", "IdeaPad"],
    "Asus": ["ROG", "Vivobook"]
}

FURNITURE_ITEMS = [
    "Sofa set", "Dining table", "Office chair", "Bed frame",
    "Wardrobe", "Coffee table", "TV unit"
]

CONDITIONS = ["New", "Like New", "Used", "Good condition", "Fair"]
FURNISHING = ["Furnished", "Semi-furnished", "Unfurnished"]

def random_phone():
    # UAE-ish looking phone (not real)
    return f"+9715{random.randint(0,9)}{random.randint(1000000,9999999)}"

def random_email():
    return f"{fake.user_name()}@{random.choice(['gmail.com','yahoo.com','outlook.com'])}"

def pick_brand(category):
    if category in BRANDS:
        return random.choice(BRANDS[category])
    return random.choice(["Generic", "Other"])

def pick_model(brand, category):
    if brand == "Apple" and category == "Laptops":
        return random.choice(MODELS["Apple_laptop"])
    return random.choice(MODELS.get(brand, ["Model X", "Model Y", "Model Z"]))

def normal_price(category):
    # Rough realistic ranges (AED)
    ranges = {
        "Mobiles": (500, 4500),
        "Electronics": (200, 5000),
        "Cars": (8000, 180000),
        "Apartments": (2500, 18000),
        "Furniture": (100, 3500),
        "Jobs": (0, 0),
        "Services": (50, 2000),
        "Bikes": (300, 20000),
        "Laptops": (700, 7000),
        "Fashion": (30, 1500)
    }
    lo, hi = ranges.get(category, (100, 5000))
    if lo == hi == 0:
        return 0
    return random.randint(lo, hi)

def make_normal_listing(listing_id):
    category = random.choice(CATEGORIES)
    location = random.choice(LOCATIONS)
    posted_days_ago = random.randint(0, 30)
    seller_type = random.choice(["individual", "business"])
    condition = random.choice(CONDITIONS)

    brand = pick_brand(category)
    model = pick_model(brand, category)

    # Fields by category
    if category == "Cars":
        year = random.randint(2008, 2024)
        mileage = random.randint(15000, 250000)
        title = random.choice(NORMAL_TITLE_TEMPLATES["Cars"]).format(
            year=year, brand=brand, model=model, mileage=mileage, condition=condition
        )
        desc = f"{condition}. Well maintained. Service history available. Located in {location}."
        price = normal_price(category)

    elif category == "Apartments":
        beds = random.randint(1, 4)
        area = location
        furnishing = random.choice(FURNISHING)
        title = random.choice(NORMAL_TITLE_TEMPLATES["Apartments"]).format(
            beds=beds, area=area, furnishing=furnishing
        )
        desc = f"{beds} bedroom apartment in {area}. {furnishing}. Ready to move. Family building."
        price = normal_price(category)

    elif category == "Furniture":
        item = random.choice(FURNITURE_ITEMS)
        title = random.choice(NORMAL_TITLE_TEMPLATES["Furniture"]).format(
            item=item, condition=condition
        )
        desc = f"{item} in {condition}. Pickup from {location}."
        price = normal_price(category)

    elif category == "Laptops":
        ram = random.choice([8, 16, 32])
        storage = random.choice([256, 512, 1024])
        title = random.choice(NORMAL_TITLE_TEMPLATES["Laptops"]).format(
            brand=brand, model=model, ram=ram, storage=storage, condition=condition
        )
        desc = f"{condition}. Battery good. Includes charger. Available in {location}."
        price = normal_price(category)

    else:
        # Generic template
        storage = random.choice([64, 128, 256, 512])
        title = random.choice(NORMAL_TITLE_TEMPLATES.get("Mobiles", ["{brand} {model}"])).format(
            brand=brand, model=model, storage=storage, condition=condition
        )
        desc = f"{condition}. No issues. Can meet in {location}."
        price = normal_price(category)

    return {
        "listing_id": listing_id,
        "category": category,
        "location": location,
        "seller_type": seller_type,
        "posted_days_ago": posted_days_ago,
        "title": title,
        "description": desc,
        "price_aed": price,
        "is_suspicious": 0,
        "suspicious_reason": ""
    }

def inject_suspicious_signals(listing):
    reasons = []

    # 1) Spammy title
    if random.random() < 0.6:
        spam = random.choice(SPAM_WORDS)
        emoji = random.choice(EMOJIS)
        listing["title"] = f"{spam} {emoji} {listing['title']}".upper()
        reasons.append("spam_title_caps")

    # 2) Add WhatsApp / phone number
    if random.random() < 0.5:
        listing["description"] += f" Contact WhatsApp {random_phone()}"
        reasons.append("phone_in_description")

    # 3) Add email
    if random.random() < 0.25:
        listing["description"] += f" Email: {random_email()}"
        reasons.append("email_in_description")

    # 4) Price anomaly (very low)
    if listing["category"] in ["Mobiles", "Cars", "Laptops", "Electronics", "Apartments"]:
        if random.random() < 0.55:
            listing["price_aed"] = max(1, int(listing["price_aed"] * random.uniform(0.05, 0.25)))
            reasons.append("price_too_low")

    # 5) Repeated words
    if random.random() < 0.35:
        word = random.choice(["original", "cheap", "urgent", "offer", "sale"])
        listing["description"] += " " + (" ".join([word] * random.randint(5, 12)))
        reasons.append("repeated_words")

    # 6) Very new listing + individual seller
    if random.random() < 0.3:
        listing["posted_days_ago"] = random.randint(0, 1)
        listing["seller_type"] = "individual"
        reasons.append("new_listing_fast_post")

    listing["is_suspicious"] = 1
    listing["suspicious_reason"] = "|".join(sorted(set(reasons)))
    return listing

def generate_dataset(n=2000, suspicious_ratio=0.30, seed=42):
    random.seed(seed)
    Faker.seed(seed)

    data = []
    n_susp = int(n * suspicious_ratio)
    n_norm = n - n_susp

    listing_id = 1000

    # Normal listings
    for _ in range(n_norm):
        data.append(make_normal_listing(listing_id))
        listing_id += 1

    # Suspicious listings
    for _ in range(n_susp):
        base = make_normal_listing(listing_id)
        base = inject_suspicious_signals(base)
        data.append(base)
        listing_id += 1

    df = pd.DataFrame(data).sample(frac=1, random_state=seed).reset_index(drop=True)
    return df

if __name__ == "__main__":
    df = generate_dataset(n=2500, suspicious_ratio=0.30, seed=42)
    df.to_csv("dubizzle_synthetic_listings.csv", index=False)
    print("Saved: dubizzle_synthetic_listings.csv")
    print(df.head(5))
