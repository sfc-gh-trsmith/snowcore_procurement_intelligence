"""
About Page
Comprehensive information about the Snowcore Procurement Intelligence platform
for both business and technical audiences.
"""

import streamlit as st

st.set_page_config(
    page_title="About | Snowcore Procurement Intelligence",
    page_icon="A",
    layout="wide"
)

# =============================================================================
# Header
# =============================================================================
st.title("About This Platform")
st.markdown("*GenAI-powered procurement intelligence for rationalized multi-ERP spend data*")

st.markdown("---")

# =============================================================================
# Overview Section (Problem + Solution)
# =============================================================================
st.header("Overview")

col_problem, col_solution = st.columns([2, 1])

with col_problem:
    st.subheader("The Problem")
    st.markdown("""
    **Snowcore Industries** has expanded rapidly through M&A, resulting in a fragmented landscape 
    of **50+ legacy ERPs** across its Industrial Compression and newly acquired "BioFlow" 
    (Life Sciences) divisions.
    
    This data sprawl creates critical challenges:
    
    - **Data Silos**: Each ERP operates independently, obscuring global spend visibility
    - **Supply Chain Blind Spots**: Difficult to manage disruptions without unified supplier risk data
    - **Premium Validation**: Unable to verify "medical-grade" supplier price premiums
    - **Cost Optimization Gaps**: No ability to compare contracted rates against market indices
    - **Manual Processes**: Time-to-insight measured in weeks using spreadsheets
    
    > *"During the 2021 chip shortage, many manufacturers discovered too late that their 
    > 'diversified' supplier base actually shared common dependencies."*
    """)

with col_solution:
    st.subheader("The Solution")
    st.markdown("""
    **Intelligent Sourcing Hub** combines:
    
    - Unified data layer across all 50+ ERPs
    - Snowflake Marketplace enrichment (risk, commodities, ESG)
    - GenAI-powered analytics (Cortex Analyst, Search, Agent)
    - XGBoost demand sensing model
    - Should-Cost modeling against market indices
    
    **Result:** Time-to-insight reduced from **weeks** to **seconds**.
    """)
    
    # Key outcomes
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1F2D1F 0%, #1E1E1E 100%); 
                border-radius: 8px; padding: 1rem; margin-top: 1rem;
                border-left: 4px solid #6BCB77;">
        <div style="font-size: 0.8rem; color: #888; text-transform: uppercase;">Target Outcomes</div>
        <div style="color: #6BCB77; font-size: 1.1rem; margin-top: 0.5rem;">
            <strong>5-8%</strong> PPV Reduction<br/>
            <strong>100%</strong> Risk Coverage<br/>
            <strong>+12%</strong> Forecast Accuracy
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# Data Architecture Section
# =============================================================================
st.header("Data Architecture")

col_internal, col_external, col_outputs = st.columns(3)

with col_internal:
    st.markdown("#### Internal Data")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;
                border-left: 4px solid #29B5E8;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 600;">PO_HISTORY_GLOBAL</span>
            <span style="background: #29B5E8; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem;">ERP</span>
        </div>
        <div style="font-size: 0.85rem; color: #AAA; margin-top: 0.5rem;">
            Consolidated purchase orders from 50+ legacy systems (SAP, Oracle, JDE, BioFlow)
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;
                border-left: 4px solid #29B5E8;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 600;">SUPPLIER_MASTER</span>
            <span style="background: #29B5E8; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem;">ERP</span>
        </div>
        <div style="font-size: 0.85rem; color: #AAA; margin-top: 0.5rem;">
            Vendor data including location, certifications, and contact information
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;
                border-left: 4px solid #6BCB77;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 600;">Supplier Contracts</span>
            <span style="background: #6BCB77; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem;">DOCS</span>
        </div>
        <div style="font-size: 0.85rem; color: #AAA; margin-top: 0.5rem;">
            PDFs indexed for RAG via Cortex Search
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_external:
    st.markdown("#### External Data")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;
                border-left: 4px solid #FF6B6B;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 600;">MARKETPLACE_INDICATORS</span>
            <span style="background: #FF6B6B; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem;">MARKETPLACE</span>
        </div>
        <div style="font-size: 0.85rem; color: #AAA; margin-top: 0.5rem;">
            External features: construction index, clinical trial spend, geopolitical risk
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;
                border-left: 4px solid #FF6B6B;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 600;">COMMODITY_INDEX</span>
            <span style="background: #FF6B6B; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem;">MARKETPLACE</span>
        </div>
        <div style="font-size: 0.85rem; color: #AAA; margin-top: 0.5rem;">
            Real-time global commodity spot prices for should-cost analysis
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;
                border-left: 4px solid #FF6B6B;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 600;">SUPPLIER_RISK_SCORES</span>
            <span style="background: #FF6B6B; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem;">MARKETPLACE</span>
        </div>
        <div style="font-size: 0.85rem; color: #AAA; margin-top: 0.5rem;">
            Financial health, credit ratings, and ESG sustainability scores
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_outputs:
    st.markdown("#### Model Outputs")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;
                border-left: 4px solid #FFD93D;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 600;">DEMAND_FORECAST_PREDICTIONS</span>
            <span style="background: #FFD93D; color: black; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem;">MODEL</span>
        </div>
        <div style="font-size: 0.85rem; color: #AAA; margin-top: 0.5rem;">
            90-day material demand forecasts with confidence intervals
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;
                border-left: 4px solid #FFD93D;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 600;">SHOULD_COST_ANALYSIS</span>
            <span style="background: #FFD93D; color: black; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem;">MODEL</span>
        </div>
        <div style="font-size: 0.85rem; color: #AAA; margin-top: 0.5rem;">
            Contract vs. market price variance with savings opportunities
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem;
                border-left: 4px solid #FFD93D;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 600;">SUPPLIER_RISK_SCORES</span>
            <span style="background: #FFD93D; color: black; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem;">MODEL</span>
        </div>
        <div style="font-size: 0.85rem; color: #AAA; margin-top: 0.5rem;">
            Composite risk levels with alternative supplier recommendations
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# How It Works Section (Tabbed for Dual Audience)
# =============================================================================
st.header("How It Works")

exec_tab, tech_tab = st.tabs(["Executive Overview", "Technical Deep-Dive"])

with exec_tab:
    st.markdown("### Why Traditional Approaches Fall Short")
    
    col_trad, col_this = st.columns(2)
    
    with col_trad:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #2D1F1F 0%, #1E1E1E 100%); 
                    border-radius: 8px; padding: 1.25rem;
                    border-left: 4px solid #FF6B6B;">
            <div style="font-size: 0.9rem; color: #FF6B6B; text-transform: uppercase; letter-spacing: 0.1em;">Traditional Approach</div>
            <ul style="color: #CCC; margin-top: 0.75rem; padding-left: 1.25rem;">
                <li>Score each supplier independently</li>
                <li>Spreadsheet-based analysis (weeks)</li>
                <li>No external market benchmarks</li>
                <li>Reactive to disruptions</li>
            </ul>
            <div style="color: #888; font-size: 0.85rem; margin-top: 0.75rem; font-style: italic;">
                Misses network effects and hidden concentration risks
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_this:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1F2D1F 0%, #1E1E1E 100%); 
                    border-radius: 8px; padding: 1.25rem;
                    border-left: 4px solid #6BCB77;">
            <div style="font-size: 0.9rem; color: #6BCB77; text-transform: uppercase; letter-spacing: 0.1em;">This Platform</div>
            <ul style="color: #CCC; margin-top: 0.75rem; padding-left: 1.25rem;">
                <li>Unified view across all 50+ ERPs</li>
                <li>AI-powered insights (seconds)</li>
                <li>Real-time market index comparison</li>
                <li>Proactive risk alerts with recommendations</li>
            </ul>
            <div style="color: #888; font-size: 0.85rem; margin-top: 0.75rem; font-style: italic;">
                Automated, scalable, continuously updated
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### The Three-Pillar Approach")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                    border-radius: 8px; padding: 1.25rem; text-align: center; min-height: 200px;
                    border-top: 4px solid #29B5E8;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">1</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #29B5E8;">UNIFY</div>
            <div style="font-size: 0.9rem; color: #AAA; margin-top: 0.75rem;">
                Rationalize 50+ legacy ERPs into a single source of truth using Dynamic Tables
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                    border-radius: 8px; padding: 1.25rem; text-align: center; min-height: 200px;
                    border-top: 4px solid #6BCB77;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">2</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #6BCB77;">ENRICH</div>
            <div style="font-size: 0.9rem; color: #AAA; margin-top: 0.75rem;">
                Augment with Snowflake Marketplace data: risk scores, commodity indices, ESG metrics
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                    border-radius: 8px; padding: 1.25rem; text-align: center; min-height: 200px;
                    border-top: 4px solid #FFD93D;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">3</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #FFD93D;">PREDICT</div>
            <div style="font-size: 0.9rem; color: #AAA; margin-top: 0.75rem;">
                Apply ML models and Cortex AI for demand sensing, should-cost analysis, and risk alerts
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Business Value")
    
    val_col1, val_col2, val_col3, val_col4 = st.columns(4)
    
    with val_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                    border-radius: 8px; padding: 1rem; text-align: center;
                    border-left: 4px solid #6BCB77;">
            <div style="font-size: 1.8rem; font-weight: bold; color: #6BCB77;">5-8%</div>
            <div style="font-size: 0.85rem; color: #AAA;">PPV Reduction</div>
            <div style="font-size: 0.75rem; color: #666; margin-top: 0.5rem;">via Should-Cost modeling</div>
        </div>
        """, unsafe_allow_html=True)
    
    with val_col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                    border-radius: 8px; padding: 1rem; text-align: center;
                    border-left: 4px solid #29B5E8;">
            <div style="font-size: 1.8rem; font-weight: bold; color: #29B5E8;">100%</div>
            <div style="font-size: 0.85rem; color: #AAA;">Risk Coverage</div>
            <div style="font-size: 0.75rem; color: #666; margin-top: 0.5rem;">via Marketplace enrichment</div>
        </div>
        """, unsafe_allow_html=True)
    
    with val_col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                    border-radius: 8px; padding: 1rem; text-align: center;
                    border-left: 4px solid #FFD93D;">
            <div style="font-size: 1.8rem; font-weight: bold; color: #FFD93D;">+12%</div>
            <div style="font-size: 0.85rem; color: #AAA;">Forecast Accuracy</div>
            <div style="font-size: 0.75rem; color: #666; margin-top: 0.5rem;">via XGBoost demand sensing</div>
        </div>
        """, unsafe_allow_html=True)
    
    with val_col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                    border-radius: 8px; padding: 1rem; text-align: center;
                    border-left: 4px solid #FF6B6B;">
            <div style="font-size: 1.8rem; font-weight: bold; color: #FF6B6B;">Seconds</div>
            <div style="font-size: 0.85rem; color: #AAA;">Time-to-Insight</div>
            <div style="font-size: 0.75rem; color: #666; margin-top: 0.5rem;">vs weeks (manual)</div>
        </div>
        """, unsafe_allow_html=True)
    
    # The "Wow" Moment
    st.markdown("### The 'Wow' Moment")
    st.info("""
    **Ask the Cortex Agent:**
    
    *"Identify suppliers for BioFlow precision components with high financial risk scores"*
    
    The system instantly:
    1. Returns a list of at-risk suppliers
    2. Calculates the revenue at risk  
    3. Recommends validated alternative suppliers from the Snowflake Marketplace
    
    **Result:** Proactive intervention before disruption occurs.
    """)

