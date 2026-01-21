#!/bin/bash
# =============================================================================
# Snowcore Industries Intelligent Sourcing Hub - Run Script
# =============================================================================
# Runtime operations: main (run ML model), test (validate), status (check health)
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATABASE="SNOWCORE_PROCUREMENT"
WAREHOUSE="SNOWCORE_PROCUREMENT_WH"
CONNECTION="demo"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Run test suite
run_tests() {
    log_info "Running test suite..."
    echo ""
    
    # Test 1: Verify database exists
    log_info "Test 1: Verifying database exists..."
    RESULT=$(snow sql -q "SELECT COUNT(*) FROM ${DATABASE}.INFORMATION_SCHEMA.TABLES" --connection "${CONNECTION}" --warehouse "${WAREHOUSE}" 2>/dev/null || echo "FAILED")
    if [[ "$RESULT" == *"FAILED"* ]]; then
        log_error "Database verification failed"
        exit 1
    fi
    log_success "Database exists"
    
    # Test 2: Verify ATOMIC tables
    log_info "Test 2: Verifying ATOMIC layer tables..."
    snow sql -q "SELECT 'SUPPLIER' as table_name, COUNT(*) as row_count FROM ${DATABASE}.ATOMIC.SUPPLIER UNION ALL SELECT 'PRODUCT', COUNT(*) FROM ${DATABASE}.ATOMIC.PRODUCT UNION ALL SELECT 'PURCHASE_ORDER', COUNT(*) FROM ${DATABASE}.ATOMIC.PURCHASE_ORDER" --connection "${CONNECTION}" --warehouse "${WAREHOUSE}"
    log_success "ATOMIC layer verified"
    
    # Test 3: Verify MART views
    log_info "Test 3: Verifying PROCUREMENT_MART views..."
    snow sql -q "SELECT 'V_SPEND_SUMMARY' as view_name, COUNT(*) as row_count FROM ${DATABASE}.PROCUREMENT_MART.V_SPEND_SUMMARY UNION ALL SELECT 'V_SUPPLIER_RISK', COUNT(*) FROM ${DATABASE}.PROCUREMENT_MART.V_SUPPLIER_RISK" --connection "${CONNECTION}" --warehouse "${WAREHOUSE}"
    log_success "MART layer verified"
    
    # Test 4: Golden Query - Top 5 EMEA suppliers with financial health < 50
    log_info "Test 4: Running golden query (Top 5 EMEA risky suppliers)..."
    snow sql -q "
        SELECT 
            s.SUPPLIER_CODE,
            p.PARTY_NAME AS supplier_name,
            SUM(po.TOTAL_PURCHASE_ORDER_VALUE) AS total_spend,
            msr.FINANCIAL_HEALTH_SCORE
        FROM ${DATABASE}.ATOMIC.SUPPLIER s
        JOIN ${DATABASE}.ATOMIC.PARTY p ON s.PARTY_ID = p.PARTY_ID
        JOIN ${DATABASE}.ATOMIC.PURCHASE_ORDER po ON s.SUPPLIER_ID = po.SUPPLIER_ID
        JOIN ${DATABASE}.ATOMIC.MARKETPLACE_SUPPLIER_RISK msr ON s.SUPPLIER_ID = msr.SUPPLIER_ID
        JOIN ${DATABASE}.ATOMIC.PARTY_ADDRESS pa ON p.PARTY_ID = pa.PARTY_ID
        JOIN ${DATABASE}.ATOMIC.GEOGRAPHY g ON pa.GEOGRAPHY_ID = g.GEOGRAPHY_ID
        WHERE g.GEOGRAPHY_NAME = 'EMEA'
        AND msr.FINANCIAL_HEALTH_SCORE < 50
        AND msr.IS_CURRENT_FLAG = TRUE
        GROUP BY s.SUPPLIER_CODE, p.PARTY_NAME, msr.FINANCIAL_HEALTH_SCORE
        ORDER BY total_spend DESC
        LIMIT 5
    " --connection "${CONNECTION}" --warehouse "${WAREHOUSE}"
    log_success "Golden query executed successfully"
    
    echo ""
    log_success "All tests passed!"
    echo ""
}

