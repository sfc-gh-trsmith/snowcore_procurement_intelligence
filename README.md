# Snowcore Industries Intelligent Sourcing Hub

A GenAI-powered procurement optimization platform integrating rationalized multi-ERP spend data with Snowflake Marketplace intelligence (Risk, Commodities, ESG) to drive predictive sourcing and "Should-Cost" modeling.

## Problem Statement

**Snowcore Industries** has expanded rapidly through M&A, resulting in a fragmented landscape of **50+ legacy ERPs** across its Industrial Compression and newly acquired "BioFlow" (Life Sciences) divisions. This data sprawl creates:

- **Data Silos**: Each ERP operates independently, obscuring global spend visibility
- **Supply Chain Blind Spots**: Difficult to manage disruptions without unified supplier risk data
- **Premium Validation Gaps**: Unable to verify "medical-grade" supplier price premiums
- **Cost Optimization Challenges**: No ability to compare contracted rates against market indices
- **Manual Processes**: Time-to-insight measured in weeks using spreadsheets

## Solution

The **Intelligent Sourcing Hub** unifies, enriches, and predicts:

1. **UNIFY** - Rationalize 50+ legacy ERPs into a single source of truth
2. **ENRICH** - Augment with Snowflake Marketplace data (risk, commodities, ESG)
3. **PREDICT** - Apply ML models and Cortex AI for demand sensing and risk alerts

**Result:** Time-to-insight reduced from **weeks** to **seconds**.

## Quick Start

```bash
# Deploy all infrastructure and data
./deploy.sh

# Run validation tests
./run.sh test

# Start the Streamlit application locally (for development)
./run.sh main

# Clean up all resources
./clean.sh
```

### Deployment Options

```bash
./deploy.sh                      # Full deployment (all components)
./deploy.sh --only-infrastructure  # Deploy database/schemas/tables only
./deploy.sh --only-data           # Generate and load data only
./deploy.sh --only-cortex         # Deploy Cortex services only
./deploy.sh --only-streamlit      # Deploy Streamlit app only
./deploy.sh --only-notebook       # Deploy ML notebook only
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Data Architecture                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │    RAW Layer    │    │  ATOMIC Layer   │    │   PROCUREMENT_MART      │  │
│  │                 │    │                 │    │                         │  │
│  │ • SAP dumps     │    │ • Normalized    │    │ • V_SPEND_SUMMARY       │  │
│  │ • Oracle dumps  │ ─► │   EDM tables    │ ─► │ • V_SUPPLIER_RISK       │  │
│  │ • BioFlow data  │    │ • Dynamic       │    │ • V_SHOULD_COST_ANALYSIS│  │
│  │ • Marketplace   │    │   Tables        │    │ • V_EXECUTIVE_KPIS      │  │
│  │   feeds         │    │ • 40+ tables    │    │ • V_ESG_SUMMARY         │  │
│  └─────────────────┘    └─────────────────┘    │ • 15+ persona views     │  │
│                                                 └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
              ┌─────┴─────┐                   ┌───────┴───────┐
              │  Cortex   │                   │  Snowpark ML  │
              │   Agent   │                   │  (XGBoost)    │
              │ (Router)  │                   │               │
              └─────┬─────┘                   └───────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
  ┌─────┴─────┐ ┌───┴───┐ ┌─────┴─────┐
  │  Cortex   │ │Cortex │ │  Cortex   │
  │  Analyst  │ │Search │ │ Complete  │
  │  (SQL)    │ │ (RAG) │ │  (LLM)    │
  └───────────┘ └───────┘ └───────────┘
                    │
              ┌─────┴─────┐
              │ Streamlit │
              │ in        │
              │ Snowflake │
              └───────────┘
```

## User Personas & Application Pages

| Persona | Role | Page | Key Capabilities |
|---------|------|------|------------------|
| **Strategic** | Chief Procurement Officer (CPO) | Executive Control Tower | Global risk map, KPI dashboard, AI-generated summaries, alternative supplier recommendations |
| **Operational** | Category Manager (Metals) | Category Manager Workbench | Should-Cost analysis, supplier scorecard, Cortex Agent chat, renegotiation playbook |
| **Technical** | Supply Chain Data Scientist | Data Science Workbench | Model registry, feature importance, external indicator correlation, forecast predictions |

## Project Structure