with tech_tab:
    st.markdown("### Data Architecture Layers")
    
    st.markdown("""
    ```
    RAW Layer                    ATOMIC Layer                 PROCUREMENT_MART Layer
    (Ingestion)                  (Normalized EDM)             (Aggregated Views)
    ─────────────────────────────────────────────────────────────────────────────────
    
    ERP Dumps (SAP, Oracle,      Dynamic Tables for           V_EXECUTIVE_KPIS
    JDE, BioFlow)         ──►    continuous transformation    V_SUPPLIER_RISK
                                                       ──►    V_SHOULD_COST_ANALYSIS
    Marketplace Feeds            SUPPLIERS_UNIFIED            V_DEMAND_FORECAST_PREDICTIONS
    (Risk, Commodity, ESG)       PURCHASE_ORDERS_UNIFIED      V_ESG_SUMMARY
                                 MARKETPLACE_ENRICHED
    ```
    """)
    
    st.markdown("### ML Model: Demand Sensing")
    
    col_model, col_features = st.columns([1, 1])
    
    with col_model:
        st.markdown("""
        **Model Specification**
        
        | Component | Choice | Rationale |
        |-----------|--------|-----------|
        | Algorithm | XGBoost Regressor | Handles mixed feature types, interpretable |
        | Target | `forecasted_material_demand_qty` | 90-day demand forecast |
        | Training | Snowpark ML | Native Snowflake, no data movement |
        | Inference | Snowflake Notebook | Scheduled or on-demand execution |
        
        **Training Configuration:**
        - Train/Test Split: 80/20 temporal
        - Cross-validation: 5-fold time-series
        - Hyperparameter tuning: Grid search
        - Output: `DEMAND_FORECAST_PREDICTIONS` table
        """)
    
    with col_features:
        st.markdown("""
        **Feature Engineering**
        
        | Feature | Type | Description |
        |---------|------|-------------|
        | `lag_consumption_7d` | Internal | 7-day rolling consumption |
        | `lag_consumption_30d` | Internal | 30-day rolling consumption |
        | `construction_starts_idx` | External | Industrial construction index |
        | `clinical_trial_spend` | External | Pharma R&D indicator |
        | `seasonality_factor` | Derived | Month/quarter encoding |
        | `supplier_lead_time` | Internal | Avg lead time by supplier |
        | `commodity_price_idx` | External | Raw material price index |
        """)
    
    st.markdown("### Cortex AI Integration")
    
    col_analyst, col_search = st.columns(2)
    
    with col_analyst:
        st.markdown("""
        **Cortex Analyst (Structured Data)**
        
        Converts natural language to SQL using a semantic model.
        
        **Semantic Model Scope:**
        - **Measures:** `Total_Spend_Amount`, `Purchase_Price_Variance`, `On_Time_Delivery_Rate`, `Carbon_Footprint_MT`
        - **Dimensions:** `Supplier_Name`, `Material_Category`, `Region`, `Risk_Level`
        - **Time Intelligence:** Date hierarchy with YoY/QoQ comparisons
        
        **Example Query:**
        ```
        "Show me the top 5 suppliers by spend in EMEA 
         who have a financial health score below 50"
        ```
        
        **Generated SQL:**
        ```sql
        SELECT Supplier_Name, SUM(Total_Spend_Amount) 
        FROM PROCUREMENT_MART 
        WHERE Region = 'EMEA' 
          AND Financial_Health_Score < 50 
        GROUP BY Supplier_Name 
        ORDER BY 2 DESC LIMIT 5
        ```
        """)
    
    with col_search:
        st.markdown("""
        **Cortex Search (Unstructured Data / RAG)**
        
        Enables Q&A over supplier contracts and compliance documents.
        
        **Service Configuration:**
        - **Service Name:** `SUPPLIER_COMPLIANCE_SEARCH_SERVICE`
        - **Indexed Content:** Contracts, Audits, Regulatory Findings
        - **Chunking:** 512 tokens with 50 token overlap
        - **Embedding Model:** e5-base-v2
        
        **Example Query:**
        ```
        "Summarize the indemnification clauses for our 
         primary BioFlow reagent supplier and check if 
         they have any recent regulatory warning letters"
        ```
        
        **Cortex Agent** routes queries to the appropriate service based on intent.
        """)
    
    st.markdown("### Dynamic Tables Pipeline")
    
    st.markdown("""
    Dynamic Tables provide declarative, incremental data transformation:
    
    ```sql
    CREATE OR REPLACE DYNAMIC TABLE PROCUREMENT_MART.SUPPLIER_RISK_UNIFIED
        TARGET_LAG = '1 hour'
        WAREHOUSE = COMPUTE_WH
    AS
    SELECT 
        s.supplier_id,
        s.supplier_name,
        m.financial_health_score,
        m.esg_score,
        CASE 
            WHEN m.financial_health_score < 30 THEN 'CRITICAL'
            WHEN m.financial_health_score < 50 THEN 'HIGH'
            WHEN m.financial_health_score < 70 THEN 'MEDIUM'
            ELSE 'LOW'
        END AS risk_level
    FROM ATOMIC.SUPPLIERS s
    JOIN ATOMIC.MARKETPLACE_RISK m ON s.supplier_id = m.supplier_id;
    ```
    
    **Benefits:**
    - Automatic refresh when source data changes
    - Incremental processing (only changed rows)
    - Declarative (define "what", not "how")
    """)

