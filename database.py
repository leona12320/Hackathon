import sqlite3

DB = 'zero_hunger.db'

def init_db():
    """Initialize database with all tables"""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    
    # Pledges table
    c.execute('''CREATE TABLE IF NOT EXISTS pledges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        pledge_text TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'active'
    )''')
    
    # Donations table
    c.execute('''CREATE TABLE IF NOT EXISTS donations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_name TEXT,
        donor_email TEXT UNIQUE,
        donation_type TEXT,
        amount TEXT,
        payment_status TEXT DEFAULT 'completed',
        stripe_payment_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # NGOs table
    c.execute('''CREATE TABLE IF NOT EXISTS ngos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        location TEXT,
        contact_email TEXT,
        phone TEXT,
        website TEXT,
        image_url TEXT,
        verification_status TEXT DEFAULT 'verified',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Food Banks table
    c.execute('''CREATE TABLE IF NOT EXISTS food_banks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        location TEXT,
        contact_email TEXT,
        phone TEXT,
        accepted_items TEXT,
        operating_hours TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Community Kitchens table
    c.execute('''CREATE TABLE IF NOT EXISTS community_kitchens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        location TEXT,
        meals_per_day INTEGER,
        contact_email TEXT,
        phone TEXT,
        operating_hours TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Insert sample data
    sample_ngos = [
        ("Feeding India", "Collects surplus food from restaurants and distributes to communities in need.", "PAN India", "info@feedingindia.org", "1234567890", "https://feedingindia.org"),
        ("Akshaya Patra Foundation", "Provides mid-day meals to children and supports community nutrition programs.", "Multiple states", "contact@akshayapatra.org", "9876543210", "https://akshayapatra.org"),
        ("Goonj", "Works on food security and disaster relief, ensuring essential supplies reach rural areas.", "India-wide", "hello@goonj.org", "5555555555", "https://goonj.org")
    ]
    
    sample_banks = [
        ("India FoodBanking Network", "Supports hunger relief by connecting donors with food distribution partners.", "Delhi NCR, Mumbai, Bengaluru", "info@indiafoodbanking.org", "1111111111", "dry rations, packaged food, fresh produce"),
        ("Delhi Food Bank", "Collects dry rations and distributes them across low-income communities.", "New Delhi", "contact@delhifoodbank.org", "2222222222", "dry rations, grains, pulses")
    ]
    
    sample_kitchens = [
        ("Indira Canteen", "Affordable meals supporting low-income communities and daily wage workers.", "Bengaluru", 500, "indira@canteen.org", "9988776655", "6 AM - 9 PM"),
        ("Amma Canteen", "Subsidized nutritious meals for the public, students, and labourers.", "Chennai", 300, "amma@canteen.org", "8877665544", "7 AM - 8 PM")
    ]
    
    try:
        for ngo in sample_ngos:
            c.execute("INSERT INTO ngos (name, description, location, contact_email, phone, website) VALUES (?, ?, ?, ?, ?, ?)", ngo)
        
        for bank in sample_banks:
            c.execute("INSERT INTO food_banks (name, description, location, contact_email, phone, accepted_items) VALUES (?, ?, ?, ?, ?, ?)", bank)
        
        for kitchen in sample_kitchens:
            c.execute("INSERT INTO community_kitchens (name, description, location, meals_per_day, contact_email, phone, operating_hours) VALUES (?, ?, ?, ?, ?, ?, ?)", kitchen)
        
        conn.commit()
        print("✓ Database initialized successfully with sample data")
    except sqlite3.IntegrityError:
        print("✓ Database tables already exist (no duplicates added)")
    
    conn.close()

def get_db():
    """Get database connection with Row factory"""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def close_db(conn):
    """Close database connection"""
    if conn:
        conn.close()