```
snowcore_procurement_intelligence/
├── deploy.sh                     # Infrastructure + data deployment
├── run.sh                        # Runtime operations (main, test, status)
├── clean.sh                      # Complete teardown
├── README.md                     # This file
├── DRD.md                        # Demo Requirements Document
│
├── sql/                          # SQL scripts (numbered execution order)
│   ├── 01_setup.sql              # Database, schemas, stages, file formats
│   ├── 02_atomic_reference.sql   # Reference/master tables (Currency, UOM, Geography, etc.)
│   ├── 03_atomic_procurement.sql # Core procurement tables (Supplier, PO, Invoice, etc.)
│   ├── 03b_atomic_persona_extensions.sql  # CPO/Category/DS persona tables
│   ├── 04_raw_layer.sql          # RAW ingestion tables (SAP, Oracle, BioFlow, Marketplace)
│   ├── 05_mart_layer.sql         # Core PROCUREMENT_MART views
│   ├── 05b_mart_persona_extensions.sql    # Persona-specific mart views
│   ├── 06_cortex_services.sql    # Cortex Search service definition
│   └── 07_load_data.sql          # COPY INTO statements for data loading
│
├── data/
│   └── synthetic/                # Pre-generated CSV demo data (30+ files)
│       ├── supplier.csv
│       ├── purchase_order.csv
│       ├── marketplace_supplier_risk.csv
│       ├── marketplace_commodity_index.csv
│       ├── delivery_performance.csv
│       ├── supplier_scorecard.csv
│       └── ... (30+ files)
│
├── utils/
│   └── generate_synthetic_data.py    # Python script to generate demo data
│
├── streamlit/                    # Streamlit in Snowflake application
│   ├── snowflake.yml             # SiS deployment configuration
│   ├── environment.yml           # Python dependencies
│   ├── streamlit_app.py          # Main entry point (Home page)
│   ├── pages/
│   │   ├── 1_Executive_Control_Tower.py   # CPO persona dashboard
│   │   ├── 2_Category_Manager_Workbench.py # Category Manager workbench
│   │   ├── 3_Data_Science_Workbench.py    # Data Scientist workbench
│   │   └── 4_About.py                     # Documentation page
│   └── utils/
│       ├── __init__.py
│       ├── data_loader.py        # Snowflake session & query execution
│       └── query_registry.py     # Centralized SQL queries
│
├── notebooks/
│   ├── demand_sensing.ipynb      # XGBoost demand forecasting model
│   ├── environment.yml           # Notebook dependencies
│   └── snowflake.yml             # Notebook deployment config
│
├── cortex/
│   └── semantic_model.yaml       # Cortex Analyst semantic model definition
│
└── solution_presentation/        # Marketing and presentation materials
    ├── images/                   # Architecture diagrams (SVG)
    ├── ProcurementIntelligence_Overview.md
    ├── ProcurementIntelligence_Architecture.md
    ├── ProcurementIntelligence_Blog.md
    ├── ProcurementIntelligence_Slides.md
    └── ProcurementIntelligence_Video_Script.md
```

## Key Features

### Executive Control Tower (CPO Persona)

- **Global Supplier Risk Map**: PyDeck visualization with risk-colored supplier locations
- **AI Executive Summary**: Cortex LLM-generated insights on supply chain state
- **Operational Excellence KPIs**: Cost reduction, ROI, spend under management, contract compliance
- **OTIF Delivery Performance**: On-Time-In-Full metrics with trend charts
- **ESG Sustainability Dashboard**: Scope 1/2/3 emissions breakdown, diversity spend tracking
- **Supplier Concentration Analysis**: Pareto chart, single-source risk identification
- **Alternative Supplier Recommendations**: Validated alternatives from Marketplace data
- **Risk Alerts Banner**: Proactive notifications for critical supplier issues

### Category Manager Workbench (Operational Persona)

- **Category Performance KPIs**: Spend, cost per unit, forward contract coverage
- **Supplier Scorecard**: Multi-dimensional evaluation (Quality, Delivery, Price, Responsiveness)
- **Lead Time Variability Analysis**: Identify suppliers with unreliable lead times
- **Forward Contract Coverage**: Hedging position visualization by category
- **Should-Cost Analysis**: Contract price vs. market index comparison
  - Time-series trend chart
  - Category-level variance analysis
  - Potential savings identification
- **Invoice-Level Drill-Down**: Specific POs with overpayment identification
- **Renegotiation Workflow**: Flag for review, create RFQ, export CSV, generate playbook
- **Cortex Agent Chat**: Natural language queries routed to Analyst/Search/Complete
- **Commodity Index Trends**: External market indices from Marketplace