st.markdown("---")

# =============================================================================
# Application Pages Section
# =============================================================================
st.header("Application Pages")

col_page1, col_page2 = st.columns(2)

with col_page1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem;
                border-left: 4px solid #29B5E8;">
        <div style="font-size: 0.8rem; color: #888; text-transform: uppercase;">Strategic</div>
        <div style="font-size: 1.1rem; font-weight: 600; color: #29B5E8;">Executive Control Tower</div>
        <div style="font-size: 0.9rem; color: #AAA; margin-top: 0.5rem;">
            Global supplier visibility, risk monitoring, ESG targets, and AI-generated executive summaries. 
            Designed for CPO and strategic procurement leadership.
        </div>
        <div style="font-size: 0.85rem; color: #666; margin-top: 0.75rem;">
            Key Features: Global risk map, KPI dashboard, concentration analysis, alternative supplier recommendations
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem;
                border-left: 4px solid #6BCB77;">
        <div style="font-size: 0.8rem; color: #888; text-transform: uppercase;">Operational</div>
        <div style="font-size: 1.1rem; font-weight: 600; color: #6BCB77;">Category Manager Workbench</div>
        <div style="font-size: 0.9rem; color: #AAA; margin-top: 0.5rem;">
            Should-Cost analysis, invoice-level variance identification, and Cortex Agent chat interface.
            Designed for category managers and sourcing specialists.
        </div>
        <div style="font-size: 0.85rem; color: #666; margin-top: 0.75rem;">
            Key Features: Contract vs. market price comparison, supplier scorecard, renegotiation playbook generator
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_page2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem;
                border-left: 4px solid #FFD93D;">
        <div style="font-size: 0.8rem; color: #888; text-transform: uppercase;">Technical</div>
        <div style="font-size: 1.1rem; font-weight: 600; color: #FFD93D;">Data Science Workbench</div>
        <div style="font-size: 0.9rem; color: #AAA; margin-top: 0.5rem;">
            Demand sensing model performance, feature importance, external indicator correlation, and forecast outputs.
            Designed for data scientists and ML engineers.
        </div>
        <div style="font-size: 0.85rem; color: #666; margin-top: 0.75rem;">
            Key Features: Model registry, accuracy metrics, business impact quantification, correlation explorer
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem;
                border-left: 4px solid #888;">
        <div style="font-size: 0.8rem; color: #888; text-transform: uppercase;">Reference</div>
        <div style="font-size: 1.1rem; font-weight: 600; color: #888;">About (This Page)</div>
        <div style="font-size: 0.9rem; color: #AAA; margin-top: 0.5rem;">
            Comprehensive documentation for both business stakeholders and technical practitioners.
        </div>
        <div style="font-size: 0.85rem; color: #666; margin-top: 0.75rem;">
            Key Features: Problem/solution overview, data architecture, dual-audience explanations
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# Technology Stack Section
# =============================================================================
st.header("Technology Stack")

