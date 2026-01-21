-- =============================================================================
-- Snowcore Industries Intelligent Sourcing Hub
-- 06_cortex_services.sql - Cortex Search Service for RAG
-- =============================================================================

USE DATABASE SNOWCORE_PROCUREMENT;
USE SCHEMA ATOMIC;

-- =============================================================================
-- CORTEX SEARCH SERVICE - Supplier Compliance Document Search
-- =============================================================================
-- This creates a search service over supplier documents for RAG queries
-- about contracts, audits, and regulatory compliance

CREATE OR REPLACE CORTEX SEARCH SERVICE SUPPLIER_COMPLIANCE_SEARCH_SERVICE
ON DOCUMENT_CONTENT
ATTRIBUTES SUPPLIER_ID, DOCUMENT_TYPE, DOCUMENT_TITLE, DOCUMENT_STATUS
WAREHOUSE = COMPUTE_WH
TARGET_LAG = '1 hour'
AS (
    SELECT 
        DOCUMENT_ID,
        SUPPLIER_ID,
        DOCUMENT_TYPE,
        DOCUMENT_TITLE,
        DOCUMENT_CONTENT,
        DOCUMENT_SUMMARY,
        EFFECTIVE_DATE,
        EXPIRATION_DATE,
        DOCUMENT_STATUS
    FROM ATOMIC.SUPPLIER_DOCUMENT
    WHERE DOCUMENT_STATUS = 'ACTIVE'
);

-- Success message
SELECT 'Cortex Search service created successfully' AS status;
