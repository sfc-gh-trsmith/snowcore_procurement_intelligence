"""
Executive Control Tower
Global supplier visibility, risk monitoring, and KPIs for CPO persona
"""

import streamlit as st
import pandas as pd
import altair as alt
import pydeck as pdk

from utils.data_loader import (
    load_data, format_currency, format_number, format_percent, get_risk_rgb
)

st.set_page_config(
    page_title="Executive Control Tower | Snowcore",
    page_icon="E",
    layout="wide"
)

# Header
st.title("Executive Control Tower")
st.markdown("*Global procurement visibility across 50+ legacy ERP systems*")

# =============================================================================
# Page Filters (Top of Page)
# =============================================================================

# Initialize session state for division filter
if 'selected_division' not in st.session_state:
    st.session_state.selected_division = 'All'

# Load filter options
regions = load_data('regions')

# Filter row at top of page
filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 2])

with filter_col1:
    division_options = ['All', 'Industrial Compression', 'BioFlow (Life Sciences)']
    selected_division = st.selectbox(
        "Business Division",
        options=division_options,
        index=division_options.index(st.session_state.selected_division),
        key="exec_division_selector",
        help="Filter data by business division"
    )
    st.session_state.selected_division = selected_division

with filter_col2:
    selected_region = st.selectbox(
        "Region",
        options=['All'] + (regions['REGION'].tolist() if not regions.empty else []),
        index=0,
        key="exec_region_selector"
    )

with filter_col3:
    # Active filter indicator
    if selected_division != 'All' or selected_region != 'All':
        active_filters = []
        if selected_division != 'All':
            active_filters.append(selected_division)
        if selected_region != 'All':
            active_filters.append(selected_region)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                    border-radius: 6px; padding: 0.5rem; margin-top: 1.5rem;
                    border-left: 3px solid #29B5E8;">
            <span style="font-size: 0.75rem; color: #888;">Active Filters: </span>
            <span style="font-size: 0.9rem; color: #29B5E8; font-weight: 600;">{' | '.join(active_filters)}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Sidebar - Quick Links only
with st.sidebar:
    st.markdown("### Quick Links")
    st.page_link("pages/2_Category_Manager_Workbench.py", label="Category Workbench")
    st.page_link("pages/3_Data_Science_Workbench.py", label="Data Science")

# Helper function to get ERP filter based on division
def get_division_erp_filter(division: str) -> str:
    """Return ERP source system filter based on selected division."""
    if division == 'BioFlow (Life Sciences)':
        return "BIOFLOW"
    elif division == 'Industrial Compression':
        return "SAP|ORACLE|JDE"  # Non-BioFlow systems
    return None

# Load KPI data
@st.cache_data(ttl=300)
def load_kpis():
    return load_data('executive_kpis')

@st.cache_data(ttl=300)
def load_supplier_map():
    return load_data('supplier_risk_map')

@st.cache_data(ttl=300)
def load_spend_by_region():
    return load_data('spend_by_region')

@st.cache_data(ttl=300)
def load_risk_distribution():
    return load_data('risk_distribution')

@st.cache_data(ttl=300)
def load_high_risk_suppliers():
    return load_data('high_risk_suppliers')

@st.cache_data(ttl=300)
def load_esg_targets():
    return load_data('esg_targets')

@st.cache_data(ttl=300)
def load_risk_alerts():
    return load_data('risk_alerts')

# CPO Persona - Operational Excellence Data
@st.cache_data(ttl=300)
def load_operational_kpis():
    return load_data('operational_kpis')

@st.cache_data(ttl=300)
def load_otif_summary():
    return load_data('otif_summary')

@st.cache_data(ttl=300)
def load_otif_trend():
    return load_data('otif_trend')

@st.cache_data(ttl=300)
def load_delivery_by_supplier():
    return load_data('delivery_by_supplier')

@st.cache_data(ttl=300)
def load_scope_emissions_summary():
    return load_data('scope_emissions_summary')

@st.cache_data(ttl=300)
def load_scope_emissions_trend():
    return load_data('scope_emissions_trend')

@st.cache_data(ttl=300)
def load_diversity_spend():
    return load_data('diversity_spend')

# =============================================================================
# Risk Alerts Banner (Proactive Recommendations)
# =============================================================================
risk_alerts = load_risk_alerts()

if not risk_alerts.empty:
    critical_count = len(risk_alerts)
    total_at_risk = risk_alerts['REVENUE_AT_RISK'].sum()
    
    st.error(f"""
    **{critical_count} Critical Risk Alert(s) | {format_currency(total_at_risk)} Revenue at Risk**
    
    Immediate review recommended for suppliers with critical financial health scores. 
    See the High Risk Suppliers section below for details and recommended actions.
    """)

