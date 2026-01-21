#!/bin/bash
# =============================================================================
# Snowcore Industries Intelligent Sourcing Hub - Deploy Script
# =============================================================================
# Deploys infrastructure, schema, and loads synthetic data to Snowflake
#
# Usage:
#   ./deploy.sh                    # Full deployment (all components)
#   ./deploy.sh --only-streamlit   # Deploy only Streamlit app
#   ./deploy.sh --only-notebook    # Deploy only notebook
#   ./deploy.sh --only-cortex      # Deploy only Cortex services
#   ./deploy.sh --only-data        # Generate and load data only
#   ./deploy.sh --only-infrastructure  # Deploy DDL/schemas only
#   ./deploy.sh --only-streamlit --only-notebook  # Combine multiple flags
# =============================================================================

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATABASE="SNOWCORE_PROCUREMENT"
WAREHOUSE="SNOWCORE_PROCUREMENT_WH"
ROLE="ACCOUNTADMIN"
CONNECTION="demo"

# Deployment flags (default: deploy everything)
DEPLOY_ALL=true
DEPLOY_INFRASTRUCTURE=false
DEPLOY_DATA=false
DEPLOY_CORTEX=false
DEPLOY_STREAMLIT=false
DEPLOY_NOTEBOOK=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Show usage
show_usage() {
    echo "Usage: ./deploy.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --only-infrastructure  Deploy database, schemas, and tables only"
    echo "  --only-data            Generate and load synthetic data only"
    echo "  --only-cortex          Deploy Cortex Search services only"
    echo "  --only-streamlit       Deploy Streamlit application only"
    echo "  --only-notebook        Deploy notebook only"
    echo "  --help, -h             Show this help message"
    echo ""
    echo "Multiple flags can be combined:"
    echo "  ./deploy.sh --only-streamlit --only-notebook"
    echo ""
    echo "Without any flags, a full deployment is performed."
    echo ""
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --only-infrastructure)
                DEPLOY_ALL=false
                DEPLOY_INFRASTRUCTURE=true
                shift
                ;;
            --only-data)
                DEPLOY_ALL=false
                DEPLOY_DATA=true
                shift
                ;;
            --only-cortex)
                DEPLOY_ALL=false
                DEPLOY_CORTEX=true
                shift
                ;;
            --only-streamlit)
                DEPLOY_ALL=false
                DEPLOY_STREAMLIT=true
                shift
                ;;
            --only-notebook)
                DEPLOY_ALL=false
                DEPLOY_NOTEBOOK=true
                shift
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v snow &> /dev/null; then
        log_error "Snowflake CLI (snow) not found. Please install it first."
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Deploy database and schemas
deploy_infrastructure() {
    log_info "Deploying database infrastructure..."
    
    snow sql -f "${SCRIPT_DIR}/sql/01_setup.sql" --connection "${CONNECTION}" --warehouse "${WAREHOUSE}" --role "${ROLE}"
    
    log_success "Infrastructure deployed"
}

# Deploy ATOMIC layer tables
deploy_atomic_layer() {
    log_info "Deploying ATOMIC layer tables..."
    
    snow sql -f "${SCRIPT_DIR}/sql/02_atomic_reference.sql" --connection "${CONNECTION}" --warehouse "${WAREHOUSE}" --role "${ROLE}"
    snow sql -f "${SCRIPT_DIR}/sql/03_atomic_procurement.sql" --connection "${CONNECTION}" --warehouse "${WAREHOUSE}" --role "${ROLE}"
    snow sql -f "${SCRIPT_DIR}/sql/03b_atomic_persona_extensions.sql" --connection "${CONNECTION}" --warehouse "${WAREHOUSE}" --role "${ROLE}"
    
    log_success "ATOMIC layer deployed"
}

# Deploy RAW layer tables
deploy_raw_layer() {
    log_info "Deploying RAW layer tables..."
    
    snow sql -f "${SCRIPT_DIR}/sql/04_raw_layer.sql" --connection "${CONNECTION}" --warehouse "${WAREHOUSE}" --role "${ROLE}"
    
    log_success "RAW layer deployed"
}

# Deploy MART layer views
deploy_mart_layer() {
    log_info "Deploying PROCUREMENT_MART layer..."
    
    snow sql -f "${SCRIPT_DIR}/sql/05_mart_layer.sql" --connection "${CONNECTION}" --warehouse "${WAREHOUSE}" --role "${ROLE}"
    snow sql -f "${SCRIPT_DIR}/sql/05b_mart_persona_extensions.sql" --connection "${CONNECTION}" --warehouse "${WAREHOUSE}" --role "${ROLE}"
    
    log_success "MART layer deployed"
}

# Deploy Cortex services
deploy_cortex() {
    log_info "Deploying Cortex services..."
    
    snow sql -f "${SCRIPT_DIR}/sql/06_cortex_services.sql" --connection "${CONNECTION}" --warehouse "${WAREHOUSE}" --role "${ROLE}"
    
    log_success "Cortex services deployed"
}

