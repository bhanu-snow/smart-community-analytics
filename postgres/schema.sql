-- postgres/schema.sql

CREATE TABLE buildings (
    building_id SERIAL PRIMARY KEY,
    name VARCHAR,
    location VARCHAR,
    num_floors INT,
    total_units INT
);

CREATE TABLE units (
    unit_id SERIAL PRIMARY KEY,
    building_id INT REFERENCES buildings(building_id),
    floor INT,
    area_sqft FLOAT,
    type VARCHAR,
    occupancy_status BOOLEAN
);

CREATE TABLE energy_usage (
    id SERIAL PRIMARY KEY,
    unit_id INT REFERENCES units(unit_id),
    building_id INT REFERENCES buildings(building_id),
    timestamp TIMESTAMP,
    kWh_used FLOAT
);

CREATE TABLE water_usage (
    id SERIAL PRIMARY KEY,
    unit_id INT REFERENCES units(unit_id),
    building_id INT REFERENCES buildings(building_id),
    timestamp TIMESTAMP,
    liters_used FLOAT
);

CREATE TABLE maintenance_logs (
    id SERIAL PRIMARY KEY,
    unit_id INT REFERENCES units(unit_id),
    building_id INT REFERENCES buildings(building_id),
    timestamp TIMESTAMP,
    issue_type VARCHAR,
    priority INT,
    status VARCHAR
);