# Check deployment status
check_status() {
    log_info "Checking deployment status..."
    echo ""
    
    # Check database
    echo "=== Database Status ==="
    snow sql -q "SELECT CURRENT_DATABASE(), CURRENT_WAREHOUSE(), CURRENT_ROLE()" --connection "${CONNECTION}" --warehouse "${WAREHOUSE}"
    
    # Check table counts
    echo ""
    echo "=== Table Row Counts ==="
    snow sql -q "
        SELECT 'ATOMIC.SUPPLIER' as table_name, COUNT(*) as rows FROM ${DATABASE}.ATOMIC.SUPPLIER
        UNION ALL SELECT 'ATOMIC.PRODUCT', COUNT(*) FROM ${DATABASE}.ATOMIC.PRODUCT
        UNION ALL SELECT 'ATOMIC.PURCHASE_ORDER', COUNT(*) FROM ${DATABASE}.ATOMIC.PURCHASE_ORDER
        UNION ALL SELECT 'ATOMIC.PURCHASE_ORDER_LINE', COUNT(*) FROM ${DATABASE}.ATOMIC.PURCHASE_ORDER_LINE
        UNION ALL SELECT 'ATOMIC.MARKETPLACE_SUPPLIER_RISK', COUNT(*) FROM ${DATABASE}.ATOMIC.MARKETPLACE_SUPPLIER_RISK
        UNION ALL SELECT 'ATOMIC.MARKETPLACE_COMMODITY_INDEX', COUNT(*) FROM ${DATABASE}.ATOMIC.MARKETPLACE_COMMODITY_INDEX
    " --connection "${CONNECTION}" --warehouse "${WAREHOUSE}"
    
    echo ""
    log_success "Status check complete"
}

# Run demand sensing notebook to generate forecasts
run_main() {
    log_info "Running demand sensing model..."
    echo ""
    
    snow notebook execute "${DATABASE}.NOTEBOOKS.DEMAND_SENSING" \
        --connection "${CONNECTION}" \
        --warehouse "${WAREHOUSE}"
    
    log_success "Demand forecasts generated successfully"
    echo ""
    echo "Forecasts written to: ${DATABASE}.PROCUREMENT_MART.DEMAND_FORECAST_PREDICTIONS"
    echo ""
}

# Get Streamlit app URL
get_streamlit_url() {
    log_info "Getting Streamlit app URL..."
    echo ""
    
    STREAMLIT_APP="${DATABASE}.STREAMLIT.PROCUREMENT_INTELLIGENCE_APP"
    
    # Get the account URL and construct the Streamlit link
    ACCOUNT_URL=$(snow sql -q "SELECT CURRENT_ORGANIZATION_NAME() || '-' || CURRENT_ACCOUNT_NAME() AS account_locator" \
        --connection "${CONNECTION}" \
        --warehouse "${WAREHOUSE}" \
        --format JSON 2>/dev/null | python3 -c "import sys,json; data=json.load(sys.stdin); print(data[0]['ACCOUNT_LOCATOR'])" 2>/dev/null)
    
    if [[ -z "$ACCOUNT_URL" ]]; then
        log_error "Could not retrieve account information"
        exit 1
    fi
    
    # Convert to lowercase for URL
    ACCOUNT_URL_LOWER=$(echo "$ACCOUNT_URL" | tr '[:upper:]' '[:lower:]')
    
    echo ""
    log_success "Streamlit App URL:"
    echo ""
    echo "  https://app.snowflake.com/${ACCOUNT_URL_LOWER}/#/streamlit-apps/${STREAMLIT_APP}"
    echo ""
    
    # Also show app status
    log_info "App Status:"
    snow sql -q "SHOW STREAMLITS LIKE 'PROCUREMENT_INTELLIGENCE_APP' IN SCHEMA ${DATABASE}.STREAMLIT" \
        --connection "${CONNECTION}" \
        --warehouse "${WAREHOUSE}" 2>/dev/null || log_warn "Could not retrieve app status"
    echo ""
}

# Show usage
show_usage() {
    echo "Usage: ./run.sh [command]"
    echo ""
    echo "Commands:"
    echo "  main       Run demand sensing model to generate forecasts"
    echo "  test       Run validation tests"
    echo "  status     Check deployment status"
    echo "  streamlit  Get Streamlit app URL"
    echo "  help       Show this help message"
    echo ""
}

# Main entry point
case "${1:-help}" in
    main)
        run_main
        ;;
    test)
        run_tests
        ;;
    status)
        check_status
        ;;
    streamlit)
        get_streamlit_url
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        log_error "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac
