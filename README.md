# Snowcore Industries Intelligent Sourcing Hub

A GenAI-powered procurement optimization platform integrating rationalized multi-ERP spend data with Snowflake Marketplace intelligence (Risk, Commodities, ESG) to drive predictive sourcing and "Should-Cost" modeling.

## Quick Start

```bash
# Deploy all infrastructure and data
./deploy.sh

# Run validation tests
./run.sh test

# Start the Streamlit application
./run.sh main

# Clean up all resources
./clean.sh
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           Data Architecture                          │
├─────────────────────────────────────────────────────────────────────┤
│  RAW Layer           →   ATOMIC Layer        →   PROCUREMENT_MART   │
│  (ERP dumps,             (Normalized,            (Aggregated        │
│   Marketplace feeds)      Dynamic Tables)         Views)            │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
              ┌─────┴─────┐                 ┌───────┴───────┐
              │  Cortex   │                 │  Snowpark ML  │
              │  Agent    │                 │  Notebook     │
              │ (Router)  │                 │  (XGBoost)    │
              └─────┬─────┘                 └───────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
  ┌─────┴─────┐          ┌──────┴──────┐
  │  Cortex   │          │   Cortex    │
  │  Analyst  │          │   Search    │
  │ (SQL)     │          │   (RAG)     │
  └───────────┘          └─────────────┘
                    │
              ┌─────┴─────┐
              │ Streamlit │
              │    App    │
              └───────────┘
```

## Project Structure

```
snowcore_procurement_intelligence/
├── deploy.sh              # Infrastructure + data deployment
├── run.sh                 # Runtime operations (main, test, status)
├── clean.sh               # Complete teardown
├── README.md              # This file
│
├── sql/                   # SQL scripts (numbered)
│   ├── 01_setup.sql
│   ├── 02_atomic_reference.sql
│   ├── 03_atomic_procurement.sql
│   ├── 04_raw_layer.sql
│   ├── 05_mart_layer.sql
│   ├── 06_cortex_services.sql
│   └── 07_load_data.sql
│
├── data/
│   └── synthetic/         # Pre-generated CSV data
│
├── utils/
│   └── generate_synthetic_data.py
│
├── streamlit/             # Streamlit app
│   ├── snowflake.yml
│   ├── environment.yml
│   ├── streamlit_app.py
│   ├── pages/
│   │   ├── 1_Executive_Control_Tower.py
│   │   └── 2_Category_Manager_Workbench.py
│   └── utils/
│       ├── query_registry.py
│       └── data_loader.py
│
├── notebooks/             # Snowflake notebooks
│   └── demand_sensing.ipynb
│
├── cortex/
│   └── semantic_model.yaml
│
└── solution_presentation/
    ├── images/
    └── video/
```

## User Personas

| Persona | Role | Key Story |
|---------|------|-----------|
| Strategic | Chief Procurement Officer (CPO) | View consolidated global spend across 50+ ERPs, verify ESG targets |
| Operational | Category Manager (Metals) | Compare contracted rates against market indices, identify overpayments |
| Technical | Supply Chain Data Scientist | Train demand sensing models using internal + external data |

## Key Features

### Executive Control Tower (Page 1)
- Global supplier map with risk-colored indicators
- KPI cards: Total Spend, Risk Exposure ($), ESG Score
- Real-time visibility across all 50+ legacy ERPs

### Category Manager Workbench (Page 2)
- "Should-Cost" analysis: Contract Price vs Market Index
- Cortex Agent chat interface for natural language queries
- Savings opportunity identification

### Cortex Intelligence
- **Analyst**: Natural language to SQL for spend analytics
- **Search**: RAG over supplier contracts and compliance documents
- **Agent**: Unified routing between Analyst and Search

### Demand Sensing (ML)
- XGBoost-based demand forecasting
- Features: Historical consumption + external indicators
- Output: Material demand predictions by product/site

## Demo Scenarios

### "Wow" Moment
Ask the Cortex Agent: *"Identify suppliers for BioFlow precision components with high financial risk scores"*

The system instantly:
1. Returns a list of at-risk suppliers
2. Calculates revenue exposure
3. Recommends validated alternatives

### Golden Query (Validation)
*"Show me the top 5 suppliers by spend in the EMEA region who have a financial health score below 50."*

## Requirements

- Snowflake account with Cortex enabled
- Snowflake CLI (`snow`)
- Python 3.11 (for local data generation)

## Configuration

Default settings in scripts:
- Database: `SNOWCORE_PROCUREMENT`
- Warehouse: `COMPUTE_WH`
- Role: `ACCOUNTADMIN`

Modify the variables in `deploy.sh`, `run.sh`, and `clean.sh` as needed.
# snowcore_procurement_intelligence