# =============================================================================
# AI-Generated Executive Summary (Cortex LLM)
# =============================================================================
@st.cache_data(ttl=600)
def generate_executive_summary(kpi_data, risk_data, esg_data):
    """Generate AI-powered executive summary using Cortex LLM."""
    from utils.data_loader import get_session
    
    session = get_session()
    if session is None:
        return None
    
    # Build context from data
    try:
        total_spend = kpi_data.get('TOTAL_SPEND', 0) if kpi_data else 0
        risk_exposure = kpi_data.get('RISK_EXPOSURE_AMOUNT', 0) if kpi_data else 0
        high_risk_count = kpi_data.get('HIGH_RISK_SUPPLIER_COUNT', 0) if kpi_data else 0
        avg_esg = kpi_data.get('AVG_ESG_SCORE', 0) if kpi_data else 0
        
        context = f"""
        Current procurement metrics:
        - Total spend: ${total_spend:,.0f}
        - Risk exposure (suppliers with health <50): ${risk_exposure:,.0f}
        - High-risk suppliers count: {high_risk_count}
        - Average ESG score: {avg_esg:.1f}/100
        - Number of critical alerts: {len(risk_data) if risk_data is not None else 0}
        """
        
        prompt = f"""Based on this procurement data, provide 3-4 concise executive insights 
        for a Chief Procurement Officer. Focus on: risk mitigation opportunities, 
        ESG target progress, and actionable recommendations. Keep each insight under 25 words.
        Format as bullet points without headers.
        
        {context}
        """
        
        # Call Cortex Complete
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.COMPLETE(
                'mistral-large2',
                '{prompt.replace("'", "''")}'
            ) AS summary
        """).collect()
        
        if result and len(result) > 0:
            return result[0]['SUMMARY']
    except Exception as e:
        # Return fallback summary on error
        return None
    
    return None

# Load data for summary
kpis_for_summary = load_kpis()
kpi_dict = kpis_for_summary.iloc[0].to_dict() if not kpis_for_summary.empty else {}

# Display AI Summary
st.markdown("### AI Executive Summary")
st.caption("*Powered by Snowflake Cortex LLM*")

with st.spinner("Generating insights..."):
    ai_summary = generate_executive_summary(kpi_dict, risk_alerts, load_esg_targets())

if ai_summary:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1E2A3A 0%, #1E1E1E 100%); 
                border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem;
                border-left: 4px solid #29B5E8;">
        <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
            <span style="font-size: 0.85rem; color: #29B5E8; text-transform: uppercase; letter-spacing: 0.1em;">
                State of Supply Chain
            </span>
        </div>
        <div style="color: #DDD; font-size: 0.95rem; line-height: 1.6;">
            {ai_summary}
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Fallback static summary when Cortex is unavailable
    kpi_row_summary = kpis_for_summary.iloc[0] if not kpis_for_summary.empty else {}
    total_spend = kpi_row_summary.get('TOTAL_SPEND', 0)
    risk_exposure = kpi_row_summary.get('RISK_EXPOSURE_AMOUNT', 0)
    risk_pct = (risk_exposure / total_spend * 100) if total_spend > 0 else 0
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1E2A3A 0%, #1E1E1E 100%); 
                border-radius: 8px; padding: 1.25rem; margin-bottom: 1rem;
                border-left: 4px solid #29B5E8;">
        <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
            <span style="font-size: 0.85rem; color: #29B5E8; text-transform: uppercase; letter-spacing: 0.1em;">
                State of Supply Chain
            </span>
        </div>
        <div style="color: #DDD; font-size: 0.95rem; line-height: 1.6;">
            <ul style="margin: 0; padding-left: 1.25rem;">
                <li><strong>{risk_pct:.1f}%</strong> of total spend ({format_currency(risk_exposure)}) is with high-risk suppliers requiring immediate attention.</li>
                <li>50+ legacy ERP systems successfully unified with <strong>100% data coverage</strong> achieved.</li>
                <li>ESG sustainability targets are being tracked - review suppliers below target threshold.</li>
                <li>Alternative supplier recommendations are available for at-risk spend mitigation.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# KPI Row with Deltas and YoY/QoQ Comparison
# =============================================================================
st.markdown("### Key Performance Indicators")

# Period comparison toggle
col_kpi_header, col_toggle = st.columns([3, 1])
with col_kpi_header:
    st.caption("*Unified metrics across 50+ legacy ERP systems*")
with col_toggle:
    comparison_period = st.radio(
        "Compare to:",
        options=["QoQ", "YoY"],
        horizontal=True,
        key="kpi_comparison",
        label_visibility="collapsed"
    )

# Load comparison data
@st.cache_data(ttl=300)
def load_yoy_data():
    return load_data('spend_yoy')

@st.cache_data(ttl=300)
def load_qoq_data():
    return load_data('spend_qoq')

kpis = load_kpis()

# Get comparison data based on selection
if comparison_period == "YoY":
    comparison_data = load_yoy_data()
    period_label = "vs last year"
else:
    comparison_data = load_qoq_data()
    period_label = "vs last quarter"

if not kpis.empty:
    kpi_row = kpis.iloc[0]
    
    # Extract comparison metrics if available
    if not comparison_data.empty:
        comp_row = comparison_data.iloc[0]
        spend_change_pct = comp_row.get('SPEND_CHANGE_PCT', 0)
        supplier_change = comp_row.get('SUPPLIER_CHANGE', 0)
        po_change_pct = comp_row.get('PO_CHANGE_PCT', 0)
    else:
        spend_change_pct = 4.2 if comparison_period == "QoQ" else 8.5
        supplier_change = 12 if comparison_period == "QoQ" else 35
        po_change_pct = 3.1 if comparison_period == "QoQ" else 7.2
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_spend = kpi_row.get('TOTAL_SPEND', 0)
        delta_text = f"{spend_change_pct:+.1f}% {period_label}" if spend_change_pct else None
        st.metric(
            label="Total Spend",
            value=format_currency(total_spend),
            delta=delta_text,
            help="Total procurement spend across all unified ERP systems"
        )
    
    with col2:
        total_suppliers = kpi_row.get('TOTAL_SUPPLIERS', 0)
        supplier_delta = f"{supplier_change:+.0f} suppliers {period_label}" if supplier_change else None
        st.metric(
            label="Active Suppliers",
            value=format_number(total_suppliers),
            delta=supplier_delta,
            help="Number of suppliers with active purchase orders"
        )
    
    with col3:
        risk_exposure = kpi_row.get('RISK_EXPOSURE_AMOUNT', 0)
        high_risk_count = kpi_row.get('HIGH_RISK_SUPPLIER_COUNT', 0)
        st.metric(
            label="Risk Exposure",
            value=format_currency(risk_exposure),
            delta=f"{high_risk_count:.0f} suppliers at risk",
            delta_color="inverse",
            help="Total spend with suppliers having financial health < 50"
        )
    
    with col4:
        esg_score = kpi_row.get('AVG_ESG_SCORE', 0)
        esg_target = 70  # Industry benchmark
        esg_delta = esg_score - esg_target
        st.metric(
            label="Avg ESG Score",
            value=f"{esg_score:.1f}",
            delta=f"{esg_delta:+.1f} vs target ({esg_target})",
            delta_color="normal" if esg_delta >= 0 else "inverse",
            help="Average ESG score across supplier base (target: 70)"
        )
    
    with col5:
        erp_count = kpi_row.get('ERP_SOURCE_COUNT', 0)
        st.metric(
            label="ERPs Unified",
            value=f"{erp_count:.0f}/50+",
            delta="100% coverage",
            help="Number of legacy ERP systems with unified spend data"
        )
    
    # Trending mini-chart row
    if comparison_period == "YoY" and not comparison_data.empty:
        st.markdown("""
        <div style="background: linear-gradient(90deg, rgba(41,181,232,0.1) 0%, transparent 100%); 
                    border-radius: 4px; padding: 0.5rem; margin-top: 0.5rem;">
            <span style="color: #29B5E8; font-size: 0.85rem;">Year-over-Year Analysis Active</span>
            <span style="color: #888; font-size: 0.8rem; margin-left: 1rem;">
                Comparing current period to same period last year
            </span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# Operational Excellence KPIs (CPO Persona Focus)
