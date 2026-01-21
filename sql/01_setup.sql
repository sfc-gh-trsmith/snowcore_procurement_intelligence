-- =============================================================================
-- Snowcore Industries Intelligent Sourcing Hub
-- 01_setup.sql - Database and Schema Setup
-- =============================================================================

-- Create database
CREATE DATABASE IF NOT EXISTS SNOWCORE_PROCUREMENT
    COMMENT = 'Snowcore Industries Intelligent Sourcing Hub - Procurement Intelligence Demo';

USE DATABASE SNOWCORE_PROCUREMENT;

-- Create project warehouse
CREATE WAREHOUSE IF NOT EXISTS SNOWCORE_PROCUREMENT_WH
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 1800
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Snowcore Procurement Intelligence - Query warehouse';

-- Create schemas for three-layer architecture
CREATE SCHEMA IF NOT EXISTS RAW
    COMMENT = 'Landing zone for ERP dumps and Marketplace feeds';

CREATE SCHEMA IF NOT EXISTS ATOMIC
    COMMENT = 'Normalized enterprise data model - conforms to EDM data dictionary';

CREATE SCHEMA IF NOT EXISTS PROCUREMENT_MART
    COMMENT = 'Aggregated views for Streamlit consumption and analytics';

CREATE SCHEMA IF NOT EXISTS STREAMLIT
    COMMENT = 'Streamlit application objects';

CREATE SCHEMA IF NOT EXISTS NOTEBOOKS
    COMMENT = 'Snowflake notebooks for ML and analytics';

-- Create internal stage for notebook files
CREATE OR REPLACE STAGE NOTEBOOKS.NOTEBOOK_STAGE
    COMMENT = 'Stage for notebook files';

-- Create file formats for data loading
CREATE OR REPLACE FILE FORMAT RAW.CSV_FORMAT
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('NULL', 'null', '')
    EMPTY_FIELD_AS_NULL = TRUE
    COMPRESSION = AUTO;

-- Create internal stage for data loading
CREATE OR REPLACE STAGE RAW.DATA_STAGE
    FILE_FORMAT = RAW.CSV_FORMAT
    COMMENT = 'Internal stage for loading synthetic demo data';

-- Grant appropriate permissions
GRANT USAGE ON DATABASE SNOWCORE_PROCUREMENT TO ROLE PUBLIC;
GRANT USAGE ON ALL SCHEMAS IN DATABASE SNOWCORE_PROCUREMENT TO ROLE PUBLIC;
GRANT USAGE ON WAREHOUSE SNOWCORE_PROCUREMENT_WH TO ROLE PUBLIC;
GRANT SELECT ON ALL TABLES IN DATABASE SNOWCORE_PROCUREMENT TO ROLE PUBLIC;
GRANT SELECT ON FUTURE TABLES IN DATABASE SNOWCORE_PROCUREMENT TO ROLE PUBLIC;
GRANT SELECT ON ALL VIEWS IN DATABASE SNOWCORE_PROCUREMENT TO ROLE PUBLIC;
GRANT SELECT ON FUTURE VIEWS IN DATABASE SNOWCORE_PROCUREMENT TO ROLE PUBLIC;

-- Success message
SELECT 'Setup completed successfully' AS status;