# Load synthetic data
load_data() {
    log_info "Loading synthetic data..."
    
    # Generate synthetic data if not exists
    if [ ! -f "${SCRIPT_DIR}/data/synthetic/supplier.csv" ]; then
        log_info "Generating synthetic data..."
        cd "${SCRIPT_DIR}"
        python3 utils/generate_synthetic_data.py
    fi
    
    # Upload files to stage
    log_info "Uploading data files to stage..."
    for csv_file in "${SCRIPT_DIR}/data/synthetic/"*.csv; do
        if [ -f "$csv_file" ]; then
            filename=$(basename "$csv_file")
            log_info "  Uploading ${filename}..."
            snow stage copy "${csv_file}" "@${DATABASE}.RAW.DATA_STAGE" --overwrite --connection "${CONNECTION}" --warehouse "${WAREHOUSE}" --role "${ROLE}" 2>/dev/null || true
        fi
    done
    
    # Run data load SQL
    snow sql -f "${SCRIPT_DIR}/sql/07_load_data.sql" --connection "${CONNECTION}" --warehouse "${WAREHOUSE}" --role "${ROLE}"
    
    log_success "Synthetic data loaded"
}

# Deploy Streamlit app to Snowflake
deploy_streamlit() {
    log_info "Deploying Streamlit app to Snowflake..."
    
    cd "${SCRIPT_DIR}/streamlit"
    snow streamlit deploy --replace --connection "${CONNECTION}" --database "${DATABASE}" --schema STREAMLIT
    
    log_success "Streamlit app deployed"
}

# Deploy demand sensing notebook to Snowflake
deploy_notebook() {
    log_info "Deploying demand sensing notebook..."
    
    # Upload notebook AND environment file to stage
    snow stage copy "${SCRIPT_DIR}/notebooks/demand_sensing.ipynb" \
        "@${DATABASE}.NOTEBOOKS.NOTEBOOK_STAGE" \
        --overwrite --connection "${CONNECTION}" --warehouse "${WAREHOUSE}" --role "${ROLE}"
    
    snow stage copy "${SCRIPT_DIR}/notebooks/environment.yml" \
        "@${DATABASE}.NOTEBOOKS.NOTEBOOK_STAGE" \
        --overwrite --connection "${CONNECTION}" --warehouse "${WAREHOUSE}" --role "${ROLE}"
    
    # Create notebook from stage (packages from environment.yml picked up automatically)
    snow sql -q "
        CREATE OR REPLACE NOTEBOOK ${DATABASE}.NOTEBOOKS.DEMAND_SENSING
            FROM '@${DATABASE}.NOTEBOOKS.NOTEBOOK_STAGE'
            MAIN_FILE = 'demand_sensing.ipynb'
            QUERY_WAREHOUSE = '${WAREHOUSE}';
        
        ALTER NOTEBOOK ${DATABASE}.NOTEBOOKS.DEMAND_SENSING ADD LIVE VERSION FROM LAST;
    " --connection "${CONNECTION}" --warehouse "${WAREHOUSE}" --role "${ROLE}"
    
    log_success "Notebook deployed"
}

# Main deployment flow
main() {
    echo ""
    echo "=============================================="
    echo "  Snowcore Procurement Intelligence Demo"
    echo "  Deployment Script"
    echo "=============================================="
    echo ""
    
    # Always check prerequisites
    check_prerequisites
    
    # Determine what to deploy
    if [ "$DEPLOY_ALL" = true ]; then
        log_info "Running full deployment..."
        deploy_infrastructure
        deploy_atomic_layer
        deploy_raw_layer
        deploy_mart_layer
        deploy_cortex
        load_data
        deploy_streamlit
        deploy_notebook
    else
        # Partial deployment based on flags
        if [ "$DEPLOY_INFRASTRUCTURE" = true ]; then
            log_info "Deploying infrastructure only..."
            deploy_infrastructure
            deploy_atomic_layer
            deploy_raw_layer
            deploy_mart_layer
        fi
        
        if [ "$DEPLOY_DATA" = true ]; then
            log_info "Deploying data only..."
            load_data
        fi
        
        if [ "$DEPLOY_CORTEX" = true ]; then
            log_info "Deploying Cortex services only..."
            deploy_cortex
        fi
        
        if [ "$DEPLOY_STREAMLIT" = true ]; then
            log_info "Deploying Streamlit only..."
            deploy_streamlit
        fi
        
        if [ "$DEPLOY_NOTEBOOK" = true ]; then
            log_info "Deploying notebook only..."
            deploy_notebook
        fi
    fi
    
    echo ""
    log_success "Deployment completed successfully!"
    echo ""
    echo "Next steps:"
    echo "  1. Run './run.sh test' to validate deployment"
    echo "  2. Run './run.sh main' to run demand sensing model"
    echo ""
}

# Parse arguments and run main function
parse_args "$@"
main