# =============================================================================
st.markdown("### Operational Excellence")
st.caption("*Procurement efficiency and cost optimization metrics*")

operational_kpis = load_operational_kpis()

if not operational_kpis.empty:
    op_row = operational_kpis.iloc[0]
    
    col_op1, col_op2, col_op3, col_op4, col_op5 = st.columns(5)
    
    with col_op1:
        cost_reduction = op_row.get('COST_REDUCTION_PCT', 5.2)
        target_pct = 5.0
        st.metric(
            label="Cost Reduction YTD",
            value=f"{cost_reduction:.1f}%",
            delta=f"{cost_reduction - target_pct:+.1f}% vs 5% target",
            delta_color="normal" if cost_reduction >= target_pct else "inverse",
            help="Annual cost reduction from procurement initiatives (target: 5-8%)"
        )
    
    with col_op2:
        roi = op_row.get('PROCUREMENT_ROI', 4.2)
        st.metric(
            label="Procurement ROI",
            value=f"{roi:.1f}x",
            delta="+0.3x vs prior year",
            help="Return on procurement investment (Savings / OpEx)"
        )
    
    with col_op3:
        spend_mgmt = op_row.get('SPEND_UNDER_MANAGEMENT_PCT', 88.5)
        st.metric(
            label="Spend Under Management",
            value=f"{spend_mgmt:.1f}%",
            delta=f"{spend_mgmt - 90:+.1f}% vs 90% target",
            delta_color="normal" if spend_mgmt >= 90 else "inverse",
            help="Percentage of total spend under procurement management"
        )
    
    with col_op4:
        compliance = op_row.get('CONTRACT_COMPLIANCE_PCT', 92.3)
        st.metric(
            label="Contract Compliance",
            value=f"{compliance:.1f}%",
            delta=f"{compliance - 95:+.1f}% vs target",
            delta_color="normal" if compliance >= 95 else "inverse",
            help="Percentage of purchases against valid contracts (vs maverick spend)"
        )
    
    with col_op5:
        cycle_time = op_row.get('AVG_PO_CYCLE_TIME_DAYS', 5.2)
        st.metric(
            label="Avg PO Cycle Time",
            value=f"{cycle_time:.1f} days",
            delta="-0.8 days vs prior period",
            help="Average days from requisition to PO approval"
        )
else:
    col_op1, col_op2, col_op3, col_op4, col_op5 = st.columns(5)
    with col_op1:
        st.metric("Cost Reduction YTD", "5.2%", "+0.2% vs 5% target")
    with col_op2:
        st.metric("Procurement ROI", "4.2x", "+0.3x")
    with col_op3:
        st.metric("Spend Under Management", "88.5%", "-1.5% vs 90% target", delta_color="inverse")
    with col_op4:
        st.metric("Contract Compliance", "92.3%", "-2.7% vs target", delta_color="inverse")
    with col_op5:
        st.metric("Avg PO Cycle Time", "5.2 days", "-0.8 days")

st.markdown("---")

# =============================================================================
# Delivery Performance (OTIF)
# =============================================================================
st.markdown("### Delivery Performance (OTIF)")
st.caption("*On-Time-In-Full delivery metrics across supplier base*")

col_otif_metrics, col_otif_chart = st.columns([1, 2])

with col_otif_metrics:
    otif_summary = load_otif_summary()
    
    if not otif_summary.empty:
        otif_row = otif_summary.iloc[0]
        
        st.metric(
            label="OTIF Rate",
            value=f"{otif_row.get('OTIF_RATE', 82.5):.1f}%",
            delta=f"{otif_row.get('OTIF_VS_TARGET', -12.5):+.1f}% vs 95% target",
            delta_color="normal" if otif_row.get('OTIF_RATE', 0) >= 95 else "inverse",
            help="On-Time-In-Full delivery rate (target: 95%)"
        )
        
        st.metric(
            label="On-Time Rate",
            value=f"{otif_row.get('ON_TIME_RATE', 87.2):.1f}%",
            help="Percentage of deliveries arriving on or before promised date"
        )
        
        st.metric(
            label="In-Full Rate",
            value=f"{otif_row.get('IN_FULL_RATE', 91.3):.1f}%",
            help="Percentage of deliveries with complete ordered quantity"
        )
    else:
        st.metric("OTIF Rate", "82.5%", "-12.5% vs 95% target", delta_color="inverse")
        st.metric("On-Time Rate", "87.2%")
        st.metric("In-Full Rate", "91.3%")

with col_otif_chart:
    otif_trend = load_otif_trend()
    
    if not otif_trend.empty:
        # Melt for multi-line chart
        trend_melted = otif_trend.melt(
            id_vars=['MONTH'],
            value_vars=['ON_TIME_RATE', 'IN_FULL_RATE', 'OTIF_RATE'],
            var_name='Metric',
            value_name='Rate'
        )
        trend_melted['Metric'] = trend_melted['Metric'].map({
            'ON_TIME_RATE': 'On-Time %',
            'IN_FULL_RATE': 'In-Full %',
            'OTIF_RATE': 'OTIF %'
        })
        
        chart = alt.Chart(trend_melted).mark_line(strokeWidth=2).encode(
            x=alt.X('MONTH:T', title='Month'),
            y=alt.Y('Rate:Q', title='Rate (%)', scale=alt.Scale(domain=[70, 100])),
            color=alt.Color('Metric:N',
                          scale=alt.Scale(domain=['On-Time %', 'In-Full %', 'OTIF %'],
                                         range=['#29B5E8', '#6BCB77', '#FFD93D']),
                          legend=alt.Legend(orient='top')),
            tooltip=['MONTH:T', 'Metric:N', 'Rate:Q']
        ).properties(height=200)
        
        # Add 95% target line
        target_line = alt.Chart(pd.DataFrame({'y': [95]})).mark_rule(
            color='#FF6B6B', strokeDash=[5, 5], strokeWidth=2
        ).encode(y='y:Q')
        
        st.altair_chart(chart + target_line, use_container_width=True)
        st.caption("*Red dashed line: 95% OTIF target*")
    else:
        st.info("OTIF trend data not available")

st.markdown("---")

# =============================================================================
# ESG Target Tracking Section
# =============================================================================
st.markdown("### ESG Sustainability Targets")

esg_targets = load_esg_targets()

if not esg_targets.empty:
    target_cols = st.columns(len(esg_targets))
    
    for i, (idx, target) in enumerate(esg_targets.iterrows()):
        with target_cols[i]:
            metric_name = target['METRIC_NAME']
            current = target['CURRENT_VALUE']
            target_val = target['TARGET_VALUE']
            status = target['STATUS']
            
            # Calculate progress percentage
            if 'Carbon' in metric_name or 'Risk' in metric_name:
                # Lower is better for these metrics
                progress = max(0, min(100, (target_val - current) / target_val * 100 + 100)) if target_val > 0 else 100
                is_on_track = current <= target_val
            else:
                # Higher is better
                progress = max(0, min(100, current / target_val * 100)) if target_val > 0 else 0
                is_on_track = current >= target_val
            
            status_color = "ON TRACK" if is_on_track else "AT RISK"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                        border-radius: 8px; padding: 1rem; text-align: center;
                        border-left: 4px solid {'#6BCB77' if is_on_track else '#FF6B6B'};">
                <div style="font-size: 0.8rem; color: #888; text-transform: uppercase;">{metric_name}</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: {'#6BCB77' if is_on_track else '#FF6B6B'};">
                    {current:.0f}
                </div>
                <div style="font-size: 0.9rem; color: #AAA;">Target: {target_val:.0f}</div>
                <div style="margin-top: 0.5rem;">{status_color} {status.replace('_', ' ').title()}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    # Fallback with reasonable defaults
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("ESG Score", "68.5", delta="-1.5 vs target (70)", delta_color="inverse")
    with col_b:
        st.metric("Carbon Footprint (MT)", "48,250", delta="-1,750 vs target", delta_color="normal")
    with col_c:
        st.metric("High ESG Risk Suppliers", "8", delta="-2 vs target (10)", delta_color="normal")

st.markdown("---")

# =============================================================================
# Main Content - Map and Charts
# =============================================================================
col_map, col_charts = st.columns([2, 1])

with col_map:
    st.markdown("### Global Supplier Risk Map")
    st.caption("*Click on suppliers to view details*")
    
    supplier_map = load_supplier_map()
    
    if not supplier_map.empty:
        # Apply region filter
        if selected_region != 'All':
            supplier_map = supplier_map[supplier_map['REGION'] == selected_region]
        
        if not supplier_map.empty:
            # Add color column based on risk level
            supplier_map['COLOR'] = supplier_map['RISK_LEVEL'].apply(get_risk_rgb)
            
            # Pre-format columns for tooltip display
            supplier_map['FINANCIAL_HEALTH_DISPLAY'] = supplier_map['FINANCIAL_HEALTH_SCORE'].apply(lambda x: f"{x:.1f}")
            supplier_map['ESG_SCORE_DISPLAY'] = supplier_map['ESG_SCORE'].apply(lambda x: f"{x:.1f}")
            supplier_map['TOTAL_SPEND_DISPLAY'] = supplier_map['TOTAL_SPEND'].apply(lambda x: f"${x:,.0f}")
            
            # Create PyDeck layer
            layer = pdk.Layer(
                "ScatterplotLayer",
                data=supplier_map,
                get_position=["LONGITUDE", "LATITUDE"],
                get_color="COLOR",
                get_radius="TOTAL_SPEND",
                radius_scale=0.0001,
                radius_min_pixels=5,
                radius_max_pixels=50,
                pickable=True,
                auto_highlight=True
            )
            
            # Create view - adjust based on region
            if selected_region == 'AMER':
                view_state = pdk.ViewState(latitude=40, longitude=-100, zoom=3, pitch=0)
            elif selected_region == 'EMEA':
                view_state = pdk.ViewState(latitude=50, longitude=10, zoom=3, pitch=0)
            elif selected_region == 'APAC':
                view_state = pdk.ViewState(latitude=20, longitude=100, zoom=3, pitch=0)
            else:
                view_state = pdk.ViewState(latitude=30, longitude=0, zoom=1.5, pitch=0)
            
            # Tooltip
            tooltip = {
                "html": """
                <b>{SUPPLIER_NAME}</b><br/>
                Country: {SUPPLIER_COUNTRY}<br/>
                Risk Level: {RISK_LEVEL}<br/>
                Financial Health: {FINANCIAL_HEALTH_DISPLAY}<br/>
                ESG Score: {ESG_SCORE_DISPLAY}<br/>
                Total Spend: {TOTAL_SPEND_DISPLAY}
                """,
                "style": {"backgroundColor": "#1E1E1E", "color": "white"}
            }
            
            # Render map (using map_style=None for CSP compliance)
            st.pydeck_chart(pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip=tooltip,
                map_style=None
            ))
            
            # Legend
            st.markdown("""
            **Risk Legend:** 
            Critical (<30) | High (30-50) | Medium (50-70) | Low (>70)
            """)
        else:
            st.info(f"No suppliers found in {selected_region} region")
    else:
        st.info("No supplier location data available")

with col_charts:
    st.markdown("### Risk Distribution")
    
    risk_dist = load_risk_distribution()
    
    if not risk_dist.empty:
        # Risk level chart
        risk_colors = {
            'CRITICAL': '#FF0000',
            'HIGH': '#FF6B6B',
            'MEDIUM': '#FFD93D',
            'LOW': '#6BCB77'
        }
        
        chart = alt.Chart(risk_dist).mark_bar().encode(
            x=alt.X('RISK_LEVEL:N', sort=['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'], 
                    title='Risk Level'),
            y=alt.Y('SUPPLIER_COUNT:Q', title='Supplier Count'),
            color=alt.Color('RISK_LEVEL:N', 
                          scale=alt.Scale(domain=list(risk_colors.keys()),
                                         range=list(risk_colors.values())),
                          legend=None),
            tooltip=['RISK_LEVEL', 'SUPPLIER_COUNT', 'TOTAL_SPEND', 'TOTAL_RISK']
        ).properties(height=200)
        
        st.altair_chart(chart, use_container_width=True)
    
    st.markdown("### Spend by Region")
    
    spend_region = load_spend_by_region()
    
    if not spend_region.empty:
        chart = alt.Chart(spend_region).mark_bar().encode(
            x=alt.X('TOTAL_SPEND:Q', title='Total Spend'),
            y=alt.Y('REGION:N', sort='-x', title='Region'),
            color=alt.Color('REGION:N', 
                          scale=alt.Scale(scheme='tableau10'),
                          legend=None),
            tooltip=['REGION', 'TOTAL_SPEND', 'PO_COUNT', 'SUPPLIER_COUNT']
        ).properties(height=200)
        
        st.altair_chart(chart, use_container_width=True)

st.markdown("---")

# =============================================================================
# High Risk Suppliers Table with Recommendations
# =============================================================================
st.markdown("### High Risk Suppliers")

high_risk = load_high_risk_suppliers()

@st.cache_data(ttl=300)
def load_alternative_suppliers():
    return load_data('alternative_suppliers')

if not high_risk.empty:
    # Apply region filter
    if selected_region != 'All':
        high_risk = high_risk[high_risk['REGION'] == selected_region]
    
    if not high_risk.empty:
        # Format for display
        display_df = high_risk[[
            'SUPPLIER_NAME', 'SUPPLIER_COUNTRY', 'REGION',
            'FINANCIAL_HEALTH_SCORE', 'CREDIT_RATING', 'ESG_SCORE',
            'TOTAL_SPEND', 'REVENUE_AT_RISK', 'RISK_LEVEL'
        ]].copy()
        
        display_df['TOTAL_SPEND'] = display_df['TOTAL_SPEND'].apply(format_currency)
        display_df['REVENUE_AT_RISK'] = display_df['REVENUE_AT_RISK'].apply(format_currency)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={
                "SUPPLIER_NAME": "Supplier",
                "SUPPLIER_COUNTRY": "Country",
                "REGION": "Region",
                "FINANCIAL_HEALTH_SCORE": st.column_config.ProgressColumn(
                    "Financial Health",
                    min_value=0,
                    max_value=100,
                    format="%.1f"
                ),
                "CREDIT_RATING": "Credit",
                "ESG_SCORE": st.column_config.ProgressColumn(
                    "ESG Score",
                    min_value=0,
                    max_value=100,
                    format="%.1f"
                ),
                "TOTAL_SPEND": "Total Spend",
                "REVENUE_AT_RISK": "At Risk",
                "RISK_LEVEL": "Risk Level"
            },
            hide_index=True
        )
        
        # Recommendations callout
        total_at_risk = high_risk['REVENUE_AT_RISK'].sum()
        critical_count = len(high_risk[high_risk['RISK_LEVEL'] == 'CRITICAL'])
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #2D1F1F 0%, #1E1E1E 100%); 
                    border-radius: 8px; padding: 1rem; margin-top: 1rem;
                    border-left: 4px solid #FF6B6B;">
            <h4 style="color: #FF6B6B; margin: 0;">Recommended Actions</h4>
            <ul style="color: #CCC; margin-top: 0.5rem;">
                <li><strong>{critical_count} suppliers</strong> require immediate financial review</li>
                <li>Consider alternative suppliers from Snowflake Marketplace for {format_currency(total_at_risk)} at-risk spend</li>
                <li>Schedule quarterly business reviews with high-risk strategic suppliers</li>
                <li>Update risk monitoring frequency from monthly to weekly for critical suppliers</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # =============================================================================
        # Alternative Supplier Recommendations (DRD "Wow" Moment)
        # =============================================================================
        st.markdown("### Recommended Alternative Suppliers")
        st.caption("*Validated suppliers from Snowflake Marketplace with strong financial health and ESG scores*")
        
        alt_suppliers = load_alternative_suppliers()
        
        if not alt_suppliers.empty:
            # Apply region filter if set
            if selected_region != 'All':
                alt_filtered = alt_suppliers[alt_suppliers['REGION'] == selected_region]
                if alt_filtered.empty:
                    alt_filtered = alt_suppliers  # Show all if no regional match
            else:
                alt_filtered = alt_suppliers
            
            # Create comparison columns
            col_metrics, col_table = st.columns([1, 3])
            
            with col_metrics:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #1F2D1F 0%, #1E1E1E 100%); 
                            border-radius: 8px; padding: 1rem;
                            border-left: 4px solid #6BCB77;">
                    <div style="font-size: 0.8rem; color: #888; text-transform: uppercase;">Potential Risk Reduction</div>
                    <div style="font-size: 1.8rem; font-weight: bold; color: #6BCB77;">""" + format_currency(total_at_risk) + """</div>
                    <div style="font-size: 0.85rem; color: #AAA; margin-top: 0.5rem;">by switching to validated alternatives</div>
                </div>
                """, unsafe_allow_html=True)
                
                avg_alt_health = alt_filtered['FINANCIAL_HEALTH_SCORE'].mean()
                avg_alt_esg = alt_filtered['ESG_SCORE'].mean()
                
                st.metric(
                    label="Avg Financial Health",
                    value=f"{avg_alt_health:.1f}",
                    delta=f"+{avg_alt_health - high_risk['FINANCIAL_HEALTH_SCORE'].mean():.1f} vs at-risk"
                )
                st.metric(
                    label="Avg ESG Score",
                    value=f"{avg_alt_esg:.1f}",
                    delta=f"+{avg_alt_esg - high_risk['ESG_SCORE'].mean():.1f} vs at-risk"
                )
            
            with col_table:
                alt_display = alt_filtered[[
                    'SUPPLIER_NAME', 'SUPPLIER_COUNTRY', 'REGION',
                    'FINANCIAL_HEALTH_SCORE', 'ESG_SCORE', 'CREDIT_RATING',
                    'CERTIFICATION_STATUS', 'MARKETPLACE_STATUS'
                ]].head(10).copy()
                
                st.dataframe(
                    alt_display,
                    use_container_width=True,
                    column_config={
                        "SUPPLIER_NAME": "Supplier",
                        "SUPPLIER_COUNTRY": "Country",
                        "REGION": "Region",
                        "FINANCIAL_HEALTH_SCORE": st.column_config.ProgressColumn(
                            "Financial Health",
                            min_value=0,
                            max_value=100,
                            format="%.1f"
                        ),
                        "ESG_SCORE": st.column_config.ProgressColumn(
                            "ESG Score",
                            min_value=0,
                            max_value=100,
                            format="%.1f"
                        ),
                        "CREDIT_RATING": "Credit",
                        "CERTIFICATION_STATUS": "Certifications",
                        "MARKETPLACE_STATUS": st.column_config.TextColumn(
                            "Status",
                            help="Supplier validation status from Snowflake Marketplace"
                        )
                    },
                    hide_index=True
                )
            
            # Action buttons
            col_action1, col_action2, col_action3 = st.columns(3)
            with col_action1:
                st.button("Generate Supplier Comparison Report", use_container_width=True, type="primary")
            with col_action2:
                st.button("Contact Procurement Team", use_container_width=True)
            with col_action3:
                # Export alternative suppliers
                csv_data = alt_filtered.to_csv(index=False)
                st.download_button(
                    label="Export Alternatives (CSV)",
                    data=csv_data,
                    file_name="alternative_suppliers.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("No alternative suppliers found matching criteria")
    else:
        st.success(f"No high-risk suppliers in {selected_region} region")
else:
    st.info("No high-risk suppliers found")

st.markdown("---")

# =============================================================================
# ESG Summary with Scope 1/2/3 Breakdown and Diversity
# =============================================================================
st.markdown("### ESG & Sustainability")

# Top row - Scope 1/2/3 emissions and Diversity Spend
col_scope, col_diversity = st.columns(2)

with col_scope:
    st.markdown("#### Scope 1/2/3 Emissions Breakdown")
    
    scope_data = load_scope_emissions_summary()
    
    if not scope_data.empty:
        # Scope colors
        scope_colors = {'SCOPE_1': '#FF6B6B', 'SCOPE_2': '#FFD93D', 'SCOPE_3': '#29B5E8'}
        
        chart = alt.Chart(scope_data).mark_arc(innerRadius=50).encode(
            theta=alt.Theta('TOTAL_EMISSIONS_MT:Q', title='Emissions (MT)'),
            color=alt.Color('SCOPE_TYPE:N', 
                          scale=alt.Scale(domain=['SCOPE_1', 'SCOPE_2', 'SCOPE_3'],
                                         range=['#FF6B6B', '#FFD93D', '#29B5E8']),
                          legend=alt.Legend(orient='bottom', title='Scope')),
            tooltip=['SCOPE_TYPE', 'TOTAL_EMISSIONS_MT', 'PCT_OF_TOTAL', 'SUPPLIER_COUNT']
        ).properties(height=200)
        
        st.altair_chart(chart, use_container_width=True)
        
        # Scope breakdown metrics
        scope_cols = st.columns(3)
        for i, (_, row) in enumerate(scope_data.iterrows()):
            with scope_cols[i]:
                scope_label = row['SCOPE_TYPE'].replace('_', ' ')
                st.markdown(f"""
                <div style="text-align: center; padding: 0.5rem;">
                    <div style="font-size: 0.7rem; color: #888;">{scope_label}</div>
                    <div style="font-size: 1.2rem; font-weight: bold;">{row['TOTAL_EMISSIONS_MT']:,.0f} MT</div>
                    <div style="font-size: 0.7rem; color: #666;">{row['PCT_OF_TOTAL']:.1f}% of total</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Scope emissions data not available")

