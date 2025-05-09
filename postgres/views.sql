-- View: Building Summary (units, occupancy, avg area)
CREATE OR REPLACE VIEW vw_building_summary AS
SELECT
    b.building_id,
    b.name AS building_name,
    b.location,
    COUNT(u.unit_id) AS total_units,
    COUNT(CASE WHEN u.occupancy_status THEN 1 END) AS occupied_units,
    ROUND(AVG(u.area_sqft)::NUMERIC, 2) AS avg_unit_area_sqft,
    ROUND(
        COUNT(CASE WHEN u.occupancy_status THEN 1 END)::DECIMAL / COUNT(u.unit_id) * 100,
        2
    ) AS occupancy_rate_pct
FROM buildings b
LEFT JOIN units u ON u.building_id = b.building_id
GROUP BY b.building_id;

-- View: Unit Occupancy by Type
CREATE OR REPLACE VIEW vw_unit_occupancy AS
SELECT
    b.name AS building_name,
    u.type AS unit_type,
    COUNT(*) AS total_units,
    COUNT(CASE WHEN u.occupancy_status THEN 1 END) AS occupied,
    ROUND(
        COUNT(CASE WHEN u.occupancy_status THEN 1 END)::DECIMAL / COUNT(*) * 100,
        2
    ) AS occupancy_pct
FROM units u
JOIN buildings b ON u.building_id = b.building_id
GROUP BY b.name, u.type;

-- View: Daily Energy Usage per Building
CREATE OR REPLACE VIEW vw_energy_daily AS
SELECT
    e.building_id,
    b.name AS building_name,
    DATE(e.timestamp) AS usage_date,
    ROUND(SUM(e.kWh_used)::NUMERIC, 2) AS total_kWh
FROM energy_usage e
JOIN buildings b ON b.building_id = e.building_id
GROUP BY e.building_id, b.name, DATE(e.timestamp)
ORDER BY usage_date;

-- View: Monthly Energy Usage
CREATE OR REPLACE VIEW vw_energy_monthly AS
SELECT
    e.building_id,
    b.name AS building_name,
    DATE_TRUNC('month', e.timestamp) AS month,
    ROUND(SUM(e.kWh_used)::NUMERIC, 2) AS total_kWh
FROM energy_usage e
JOIN buildings b ON b.building_id = e.building_id
GROUP BY e.building_id, b.name, DATE_TRUNC('month', e.timestamp)
ORDER BY month;

-- View: Forecast-Ready Daily kWh per Building
CREATE OR REPLACE VIEW vw_forecast_ready_energy AS
SELECT
    e.building_id,
    b.name AS building_name,
    DATE(e.timestamp) AS ds,
    ROUND(SUM(e.kWh_used)::NUMERIC, 2) AS y
FROM energy_usage e
JOIN buildings b ON b.building_id = e.building_id
GROUP BY e.building_id, b.name, DATE(e.timestamp)
ORDER BY ds;

-- View: Maintenance Summary (stub – extend if you add maintenance_logs table)
-- Ensure the maintenance_logs table has data before using this view
CREATE OR REPLACE VIEW vw_maintenance_summary AS
SELECT
    m.building_id,
    b.name AS building_name,
    m.status,
    m.priority,
    COUNT(*) AS ticket_count
FROM maintenance_logs m
JOIN buildings b ON b.building_id = m.building_id
GROUP BY m.building_id, b.name, m.status, m.priority
ORDER BY ticket_count DESC;