### Data Science Workbench (Technical Persona)

- **Model Operations Dashboard**: Deployed model status, algorithm comparison
- **Business Impact Metrics**: Inventory reduction, cost savings, service level improvement
- **Model Performance Summary**: Accuracy, MAPE, prediction counts by category
- **Forecast vs Actual Trend**: Time-series comparison with confidence bands
- **Feature Importance**: XGBoost feature contributions (internal vs. external)
- **External Indicator Correlation Explorer**: Scatter plots and correlation analysis
- **90-Day Demand Forecast Predictions**: Tabular view with export capability
- **Model Registry**: Version tracking, performance metrics, deployment status

### Cortex AI Integration

| Service | Purpose | Implementation |
|---------|---------|----------------|
| **Cortex Analyst** | Natural language to SQL | Semantic model with 5 views, 50+ measures/dimensions |
| **Cortex Search** | RAG over supplier documents | `SUPPLIER_COMPLIANCE_SEARCH_SERVICE` indexing contracts/audits |
| **Cortex Complete** | General LLM responses | Executive summaries, contextual answers |
| **Cortex Agent** | Unified routing | Routes queries to Analyst, Search, or Complete based on intent |

### Semantic Model (Cortex Analyst)

```yaml
Tables:
  - V_SPEND_SUMMARY: Consolidated PO spend across all ERPs
  - V_SUPPLIER_RISK: Financial health, ESG, risk levels
  - V_SHOULD_COST_ANALYSIS: Contract vs. market price variance
  - V_ESG_SUMMARY: Sustainability metrics
  - V_EXECUTIVE_KPIS: High-level executive metrics

Verified Queries:
  - "Top 5 suppliers by spend in EMEA with financial health < 50"
  - "Total spend by region"
  - "Revenue at risk from high-risk suppliers"
  - "BioFlow precision component suppliers with high financial risk"
  - "Potential savings from should-cost analysis"
```

## Data Model

### ATOMIC Layer Tables (40+ tables)

**Reference/Master Data:**
- `CURRENCY`, `UNIT_OF_MEASURE`, `GEOGRAPHY`
- `PARTY`, `PARTY_ADDRESS`, `PERSON`
- `ORGANIZATION`, `SITE`, `LOCATION`
- `PRODUCT`, `PRODUCT_CATEGORY`, `PRODUCT_COST`

**Procurement Core:**
- `SUPPLIER`, `SUPPLIER_SITE`, `SUPPLIER_PRODUCT`, `SUPPLIER_PERFORMANCE`
- `PURCHASE_ORDER`, `PURCHASE_ORDER_LINE`
- `PURCHASE_REQUISITION`, `PURCHASE_REQUISITION_LINE`
- `PURCHASE_ORDER_RECEIPT`, `PURCHASE_ORDER_RECEIPT_LINE`
- `PURCHASE_ORDER_INVOICE`, `PURCHASE_ORDER_INVOICE_LINE`
- `INVENTORY_ITEM`, `INVENTORY_BALANCE`
- `DEMAND_FORECAST`, `DEMAND_ACTUAL`

**Marketplace Integration:**
- `MARKETPLACE_COMMODITY_INDEX`: External commodity price indices
- `MARKETPLACE_SUPPLIER_RISK`: Financial health, ESG, cyber risk scores
- `MARKETPLACE_INDICATORS`: Economic indicators (construction starts, PMI, etc.)

**Persona Extensions:**
- `DELIVERY_PERFORMANCE`: OTIF tracking
- `PROCUREMENT_OPERATIONAL_METRICS`: Monthly operational KPIs
- `EMISSION_RECORD_SCOPED`: Scope 1/2/3 carbon emissions
- `SUPPLIER_DIVERSITY`: Minority/Women/Veteran-owned classifications
- `SUPPLIER_SCORECARD`: Multi-dimensional supplier evaluation
- `FORWARD_CONTRACT`: Commodity hedging positions
- `MODEL_REGISTRY`: ML model versioning and metrics
- `BUSINESS_IMPACT_METRICS`: ML model business value tracking

### PROCUREMENT_MART Views (15+ views)

**Core Views:**
- `V_SPEND_SUMMARY`, `V_SUPPLIER_RISK`, `V_SHOULD_COST_ANALYSIS`
- `V_SUPPLIER_PERFORMANCE_SUMMARY`, `V_ESG_SUMMARY`
- `V_DEMAND_FORECAST_ANALYSIS`, `V_DEMAND_FORECAST_PREDICTIONS`
- `V_EXECUTIVE_KPIS`

