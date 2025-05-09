import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import random

# --- DB Connection ---
DB_USER = 'postgres'
DB_PASS = '123'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'smart_community'

engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# --- Delete Data from Tables (But Keep Structure) ---
# with engine.connect() as conn:
#     conn.execute("DELETE FROM maintenance_logs;")
#     conn.execute("DELETE FROM energy_usage;")
#     conn.execute("DELETE FROM water_usage;")
#     conn.execute("DELETE FROM units;")
#     conn.execute("DELETE FROM buildings;")

# print("✅ Existing data deleted from tables.")

# --- 1. Simulate Buildings ---
buildings = pd.DataFrame([
    {"name": "Tower A", "location": "Riyadh", "num_floors": 10, "total_units": 40},
    {"name": "Tower B", "location": "Jeddah", "num_floors": 8, "total_units": 32},
    {"name": "Villa Complex", "location": "Dammam", "num_floors": 2, "total_units": 20}
])
buildings.to_sql("buildings", engine, index=False, if_exists="append")

# --- 2. Load Units ---
buildings_db = pd.read_sql("SELECT * FROM buildings", engine)
unit_rows = []
for _, b in buildings_db.iterrows():
    for _ in range(b['total_units']):
        unit_rows.append({
            "building_id": b['building_id'],
            "floor": random.randint(1, b['num_floors']),
            "area_sqft": random.choice([800, 1000, 1200, 1500]),
            "type": random.choice(["residential", "commercial"]),
            "occupancy_status": random.choice([True, False])
        })
units = pd.DataFrame(unit_rows)
units.to_sql("units", engine, index=False, if_exists="append")

# --- 3. Load Energy Usage ---
units_db = pd.read_sql("SELECT unit_id, building_id FROM units", engine)
energy_rows = []
for _, unit in units_db.iterrows():
    base_date = datetime.now() - timedelta(days=30)
    for i in range(30):
        energy_rows.append({
            "unit_id": unit.unit_id,
            "building_id": unit.building_id,
            "timestamp": base_date + timedelta(days=i),
            "kwh_used": round(random.uniform(10, 50), 2)
        })
energy_df = pd.DataFrame(energy_rows)
energy_df.to_sql("energy_usage", engine, index=False, if_exists="append")

# --- 4. Load Water Usage ---
water_rows = []
for _, unit in units_db.iterrows():
    base_date = datetime.now() - timedelta(days=30)
    for i in range(30):
        water_rows.append({
            "unit_id": unit.unit_id,
            "building_id": unit.building_id,
            "timestamp": base_date + timedelta(days=i),
            "liters_used": round(random.uniform(100, 500), 2)
        })
water_df = pd.DataFrame(water_rows)
water_df.to_sql("water_usage", engine, index=False, if_exists="append")

# --- 5. Load Maintenance Logs ---
maintenance_rows = []
issues = ["AC Fault", "Water Leak", "Elevator Issue", "Lighting", "Internet"]
for _, unit in units_db.iterrows():
    for _ in range(random.randint(1, 3)):
        maintenance_rows.append({
            "unit_id": unit.unit_id,
            "building_id": unit.building_id,
            "timestamp": datetime.now() - timedelta(days=random.randint(0, 60)),
            "issue_type": random.choice(issues),
            "priority": random.randint(1, 5),
            "status": random.choice(["Open", "Closed", "In Progress"])
        })
maint_df = pd.DataFrame(maintenance_rows)
maint_df.to_sql("maintenance_logs", engine, index=False, if_exists="append")

print("✅ All data loaded: buildings, units, energy, water, maintenance.")