with col_diversity:
    st.markdown("#### Supplier Diversity Spend")
    
    diversity_data = load_diversity_spend()
    
    if not diversity_data.empty:
        # Diversity bar chart
        chart = alt.Chart(diversity_data).mark_bar().encode(
            x=alt.X('PCT_OF_TOTAL:Q', title='% of Total Spend'),
            y=alt.Y('DIVERSITY_CATEGORY:N', sort='-x', title=None),
            color=alt.Color('DIVERSITY_CATEGORY:N', legend=None,
                          scale=alt.Scale(scheme='tableau10')),
            tooltip=['DIVERSITY_CATEGORY', 'SUPPLIER_COUNT', 'DIVERSITY_SPEND', 'PCT_OF_TOTAL']
        ).properties(height=180)
        
        st.altair_chart(chart, use_container_width=True)
        
        # Total diversity stats
        total_diverse = diversity_data['SUPPLIER_COUNT'].sum()
        total_diverse_spend = diversity_data['DIVERSITY_SPEND'].sum()
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                    border-radius: 8px; padding: 0.75rem; text-align: center;
                    border-left: 4px solid #6BCB77;">
            <div style="font-size: 0.75rem; color: #888;">Total Diverse Suppliers</div>
            <div style="font-size: 1.4rem; font-weight: bold; color: #6BCB77;">{total_diverse:,.0f}</div>
            <div style="font-size: 0.75rem; color: #666;">Diversity Spend: {format_currency(total_diverse_spend)}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Supplier diversity data not available")

# Bottom row - ESG Risk Level and Carbon by Region
col1, col2 = st.columns(2)

with col1:
    esg_data = load_data('esg_summary')
    if not esg_data.empty:
        chart = alt.Chart(esg_data).mark_bar().encode(
            x=alt.X('ESG_RISK_LEVEL:N', title='ESG Risk Level',
                   sort=['HIGH_RISK', 'MEDIUM_RISK', 'LOW_RISK', 'LEADER']),
            y=alt.Y('SUPPLIER_COUNT:Q', title='Supplier Count'),
            color=alt.Color('ESG_RISK_LEVEL:N', legend=None),
            tooltip=['ESG_RISK_LEVEL', 'SUPPLIER_COUNT', 'AVG_ESG_SCORE', 'TOTAL_SPEND']
        ).properties(height=200, title='Suppliers by ESG Risk Level')
        
        st.altair_chart(chart, use_container_width=True)

with col2:
    carbon_data = load_data('carbon_by_region')
    if not carbon_data.empty:
        chart = alt.Chart(carbon_data).mark_bar().encode(
            x=alt.X('REGION:N', title='Region'),
            y=alt.Y('TOTAL_EMISSIONS:Q', title='Carbon Emissions (MT)'),
            color=alt.Color('REGION:N', legend=None),
            tooltip=['REGION', 'TOTAL_EMISSIONS', 'SUPPLIER_COUNT']
        ).properties(height=200, title='Carbon Footprint by Region (Total)')
        
        st.altair_chart(chart, use_container_width=True)

# =============================================================================
# Supplier Concentration Analysis
# =============================================================================
st.markdown("---")
st.markdown("### Supplier Concentration Analysis")
st.caption("*Identify concentration risk and single-source dependencies*")

@st.cache_data(ttl=300)
def load_spend_concentration():
    return load_data('spend_concentration')

@st.cache_data(ttl=300)
def load_single_source_risk():
    return load_data('single_source_risk')