**CPO Persona Views:**
- `V_OPERATIONAL_KPIS`, `V_DELIVERY_PERFORMANCE`, `V_OTIF_SUMMARY`
- `V_SCOPE_EMISSIONS`, `V_SCOPE_EMISSIONS_SUMMARY`, `V_DIVERSITY_SPEND`

**Category Manager Views:**
- `V_SUPPLIER_SCORECARD_LATEST`, `V_SUPPLIER_SCORECARD_TREND`
- `V_FORWARD_CONTRACT_COVERAGE`, `V_CATEGORY_METRICS`
- `V_LEAD_TIME_VARIABILITY`

**Data Scientist Views:**
- `V_MODEL_REGISTRY`, `V_MODEL_COMPARISON`
- `V_EXTERNAL_INDICATORS_LATEST`, `V_EXTERNAL_INDICATORS_TREND`
- `V_BUSINESS_IMPACT`, `V_BUSINESS_IMPACT_SUMMARY`

## Demo Scenarios

### The "Wow" Moment

Ask the Cortex Agent:

> *"Identify suppliers for BioFlow precision components with high financial risk scores"*

The system instantly:
1. Returns a list of at-risk suppliers with financial health scores
2. Calculates the total revenue at risk
3. Recommends validated alternative suppliers from Snowflake Marketplace
4. Provides action buttons to generate comparison reports

### Golden Query (Validation)

> *"Show me the top 5 suppliers by spend in the EMEA region who have a financial health score below 50."*

Expected behavior: Cortex Analyst generates SQL, executes query, returns formatted results.

### Should-Cost Analysis Demo

1. Navigate to Category Manager Workbench
2. Filter to "Alloys & Metals" category
3. View Contract Price vs. Market Index time-series chart
4. Identify specific invoices with overpayment
5. Generate Renegotiation Playbook with talking points

### Demand Sensing Demo

1. Navigate to Data Science Workbench
2. View deployed XGBoost model metrics (88%+ accuracy)
3. Explore feature importance (internal consumption + external indicators)
4. Analyze correlation between Construction Starts Index and demand
5. Export 90-day forecast predictions

## ML Model: Demand Sensing

| Component | Specification |
|-----------|---------------|
| **Algorithm** | XGBoost Regressor |
| **Target** | `forecasted_material_demand_qty` |
| **Training** | Snowpark ML (native Snowflake) |
| **Features** | 12 features (internal + external) |
| **Accuracy** | 88%+ (MAPE < 12%) |
| **Output** | `DEMAND_FORECAST_PREDICTIONS` table |

**Feature Categories:**
- **Internal**: `lag_consumption_7d`, `lag_consumption_30d`, `inventory_level`, `supplier_lead_time`
- **External**: `construction_starts_idx`, `clinical_trial_spend`, `commodity_price_idx`
- **Derived**: `seasonality_factor`, `day_of_week`, `month`

## Requirements

- Snowflake account with Cortex enabled
- Snowflake CLI (`snow`) version 2.0+
- Python 3.11 (for local data generation)
- Role with permissions: `ACCOUNTADMIN` or equivalent

## Configuration

Default settings in deployment scripts:

```bash
DATABASE="SNOWCORE_PROCUREMENT"
WAREHOUSE="SNOWCORE_PROCUREMENT_WH"
ROLE="ACCOUNTADMIN"
CONNECTION="demo"
```

Modify variables in `deploy.sh`, `run.sh`, and `clean.sh` as needed.

## Technology Stack

| Technology | Purpose |
|------------|---------|
| **Snowflake** | Core data platform |
| **Streamlit in Snowflake** | Interactive UI |
| **Snowpark ML** | XGBoost model training |
| **Cortex AI** | LLM, Analyst, Search |
| **Dynamic Tables** | Incremental ETL |
| **Snowflake Marketplace** | External data enrichment |
| **PyDeck** | Geospatial visualization |
| **Altair** | Declarative charts |

## Target Business Outcomes

| KPI | Target | Method |
|-----|--------|--------|
| **PPV Reduction** | 5-8% | Should-Cost modeling against market indices |
| **Risk Coverage** | 100% | Marketplace financial/geopolitical data |
| **Forecast Accuracy** | +12% | XGBoost with external indicators |
| **Time-to-Insight** | Seconds | From weeks (manual spreadsheets) |

---

*© 2025 Snowcore Industries | Powered by Snowflake Cortex*