tech_cols = st.columns(6)

tech_items = [
    ("Snowflake", "#29B5E8", "Core Data Platform"),
    ("Streamlit", "#FF4B4B", "Interactive UI"),
    ("Snowpark ML", "#6BCB77", "XGBoost Training"),
    ("Cortex AI", "#FFD93D", "LLM + Analyst + Search"),
    ("Dynamic Tables", "#29B5E8", "Incremental ETL"),
    ("Marketplace", "#FF6B6B", "External Data"),
]

for i, (name, color, desc) in enumerate(tech_items):
    with tech_cols[i]:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                    border-radius: 8px; padding: 1rem; text-align: center;
                    border-top: 3px solid {color};">
            <div style="font-size: 1rem; font-weight: 600; color: {color};">{name}</div>
            <div style="font-size: 0.75rem; color: #888; margin-top: 0.25rem;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# Getting Started Section
# =============================================================================
st.header("Getting Started")

col_queries, col_resources = st.columns(2)

with col_queries:
    st.markdown("#### Sample Questions for Cortex Agent")
    st.markdown("""
    **Structured Data (Cortex Analyst):**
    - "What is our total spend with high-risk suppliers?"
    - "Show top 5 EMEA suppliers by spend with low financial health"
    - "What are the potential savings from should-cost analysis?"
    - "Identify suppliers for BioFlow precision components with high financial risk"
    
    **Documents (Cortex Search):**
    - "What are the payment terms for our German suppliers?"
    - "Summarize indemnification clauses for BioFlow suppliers"
    - "Are there any recent regulatory warning letters for our reagent suppliers?"
    """)

with col_resources:
    st.markdown("#### Quick Links")
    st.page_link("streamlit_app.py", label="Home - Role Selection")
    st.page_link("pages/1_Executive_Control_Tower.py", label="Executive Control Tower")
    st.page_link("pages/2_Category_Manager_Workbench.py", label="Category Manager Workbench")
    st.page_link("pages/3_Data_Science_Workbench.py", label="Data Science Workbench")
    
    st.markdown("#### Data Refresh")
    st.markdown("""
    - **Dashboard data:** Cached for 5 minutes
    - **Dynamic Tables:** TARGET_LAG = 1 hour
    - **ML Predictions:** Updated via scheduled notebook
    """)

# =============================================================================
# Footer
# =============================================================================
st.markdown("---")
st.caption("Snowcore Industries Intelligent Sourcing Hub | Powered by Snowflake Cortex")