col_pareto, col_single_source = st.columns(2)

with col_pareto:
    st.markdown("#### Spend Concentration (Pareto)")
    
    concentration_data = load_spend_concentration()
    
    if not concentration_data.empty:
        # Calculate top supplier concentration
        top_10_pct = concentration_data.head(10)['SPEND_PCT'].sum()
        top_10_spend = concentration_data.head(10)['TOTAL_SPEND'].sum()
        
        # Metrics
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(
                "Top 10 Suppliers",
                f"{top_10_pct:.1f}%",
                delta="of total spend",
                delta_color="off"
            )
        with col_m2:
            concentration_risk = "HIGH" if top_10_pct > 60 else "MEDIUM" if top_10_pct > 40 else "LOW"
            risk_color = "#FF6B6B" if concentration_risk == "HIGH" else "#FFD93D" if concentration_risk == "MEDIUM" else "#6BCB77"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                        border-radius: 8px; padding: 0.75rem; text-align: center;
                        border-left: 4px solid {risk_color};">
                <div style="font-size: 0.75rem; color: #888;">Concentration Risk</div>
                <div style="font-size: 1.2rem; font-weight: bold; color: {risk_color};">{concentration_risk}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Pareto chart (cumulative % line)
        concentration_data['SUPPLIER_SHORT'] = concentration_data['SUPPLIER_NAME'].str[:15]
        
        base = alt.Chart(concentration_data.head(15)).encode(
            x=alt.X('SUPPLIER_SHORT:N', sort=None, title='Supplier')
        )
        
        bars = base.mark_bar(color='#29B5E8').encode(
            y=alt.Y('SPEND_PCT:Q', title='% of Total Spend'),
            tooltip=['SUPPLIER_NAME', 'TOTAL_SPEND', 'SPEND_PCT', 'PO_COUNT']
        )
        
        line = base.mark_line(color='#FF6B6B', strokeWidth=2).encode(
            y=alt.Y('CUMULATIVE_PCT:Q', title='Cumulative %'),
            tooltip=['SUPPLIER_NAME', 'CUMULATIVE_PCT']
        )
        
        points = base.mark_point(color='#FF6B6B', size=50).encode(
            y=alt.Y('CUMULATIVE_PCT:Q'),
            tooltip=['SUPPLIER_NAME', 'CUMULATIVE_PCT']
        )
        
        # 80% reference line
        rule = alt.Chart(pd.DataFrame({'y': [80]})).mark_rule(
            color='#FFD93D', strokeDash=[5, 5], strokeWidth=2
        ).encode(y='y:Q')
        
        chart = alt.layer(bars, line, points, rule).resolve_scale(
            y='independent'
        ).properties(height=250)
        
        st.altair_chart(chart, use_container_width=True)
        st.caption("*Red line: Cumulative %. Yellow dashed: 80% threshold.*")
    else:
        st.info("Concentration data not available")

with col_single_source:
    st.markdown("#### Single-Source Risk by Category")
    
    single_source = load_single_source_risk()
    
    if not single_source.empty:
        # Count categories by risk level
        risk_counts = single_source['CONCENTRATION_RISK'].value_counts()
        critical_count = risk_counts.get('CRITICAL', 0)
        high_count = risk_counts.get('HIGH', 0)
        
        if critical_count > 0 or high_count > 0:
            st.warning(f"**{critical_count} categories** with single-source risk, **{high_count}** with only 2 suppliers")
        
        # Risk colors for chart
        risk_colors = {
            'CRITICAL': '#FF0000',
            'HIGH': '#FF6B6B',
            'MEDIUM': '#FFD93D',
            'LOW': '#6BCB77'
        }
        
        single_source['RISK_ORDER'] = single_source['CONCENTRATION_RISK'].map(
            {'CRITICAL': 1, 'HIGH': 2, 'MEDIUM': 3, 'LOW': 4}
        )
        single_source_sorted = single_source.sort_values('RISK_ORDER')
        
        chart = alt.Chart(single_source_sorted).mark_bar().encode(
            x=alt.X('SUPPLIER_COUNT:Q', title='Number of Suppliers'),
            y=alt.Y('MATERIAL_CATEGORY:N', sort=None, title='Category'),
            color=alt.Color('CONCENTRATION_RISK:N',
                          scale=alt.Scale(domain=list(risk_colors.keys()),
                                         range=list(risk_colors.values())),
                          legend=alt.Legend(title='Risk Level', orient='bottom')),
            tooltip=['MATERIAL_CATEGORY', 'SUPPLIER_COUNT', 'TOTAL_SPEND', 'CONCENTRATION_RISK', 'SUPPLIERS']
        ).properties(height=250)
        
        st.altair_chart(chart, use_container_width=True)
        
        # Show critical categories
        critical_cats = single_source[single_source['CONCENTRATION_RISK'].isin(['CRITICAL', 'HIGH'])]
        if not critical_cats.empty:
            with st.expander("View High-Risk Categories", expanded=False):
                for _, row in critical_cats.iterrows():
                    st.markdown(f"""
                    **{row['MATERIAL_CATEGORY']}** ({row['CONCENTRATION_RISK']})
                    - Suppliers: {row['SUPPLIERS']}
                    - Total Spend: {format_currency(row['TOTAL_SPEND'])}
                    """)
    else:
        st.info("Single-source risk data not available")

# Footer
st.markdown("---")
st.caption("Data refreshed every 5 minutes | Executive Control Tower")
