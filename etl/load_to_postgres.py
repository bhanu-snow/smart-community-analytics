import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import random

# --- DB Connection Config ---
DB_USER = 'postgres'
DB_PASS = '123'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'smart_community'

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# --- Simulate Buildings Data ---
buildings = pd.DataFrame([
    {"name": "Tower A", "location": "Riyadh", "num_floors": 10, "total_units": 40},
    {"name": "Tower B", "location": "Jeddah", "num_floors": 8, "total_units": 32},
    {"name": "Villa Complex", "location": "Dammam", "num_floors": 2, "total_units": 20}
])

buildings.to_sql("buildings", engine, index=False, if_exists="append")

# --- Fetch Building IDs ---
buildings_db = pd.read_sql("SELECT * FROM buildings", engine)

# --- Simulate Units Data ---
unit_rows = []
for _, b in buildings_db.iterrows():
    for i in range(b['total_units']):
        unit_rows.append({
            "building_id": b['building_id'],
            "floor": random.randint(1, b['num_floors']),
            "area_sqft": random.choice([800, 1000, 1200, 1500]),
            "type": random.choice(["residential", "commercial"]),
            "occupancy_status": random.choice([True, False])
        })
units = pd.DataFrame(unit_rows)
units.to_sql("units", engine, index=False, if_exists="append")

# --- Fetch Unit IDs ---
units_db = pd.read_sql("SELECT * FROM units", engine)

# --- Simulate Energy and Water Usage ---
def generate_usage(unit, days=30):
    records = []
    base_date = datetime.now() - timedelta(days=days)
    for i in range(days):
        day = base_date + timedelta(days=i)
        records.append({
            "unit_id": unit["unit_id"],
            "building_id": unit["building_id"],
            "timestamp": day,
            "kWh_used": round(random.uniform(10, 50), 2)
        })
    return records

energy_records = []
for _, unit in units_db.iterrows():
    energy_records.extend(generate_usage(unit))

energy_df = pd.DataFrame(energy_records)
energy_df.to_sql("energy_usage", engine, index=False, if_exists="append")

# --- Water Usage (optional for now) ---
# You can replicate the same structure for water_usage and maintenance_logs

print("Data inserted successfully.")
