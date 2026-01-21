-- =============================================================================
-- Snowcore Industries Intelligent Sourcing Hub
-- 03b_atomic_persona_extensions.sql - ATOMIC Layer Persona-Specific Tables
-- Supports CPO, Category Manager, and Data Scientist persona KPIs
-- =============================================================================

USE DATABASE SNOWCORE_PROCUREMENT;
USE SCHEMA ATOMIC;

-- =============================================================================
-- CPO PERSONA TABLES
-- =============================================================================

-- =============================================================================
-- DELIVERY_PERFORMANCE - OTIF (On-Time-In-Full) tracking
-- =============================================================================
CREATE OR REPLACE TABLE DELIVERY_PERFORMANCE (
    DELIVERY_ID NUMBER(38,0) NOT NULL PRIMARY KEY,
    PURCHASE_ORDER_LINE_ID NUMBER(38,0) REFERENCES PURCHASE_ORDER_LINE(PURCHASE_ORDER_LINE_ID),
    SUPPLIER_ID NUMBER(38,0) REFERENCES SUPPLIER(SUPPLIER_ID),
    PROMISED_DATE DATE NOT NULL,
    ACTUAL_DELIVERY_DATE DATE NOT NULL,
    REQUESTED_QUANTITY NUMBER(18,4),
    DELIVERED_QUANTITY NUMBER(18,4),
    ON_TIME_FLAG BOOLEAN,
    IN_FULL_FLAG BOOLEAN,
    OTIF_FLAG BOOLEAN,
    DAYS_EARLY_LATE NUMBER(10,0),
    CREATED_TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

COMMENT ON TABLE DELIVERY_PERFORMANCE IS 'Tracks delivery performance metrics including On-Time-In-Full (OTIF) rates for supplier performance monitoring';

-- =============================================================================
-- PROCUREMENT_OPERATIONAL_METRICS - Monthly operational KPIs
-- =============================================================================
CREATE OR REPLACE TABLE PROCUREMENT_OPERATIONAL_METRICS (
    METRIC_ID NUMBER(38,0) NOT NULL PRIMARY KEY,
    METRIC_DATE DATE NOT NULL,
    TOTAL_PO_COUNT NUMBER(38,0),
    MAVERICK_SPEND_AMOUNT NUMBER(18,2),
    MANAGED_SPEND_AMOUNT NUMBER(18,2),
    PROCUREMENT_OPEX NUMBER(18,2),
    REALIZED_SAVINGS NUMBER(18,2),
    EMERGENCY_PO_COUNT NUMBER(38,0),
    AVG_CYCLE_TIME_DAYS NUMBER(10,2),
    CREATED_TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

COMMENT ON TABLE PROCUREMENT_OPERATIONAL_METRICS IS 'Monthly procurement operational metrics including spend under management, cost per PO, and savings realized';

-- =============================================================================
-- EMISSION_RECORD_SCOPED - Scope 1/2/3 emissions breakdown
-- =============================================================================
CREATE OR REPLACE TABLE EMISSION_RECORD_SCOPED (
    EMISSION_SCOPED_ID NUMBER(38,0) NOT NULL PRIMARY KEY,
    RECORD_DATE DATE NOT NULL,
    SUPPLIER_ID NUMBER(38,0) REFERENCES SUPPLIER(SUPPLIER_ID),
    SCOPE_TYPE TEXT(20) NOT NULL,  -- SCOPE_1, SCOPE_2, SCOPE_3
    EMISSION_QUANTITY_MT NUMBER(18,4),
    EMISSION_SOURCE TEXT(100),
    CREATED_TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

COMMENT ON TABLE EMISSION_RECORD_SCOPED IS 'Carbon emissions by GHG Protocol scope (Scope 1: direct, Scope 2: indirect energy, Scope 3: supply chain)';

-- =============================================================================
-- SUPPLIER_DIVERSITY - Diversity classification and certification
-- =============================================================================
CREATE OR REPLACE TABLE SUPPLIER_DIVERSITY (
    SUPPLIER_DIVERSITY_ID NUMBER(38,0) NOT NULL PRIMARY KEY,
    SUPPLIER_ID NUMBER(38,0) REFERENCES SUPPLIER(SUPPLIER_ID),
    IS_MINORITY_OWNED BOOLEAN DEFAULT FALSE,
    IS_WOMEN_OWNED BOOLEAN DEFAULT FALSE,
    IS_VETERAN_OWNED BOOLEAN DEFAULT FALSE,
    IS_SMALL_BUSINESS BOOLEAN DEFAULT FALSE,
    DIVERSITY_CERTIFICATION TEXT(200),
    CERTIFICATION_DATE DATE,
    CERTIFICATION_EXPIRY DATE,
    CREATED_TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

COMMENT ON TABLE SUPPLIER_DIVERSITY IS 'Supplier diversity classifications for ESG and diversity spend tracking';

-- =============================================================================
-- CATEGORY MANAGER PERSONA TABLES
-- =============================================================================

-- =============================================================================
-- SUPPLIER_SCORECARD - Multi-dimensional supplier evaluation
-- =============================================================================
CREATE OR REPLACE TABLE SUPPLIER_SCORECARD (
    SCORECARD_ID NUMBER(38,0) NOT NULL PRIMARY KEY,
    SUPPLIER_ID NUMBER(38,0) REFERENCES SUPPLIER(SUPPLIER_ID),
    EVALUATION_DATE DATE NOT NULL,
    QUALITY_SCORE NUMBER(5,2),
    DELIVERY_SCORE NUMBER(5,2),
    PRICE_SCORE NUMBER(5,2),
    RESPONSIVENESS_SCORE NUMBER(5,2),
    OVERALL_SCORE NUMBER(5,2),
    LEAD_TIME_VARIANCE_DAYS NUMBER(10,2),
    INVOICE_ACCURACY_PCT NUMBER(5,2),
    EVALUATION_PERIOD TEXT(20),
    EVALUATOR_NOTES TEXT(2000),
    CREATED_TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

COMMENT ON TABLE SUPPLIER_SCORECARD IS 'Comprehensive supplier scorecard with quality, delivery, price, and responsiveness dimensions';

-- =============================================================================
-- FORWARD_CONTRACT - Forward contract coverage for hedging
-- =============================================================================
CREATE OR REPLACE TABLE FORWARD_CONTRACT (
    CONTRACT_ID NUMBER(38,0) NOT NULL PRIMARY KEY,
    SUPPLIER_ID NUMBER(38,0) REFERENCES SUPPLIER(SUPPLIER_ID),
    MATERIAL_CATEGORY TEXT(100),
    CONTRACT_START_DATE DATE NOT NULL,
    CONTRACT_END_DATE DATE NOT NULL,
    CONTRACTED_QUANTITY NUMBER(18,4),
    CONTRACTED_PRICE NUMBER(18,4),
    PRICE_UNIT TEXT(50),
    UTILIZATION_PCT NUMBER(5,4),
    CONTRACT_STATUS TEXT(20) DEFAULT 'ACTIVE',
    CREATED_TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

COMMENT ON TABLE FORWARD_CONTRACT IS 'Forward contracts for commodity hedging and price risk management';

-- =============================================================================
-- DATA SCIENTIST PERSONA TABLES
-- =============================================================================

-- =============================================================================
-- MARKETPLACE_INDICATORS - External macro-economic indicators
-- =============================================================================
CREATE OR REPLACE TABLE MARKETPLACE_INDICATORS (
    INDICATOR_ID NUMBER(38,0) NOT NULL PRIMARY KEY,
    INDICATOR_DATE DATE NOT NULL,
    INDICATOR_NAME TEXT(100) NOT NULL,
    INDICATOR_VALUE NUMBER(18,4),
    PERCENTAGE_CHANGE NUMBER(8,4),
    INDICATOR_TYPE TEXT(50),  -- ECONOMIC, INDUSTRY, COMMODITY
    DATA_SOURCE TEXT(100),
    CREATED_TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

COMMENT ON TABLE MARKETPLACE_INDICATORS IS 'External macro-economic indicators for demand sensing ML models (construction starts, clinical trial spend, PMI, etc.)';

-- =============================================================================
-- MODEL_REGISTRY - ML model tracking and versioning
-- =============================================================================
CREATE OR REPLACE TABLE MODEL_REGISTRY (
    MODEL_ID NUMBER(38,0) NOT NULL PRIMARY KEY,
    MODEL_NAME TEXT(100) NOT NULL,
    MODEL_VERSION TEXT(50) NOT NULL,
    ALGORITHM TEXT(50),
    TRAINING_DATE TIMESTAMP_NTZ,
    MAE NUMBER(18,4),
    RMSE NUMBER(18,4),
    MAPE NUMBER(8,4),
    R2_SCORE NUMBER(8,6),
    FEATURE_COUNT NUMBER(10,0),
    TRAINING_SAMPLES NUMBER(38,0),
    IS_DEPLOYED BOOLEAN DEFAULT FALSE,
    DEPLOYMENT_DATE TIMESTAMP_NTZ,
    MODEL_ARTIFACT_PATH TEXT(500),
    TRAINING_PARAMETERS VARIANT,
    CREATED_TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

COMMENT ON TABLE MODEL_REGISTRY IS 'ML model registry for tracking model versions, performance metrics, and deployment status';

-- =============================================================================
-- BUSINESS_IMPACT_METRICS - Track ML model business impact
-- =============================================================================
CREATE OR REPLACE TABLE BUSINESS_IMPACT_METRICS (
    IMPACT_ID NUMBER(38,0) NOT NULL PRIMARY KEY AUTOINCREMENT,
    METRIC_DATE DATE NOT NULL,
    MODEL_ID NUMBER(38,0) REFERENCES MODEL_REGISTRY(MODEL_ID),
    INVENTORY_REDUCTION_AMOUNT NUMBER(18,2),
    COST_SAVINGS_AMOUNT NUMBER(18,2),
    SERVICE_LEVEL_IMPROVEMENT_PCT NUMBER(5,2),
    STOCKOUT_REDUCTION_PCT NUMBER(5,2),
    FORECAST_VALUE_ADDED NUMBER(18,2),
    NOTES TEXT(1000),
    CREATED_TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

COMMENT ON TABLE BUSINESS_IMPACT_METRICS IS 'Business impact metrics from ML model predictions including inventory reduction and cost savings';

-- Success message
SELECT 'ATOMIC persona extension tables created successfully' AS status;
