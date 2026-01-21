"""
Snowcore Industries Intelligent Sourcing Hub
Main Streamlit Application Entry Point
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Snowcore Procurement Intelligence",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme with Snowflake branding
st.markdown("""
<style>
    /* Dark theme base */
    .stApp {
        background-color: #121212;
    }
    
    /* Snowflake Blue accents */
    .stMetric {
        background-color: #1E1E1E;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #29B5E8;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF;
    }
    
    /* KPI cards */
    .kpi-card {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 4px solid #29B5E8;
        margin-bottom: 1rem;
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #29B5E8;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #888888;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    
    .kpi-delta {
        font-size: 0.85rem;
        color: #6BCB77;
        margin-top: 0.25rem;
    }
    
    /* Persona cards */
    .persona-card {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #29B5E8;
        min-height: 280px;
    }
    
    .persona-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #29B5E8;
        margin-bottom: 0.25rem;
    }
    
    .persona-role {
        font-size: 0.85rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 1rem;
    }
    
    .persona-outcome {
        background: rgba(41, 181, 232, 0.1);
        border-radius: 8px;
        padding: 0.75rem;
        margin-top: 1rem;
    }
    
    .outcome-label {
        font-size: 0.75rem;
        color: #888;
        text-transform: uppercase;
    }
    
    .outcome-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #6BCB77;
    }
    
    /* Risk level badges */
    .risk-critical { background-color: #FF0000; color: white; padding: 4px 12px; border-radius: 4px; }
    .risk-high { background-color: #FF6B6B; color: white; padding: 4px 12px; border-radius: 4px; }
    .risk-medium { background-color: #FFD93D; color: black; padding: 4px 12px; border-radius: 4px; }
    .risk-low { background-color: #6BCB77; color: white; padding: 4px 12px; border-radius: 4px; }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1E1E1E;
    }
    
    /* Chat interface */
    .stChatMessage {
        background-color: #1E1E1E;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for division filter
if 'selected_division' not in st.session_state:
    st.session_state.selected_division = 'All'

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/f/ff/Snowflake_Logo.svg", width=150)
    st.markdown("---")
    st.markdown("### Snowcore Industries")
    st.markdown("**Intelligent Sourcing Hub**")
    st.markdown("---")
    
    # Division Selector (Global Filter)
    st.markdown("#### Business Division")
    division_options = ['All', 'Industrial Compression', 'BioFlow (Life Sciences)']
    selected_division = st.selectbox(
        "Select Division",
        options=division_options,
        index=division_options.index(st.session_state.selected_division),
        key="division_selector",
        help="Filter data by business division across all pages"
    )
    st.session_state.selected_division = selected_division
    
    if selected_division != 'All':
        div_color = "#29B5E8" if selected_division == "Industrial Compression" else "#6BCB77"
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                    border-radius: 6px; padding: 0.5rem; margin-bottom: 0.5rem;
                    border-left: 3px solid {div_color};">
            <div style="font-size: 0.75rem; color: #888;">Active Filter</div>
            <div style="font-size: 0.9rem; color: {div_color}; font-weight: 600;">{selected_division}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("#### Navigation")
    st.page_link("streamlit_app.py", label="Home")
    st.page_link("pages/1_Executive_Control_Tower.py", label="Executive Control Tower")
    st.page_link("pages/2_Category_Manager_Workbench.py", label="Category Manager Workbench")
    st.page_link("pages/3_Data_Science_Workbench.py", label="Data Science Workbench")
    st.page_link("pages/4_About.py", label="About")
    
    st.markdown("---")
    st.markdown("#### Data Sources")
    st.markdown("• **50+** Legacy ERP Systems")
    st.markdown("• Marketplace Risk Data")
    st.markdown("• Commodity Price Indices")
    st.markdown("• ESG Sustainability Scores")
    
    st.markdown("---")
    st.caption("Powered by Snowflake Cortex")

# Main content
st.title("Snowcore Industries")
st.markdown("## Intelligent Sourcing Hub")

st.markdown("""
Welcome to the **Procurement Intelligence Platform** - a GenAI-powered solution integrating 
rationalized multi-ERP spend data with Snowflake Marketplace intelligence for predictive 
sourcing and "Should-Cost" modeling.
""")

# Quick stats row with deltas
st.markdown("### Platform Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-value">50+</div>
        <div class="kpi-label">Legacy ERPs Unified</div>
        <div class="kpi-delta">100% coverage achieved</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-value">200+</div>
        <div class="kpi-label">Global Suppliers</div>
        <div class="kpi-delta">+12 new this quarter</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-value">$2.4M</div>
        <div class="kpi-label">Identified Savings</div>
        <div class="kpi-delta">5.8% PPV reduction</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="kpi-card">
        <div class="kpi-value">88%</div>
        <div class="kpi-label">Forecast Accuracy</div>
        <div class="kpi-delta">+12% vs baseline</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# Role-Based Entry Points (Persona Cards)
# =============================================================================
st.markdown("### Select Your Role")
st.caption("*Choose the view tailored to your responsibilities*")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="persona-card" style="border-left-color: #29B5E8;">
        <div class="persona-role">Strategic</div>
        <div class="persona-title">Chief Procurement Officer</div>
        <p style="color: #CCC; font-size: 0.9rem; margin-top: 0.5rem;">
            Consolidated global spend visibility, ESG target tracking, and proactive risk alerts across all 50+ ERPs.
        </p>
        <ul style="color: #AAA; font-size: 0.85rem; margin-top: 0.5rem;">
            <li>Global supplier risk map</li>
            <li>ESG sustainability targets</li>
            <li>Risk exposure monitoring</li>
        </ul>
        <div class="persona-outcome">
            <div class="outcome-label">Key Outcome</div>
            <div class="outcome-value">100% Risk Coverage</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Executive Control Tower", key="btn_cpo", use_container_width=True):
        st.switch_page("pages/1_Executive_Control_Tower.py")

with col2:
    st.markdown("""
    <div class="persona-card" style="border-left-color: #6BCB77;">
        <div class="persona-role">Operational</div>
        <div class="persona-title">Category Manager</div>
        <p style="color: #CCC; font-size: 0.9rem; margin-top: 0.5rem;">
            Compare contracted rates against market indices, identify overpayments, and negotiate better terms.
        </p>
        <ul style="color: #AAA; font-size: 0.85rem; margin-top: 0.5rem;">
            <li>Should-Cost analysis</li>
            <li>Invoice-level variance</li>
            <li>Cortex Agent chat</li>
        </ul>
        <div class="persona-outcome">
            <div class="outcome-label">Key Outcome</div>
            <div class="outcome-value">5-8% PPV Reduction</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Category Manager Workbench", key="btn_category", use_container_width=True):
        st.switch_page("pages/2_Category_Manager_Workbench.py")

with col3:
    st.markdown("""
    <div class="persona-card" style="border-left-color: #FFD93D;">
        <div class="persona-role">Technical</div>
        <div class="persona-title">Supply Chain Data Scientist</div>
        <p style="color: #CCC; font-size: 0.9rem; margin-top: 0.5rem;">
            Demand sensing model outputs, feature importance, forecast accuracy, and external indicator integration.
        </p>
        <ul style="color: #AAA; font-size: 0.85rem; margin-top: 0.5rem;">
            <li>XGBoost model metrics</li>
            <li>Feature importance</li>
            <li>90-day forecasts</li>
        </ul>
        <div class="persona-outcome">
            <div class="outcome-label">Key Outcome</div>
            <div class="outcome-value">+12% Forecast Accuracy</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Open Data Science Workbench", key="btn_ds", use_container_width=True):
        st.switch_page("pages/3_Data_Science_Workbench.py")

st.markdown("---")

# Demo scenario (The "Wow" Moment)
st.markdown("### Demo Scenario: The 'Wow' Moment")

st.info("""
**Ask the Cortex Agent:**

*"Identify suppliers for BioFlow precision components with high financial risk scores"*

The system instantly:
1. Returns a list of at-risk suppliers
2. Calculates the revenue at risk
3. Recommends validated alternative suppliers from the Snowflake Marketplace

**Result:** Time-to-insight reduced from **weeks** (manual spreadsheets) to **seconds**.
""")

st.markdown("---")

# Key capabilities summary
st.markdown("### Platform Capabilities")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### Cortex Intelligence
    - **Analyst**: Natural language to SQL for procurement analytics
    - **Search**: RAG over supplier contracts and compliance documents
    - **Agent**: Unified routing for compound queries
    
    #### Unified Data Layer
    - 50+ legacy ERP systems rationalized
    - Snowflake Marketplace enrichment
    - Real-time commodity indices
    """)

with col2:
    st.markdown("""
    #### Predictive Analytics
    - XGBoost demand sensing model (Snowpark ML)
    - 90-day material demand forecasts
    - External indicator integration
    - Inventory optimization recommendations
    
    #### ESG & Sustainability
    - Supplier ESG scoring
    - Carbon footprint tracking (Scope 3)
    - Sustainability target monitoring
    """)

# Footer
st.markdown("---")
st.caption("© 2025 Snowcore Industries | Powered by Snowflake Cortex")
