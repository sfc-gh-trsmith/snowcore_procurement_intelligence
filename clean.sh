#!/bin/bash
# =============================================================================
# Snowcore Industries Intelligent Sourcing Hub - Clean Script
# =============================================================================
# Complete teardown of all deployed resources
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATABASE="SNOWCORE_PROCUREMENT"
WAREHOUSE="SNOWCORE_PROCUREMENT_WH"
ROLE="ACCOUNTADMIN"
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

# Confirm cleanup
confirm_cleanup() {
    echo ""
    echo "=============================================="
    echo "  WARNING: This will delete all resources!"
    echo "=============================================="
    echo ""
    echo "The following will be permanently deleted:"
    echo "  - Database: ${DATABASE}"
    echo "  - Warehouse: ${WAREHOUSE}"
    echo "  - All schemas: RAW, ATOMIC, PROCUREMENT_MART"
    echo "  - All tables, views, and data"
    echo "  - Cortex Search services"
    echo "  - Streamlit application"
    echo ""
    
    if [ "${1}" != "--force" ] && [ "${1}" != "-f" ]; then
        read -p "Are you sure you want to continue? (yes/no): " CONFIRM
        if [ "${CONFIRM}" != "yes" ]; then
            log_info "Cleanup cancelled"
            exit 0
        fi
    fi
}

# Drop Cortex services
clean_cortex() {
    log_info "Removing Cortex services..."
    
    snow sql -q "
        DROP CORTEX SEARCH SERVICE IF EXISTS ${DATABASE}.ATOMIC.SUPPLIER_COMPLIANCE_SEARCH_SERVICE;
    " --connection "${CONNECTION}" --warehouse "${WAREHOUSE}" --role "${ROLE}" 2>/dev/null || true
    
    log_success "Cortex services removed"
}

# Drop Streamlit app
clean_streamlit() {
    log_info "Removing Streamlit application..."
    
    snow sql -q "
        DROP STREAMLIT IF EXISTS ${DATABASE}.STREAMLIT.PROCUREMENT_INTELLIGENCE_APP;
    " --connection "${CONNECTION}" --warehouse "${WAREHOUSE}" --role "${ROLE}" 2>/dev/null || true
    
    log_success "Streamlit application removed"
}

# Drop warehouse (must be before database per skill deletion order)
clean_warehouse() {
    log_info "Dropping warehouse ${WAREHOUSE}..."
    
    snow sql -q "DROP WAREHOUSE IF EXISTS ${WAREHOUSE};" --connection "${CONNECTION}" --role "${ROLE}" 2>/dev/null || true
    
    log_success "Warehouse dropped"
}

# Drop database (cascades to all objects)
clean_database() {
    log_info "Dropping database ${DATABASE}..."
    
    snow sql -q "DROP DATABASE IF EXISTS ${DATABASE} CASCADE;" --connection "${CONNECTION}" --role "${ROLE}"
    
    log_success "Database dropped"
}

# Clean local generated files
clean_local() {
    log_info "Cleaning local generated files..."
    
    # Remove generated synthetic data (keep directory structure)
    rm -f "${SCRIPT_DIR}/data/synthetic/"*.csv 2>/dev/null || true
    rm -f "${SCRIPT_DIR}/data/synthetic/"*.parquet 2>/dev/null || true
    
    # Remove Python cache
    find "${SCRIPT_DIR}" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "${SCRIPT_DIR}" -type f -name "*.pyc" -delete 2>/dev/null || true
    
    log_success "Local files cleaned"
}

# Main cleanup flow
main() {
    confirm_cleanup "$1"
    
    echo ""
    log_info "Starting cleanup..."
    echo ""
    
    clean_cortex
    clean_streamlit
    clean_warehouse
    clean_database
    clean_local
    
    echo ""
    log_success "Cleanup completed successfully!"
    echo ""
    echo "To redeploy, run: ./deploy.sh"
    echo ""
}

# Run main function
main "$@"
