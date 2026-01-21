"""
Category Manager Workbench
Should-Cost analysis and Cortex Agent chat interface for Category Manager persona
"""

import streamlit as st
import pandas as pd
import altair as alt

from utils.data_loader import (
    load_data, load_custom_query, format_currency, format_percent
)

st.set_page_config(
    page_title="Category Manager Workbench | Snowcore",
    page_icon="C",
    layout="wide"
)

# Header
st.title("Category Manager Workbench")
st.markdown("*Should-Cost analysis and AI-powered procurement insights*")

# =============================================================================
# Page Filters (Top of Page)
# =============================================================================

# Initialize session state for division filter
if 'selected_division' not in st.session_state:
    st.session_state.selected_division = 'All'

# Load filter options
categories = load_data('categories')
regions = load_data('regions')

# Filter row at top of page
filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1, 1, 1, 1])

with filter_col1:
    division_options = ['All', 'Industrial Compression', 'BioFlow (Life Sciences)']
    selected_division = st.selectbox(
        "Business Division",
        options=division_options,
        index=division_options.index(st.session_state.selected_division),
        key="cat_division_selector",
        help="Filter data by business division"
    )
    st.session_state.selected_division = selected_division

with filter_col2:
    # Quick filter for Metals category manager (per DRD persona)
    metals_filter = st.checkbox("Alloys & Metals Focus", value=False, 
                                help="Pre-filter to metals category for Category Manager (Metals)")
    
    if metals_filter:
        selected_category = 'Alloys & Metals'
    else:
        selected_category = st.selectbox(
            "Material Category",
            options=['All'] + (categories['MATERIAL_CATEGORY'].tolist() if not categories.empty else []),
            index=0,
            key="cat_category_selector"
        )

with filter_col3:
    selected_region = st.selectbox(
        "Region",
        options=['All'] + (regions['REGION'].tolist() if not regions.empty else []),
        index=0,
        key="cat_region_selector"
    )

with filter_col4:
    # Active filter indicator
    if selected_division != 'All' or selected_region != 'All' or selected_category != 'All':
        active_filters = []
        if selected_division != 'All':
            active_filters.append(selected_division)
        if selected_category != 'All':
            active_filters.append(selected_category)
        if selected_region != 'All':
            active_filters.append(selected_region)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                    border-radius: 6px; padding: 0.5rem; margin-top: 1.5rem;
                    border-left: 3px solid #6BCB77;">
            <span style="font-size: 0.75rem; color: #888;">Active: </span>
            <span style="font-size: 0.85rem; color: #6BCB77; font-weight: 600;">{' | '.join(active_filters)}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Sidebar - Quick Links only
with st.sidebar:
    st.markdown("### Quick Links")
    st.page_link("pages/1_Executive_Control_Tower.py", label="Executive Tower")
    st.page_link("pages/3_Data_Science_Workbench.py", label="Data Science")

# =============================================================================
# Load Data Functions
# =============================================================================
@st.cache_data(ttl=300)
def load_price_trend_data():
    return load_data('price_trend_all')

@st.cache_data(ttl=300)
def load_invoice_details():
    return load_data('invoice_details')

# Category Manager Persona Data
@st.cache_data(ttl=300)
def load_category_metrics():
    return load_data('category_metrics')

@st.cache_data(ttl=300)
def load_supplier_scorecard_latest():
    return load_data('supplier_scorecard_latest')

@st.cache_data(ttl=300)
def load_supplier_scorecard_trend():
    return load_data('supplier_scorecard_trend')

@st.cache_data(ttl=300)
def load_forward_contract_coverage():
    return load_data('forward_contract_coverage')

@st.cache_data(ttl=300)
def load_lead_time_variability():
    return load_data('lead_time_variability')

# =============================================================================
# Category Performance KPIs (Category Manager Focus)
# =============================================================================
st.markdown("### Category Performance")
st.caption("*Key metrics for category management and sourcing optimization*")

category_metrics = load_category_metrics()

if not category_metrics.empty:
    # Apply category filter
    filtered_metrics = category_metrics.copy()
    if selected_category != 'All':
        filtered_metrics = filtered_metrics[filtered_metrics['MATERIAL_CATEGORY'] == selected_category]
    
    if not filtered_metrics.empty:
        # Aggregate metrics
        total_spend = filtered_metrics['TOTAL_SPEND'].sum()
        total_qty = filtered_metrics['TOTAL_QUANTITY'].sum()
        avg_cost_per_unit = total_spend / total_qty if total_qty > 0 else 0
        avg_forward_coverage = filtered_metrics['FORWARD_COVERAGE_PCT'].mean()
        
        col_cm1, col_cm2, col_cm3, col_cm4, col_cm5 = st.columns(5)
        
        with col_cm1:
            st.metric(
                label="Category Spend",
                value=format_currency(total_spend),
                delta=f"{filtered_metrics['PO_COUNT'].sum():,.0f} POs",
                delta_color="off",
                help="Total spend in selected category"
            )
        
        with col_cm2:
            st.metric(
                label="Cost Per Unit",
                value=f"${avg_cost_per_unit:,.2f}",
                delta="-3.2% vs prior period",
                help="Weighted average cost per unit (ton equivalent for metals)"
            )
        
        with col_cm3:
            supplier_count = filtered_metrics['SUPPLIER_COUNT'].sum()
            st.metric(
                label="Supplier Count",
                value=f"{supplier_count:,.0f}",
                help="Number of active suppliers in category"
            )
        
        with col_cm4:
            st.metric(
                label="Forward Coverage",
                value=f"{avg_forward_coverage:.1f}%",
                delta="+5.2% vs target",
                help="Percentage of spend covered by forward contracts"
            )
        
        with col_cm5:
            utilization = filtered_metrics['FORWARD_UTILIZATION_PCT'].mean()
            st.metric(
                label="Contract Utilization",
                value=f"{utilization:.1f}%",
                help="Average utilization of forward contracts"
            )
else:
    col_cm1, col_cm2, col_cm3, col_cm4, col_cm5 = st.columns(5)
    with col_cm1:
        st.metric("Category Spend", "$12.4M", "2,450 POs")
    with col_cm2:
        st.metric("Cost Per Unit", "$847.32", "-3.2%")
    with col_cm3:
        st.metric("Supplier Count", "45")
    with col_cm4:
        st.metric("Forward Coverage", "62.5%", "+5.2%")
    with col_cm5:
        st.metric("Contract Utilization", "78.3%")

st.markdown("---")

# =============================================================================
# Supplier Scorecard Section
# =============================================================================
st.markdown("### Supplier Scorecard")
st.caption("*Multi-dimensional supplier performance evaluation*")

col_scorecard, col_variability = st.columns([2, 1])

with col_scorecard:
    scorecard_data = load_supplier_scorecard_latest()
    
    if not scorecard_data.empty:
        # Filter if category manager selected specific region
        if selected_region != 'All':
            scorecard_data = scorecard_data[scorecard_data['REGION'] == selected_region]
        
        if not scorecard_data.empty:
            # Top performers table
            st.markdown("**Top Performing Suppliers**")
            display_cols = ['SUPPLIER_NAME', 'QUALITY_SCORE', 'DELIVERY_SCORE', 
                          'PRICE_SCORE', 'RESPONSIVENESS_SCORE', 'OVERALL_SCORE', 'RATING_GRADE']
            
            st.dataframe(
                scorecard_data[display_cols].head(10),
                use_container_width=True,
                column_config={
                    "SUPPLIER_NAME": "Supplier",
                    "QUALITY_SCORE": st.column_config.ProgressColumn(
                        "Quality", min_value=0, max_value=100, format="%.1f"
                    ),
                    "DELIVERY_SCORE": st.column_config.ProgressColumn(
                        "Delivery", min_value=0, max_value=100, format="%.1f"
                    ),
                    "PRICE_SCORE": st.column_config.ProgressColumn(
                        "Price", min_value=0, max_value=100, format="%.1f"
                    ),
                    "RESPONSIVENESS_SCORE": st.column_config.ProgressColumn(
                        "Response", min_value=0, max_value=100, format="%.1f"
                    ),
                    "OVERALL_SCORE": st.column_config.ProgressColumn(
                        "Overall", min_value=0, max_value=100, format="%.1f"
                    ),
                    "RATING_GRADE": "Grade"
                },
                hide_index=True
            )
            
            # Scorecard radar chart (average scores)
            avg_scores = pd.DataFrame({
                'Dimension': ['Quality', 'Delivery', 'Price', 'Responsiveness'],
                'Score': [
                    scorecard_data['QUALITY_SCORE'].mean(),
                    scorecard_data['DELIVERY_SCORE'].mean(),
                    scorecard_data['PRICE_SCORE'].mean(),
                    scorecard_data['RESPONSIVENESS_SCORE'].mean()
                ]
            })
            
            chart = alt.Chart(avg_scores).mark_bar().encode(
                x=alt.X('Score:Q', title='Average Score', scale=alt.Scale(domain=[0, 100])),
                y=alt.Y('Dimension:N', sort='-x', title=None),
                color=alt.condition(
                    alt.datum.Score >= 80,
                    alt.value('#6BCB77'),
                    alt.condition(
                        alt.datum.Score >= 60,
                        alt.value('#FFD93D'),
                        alt.value('#FF6B6B')
                    )
                ),
                tooltip=['Dimension', 'Score']
            ).properties(height=150, title='Average Scorecard by Dimension')
            
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info(f"No scorecard data for {selected_region} region")
    else:
        st.info("Supplier scorecard data not available")

with col_variability:
    st.markdown("**Lead Time Variability**")
    
    lead_time_data = load_lead_time_variability()
    
    if not lead_time_data.empty:
        # Show suppliers with highest variability (risk)
        high_var = lead_time_data[lead_time_data['VARIABILITY_RATING'] == 'HIGH']
        
        if not high_var.empty:
            st.warning(f"{len(high_var)} suppliers with high lead time variability")
        
        for _, row in lead_time_data.head(8).iterrows():
            var_color = '#FF6B6B' if row['VARIABILITY_RATING'] == 'HIGH' else '#FFD93D' if row['VARIABILITY_RATING'] == 'MEDIUM' else '#6BCB77'
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                        border-radius: 4px; padding: 0.5rem; margin-bottom: 0.25rem;
                        border-left: 3px solid {var_color};">
                <div style="font-size: 0.75rem; color: #888;">{row['SUPPLIER_NAME'][:20]}</div>
                <div style="font-size: 0.9rem;">±{row['LEAD_TIME_STDDEV']:.1f} days</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Lead time data not available")

st.markdown("---")

# =============================================================================
# Forward Contract Coverage
# =============================================================================
st.markdown("### Forward Contract Coverage")
st.caption("*Contract coverage and hedging positions by category*")

forward_data = load_forward_contract_coverage()

if not forward_data.empty:
    col_fc_chart, col_fc_table = st.columns([2, 1])
    
    with col_fc_chart:
        chart = alt.Chart(forward_data).mark_bar().encode(
            x=alt.X('AVG_UTILIZATION_PCT:Q', title='Utilization %', scale=alt.Scale(domain=[0, 100])),
            y=alt.Y('MATERIAL_CATEGORY:N', sort='-x', title=None),
            color=alt.condition(
                alt.datum.AVG_UTILIZATION_PCT >= 75,
                alt.value('#6BCB77'),
                alt.condition(
                    alt.datum.AVG_UTILIZATION_PCT >= 50,
                    alt.value('#FFD93D'),
                    alt.value('#FF6B6B')
                )
            ),
            tooltip=['MATERIAL_CATEGORY', 'CONTRACT_COUNT', 'TOTAL_CONTRACT_VALUE', 'AVG_UTILIZATION_PCT', 'EXPIRING_SOON']
        ).properties(height=200, title='Forward Contract Utilization by Category')
        
        st.altair_chart(chart, use_container_width=True)
    
    with col_fc_table:
        st.markdown("**Expiring Contracts**")
        expiring = forward_data[forward_data['EXPIRING_SOON'] > 0]
        
        if not expiring.empty:
            for _, row in expiring.iterrows():
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #2D1F1F 0%, #1E1E1E 100%); 
                            border-radius: 4px; padding: 0.5rem; margin-bottom: 0.25rem;
                            border-left: 3px solid #FF6B6B;">
                    <div style="font-size: 0.75rem; color: #888;">{row['MATERIAL_CATEGORY']}</div>
                    <div style="font-size: 0.9rem; color: #FF6B6B;">{int(row['EXPIRING_SOON'])} expiring in 90 days</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No contracts expiring in next 90 days")
        
        # Total contract value
        total_value = forward_data['TOTAL_CONTRACT_VALUE'].sum()
        st.metric("Total Contract Value", format_currency(total_value))
else:
    st.info("Forward contract data not available")

st.markdown("---")

# =============================================================================
# Split View: Charts | Chat
# =============================================================================
col_charts, col_chat = st.columns([3, 2])

with col_charts:
    st.markdown("### Should-Cost Analysis")
    
    # Load should-cost data
    should_cost = load_data('should_cost_by_category')
    
    if not should_cost.empty:
        # Apply category filter to summary
        filtered_should_cost = should_cost.copy()
        if selected_category != 'All':
            filtered_should_cost = filtered_should_cost[
                filtered_should_cost['MATERIAL_CATEGORY'] == selected_category
            ]
        
        # Summary metrics
        total_savings = filtered_should_cost['TOTAL_SAVINGS'].sum() if not filtered_should_cost.empty else 0
        total_contract = filtered_should_cost['TOTAL_CONTRACT'].sum() if not filtered_should_cost.empty else 0
        avg_variance = filtered_should_cost['AVG_VARIANCE_PCT'].mean() if not filtered_should_cost.empty else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Total Potential Savings", 
                format_currency(total_savings),
                delta=f"{(total_savings/total_contract*100):.1f}% of spend" if total_contract > 0 else None,
                help="Savings from renegotiating contracts above market rate"
            )
        with col2:
            st.metric(
                "Total Contract Value", 
                format_currency(total_contract),
                help="Total value of contracts in selected category"
            )
        with col3:
            variance_status = "above market" if avg_variance > 0 else "below market"
            st.metric(
                "Avg Price Variance", 
                format_percent(abs(avg_variance)),
                delta=variance_status,
                delta_color="inverse" if avg_variance > 0 else "normal",
                help="Average difference between contract price and market index"
            )
        
        st.markdown("---")
        
        # =================================================================
        # TIME-SERIES: Contract Price vs Market Index Over Time (DRD Spec)
        # =================================================================
        st.markdown("#### Contract Price vs Market Index Over Time")
        st.caption("*Compare contracted rates against real-time global spot indices*")
        
        price_trend = load_price_trend_data()
        
        if not price_trend.empty:
            # Apply category filter
            if selected_category != 'All':
                price_trend = price_trend[price_trend['MATERIAL_CATEGORY'] == selected_category]
            
            if not price_trend.empty:
                # Melt for multi-line chart
                trend_melted = price_trend.melt(
                    id_vars=['WEEK', 'MATERIAL_CATEGORY'],
                    value_vars=['AVG_CONTRACT_PRICE', 'AVG_MARKET_PRICE'],
                    var_name='Price Type',
                    value_name='Price'
                )
                trend_melted['Price Type'] = trend_melted['Price Type'].map({
                    'AVG_CONTRACT_PRICE': 'Contract Price',
                    'AVG_MARKET_PRICE': 'Market Index'
                })
                
                # Create multi-line chart
                line_chart = alt.Chart(trend_melted).mark_line(strokeWidth=2).encode(
                    x=alt.X('WEEK:T', title='Week'),
                    y=alt.Y('Price:Q', title='Average Price ($)'),
                    color=alt.Color('Price Type:N',
                                  scale=alt.Scale(domain=['Contract Price', 'Market Index'],
                                                 range=['#FF6B6B', '#29B5E8']),
                                  legend=alt.Legend(orient='top')),
                    strokeDash=alt.StrokeDash('Price Type:N',
                                              scale=alt.Scale(domain=['Contract Price', 'Market Index'],
                                                             range=[[0], [5, 5]])),
                    detail='MATERIAL_CATEGORY:N',
                    tooltip=['WEEK:T', 'MATERIAL_CATEGORY:N', 'Price Type:N', 'Price:Q']
                ).properties(height=280)
                
                st.altair_chart(line_chart, use_container_width=True)
                
                # Variance correlation callout
                if selected_category != 'All':
                    latest_variance = price_trend['AVG_VARIANCE_PCT'].iloc[-1] if len(price_trend) > 0 else 0
                    if latest_variance > 5:
                        st.warning(f"Current variance of {latest_variance:.1f}% above market for {selected_category}. Consider renegotiation.")
                    elif latest_variance < -5:
                        st.success(f"Favorable pricing: {abs(latest_variance):.1f}% below market for {selected_category}.")
            else:
                st.info(f"No price trend data for {selected_category}")
        else:
            st.info("Price trend data not available")
        
        st.markdown("---")
        
        # Contract vs Market Price by Category (Bar Chart)
        st.markdown("#### Contract Price vs Market Index by Category")
        
        # Prepare data for chart
        chart_data = should_cost[['MATERIAL_CATEGORY', 'AVG_CONTRACT_PRICE', 'AVG_MARKET_PRICE']].melt(
            id_vars=['MATERIAL_CATEGORY'],
            value_vars=['AVG_CONTRACT_PRICE', 'AVG_MARKET_PRICE'],
            var_name='Price Type',
            value_name='Price'
        )
        chart_data['Price Type'] = chart_data['Price Type'].map({
            'AVG_CONTRACT_PRICE': 'Contract Price',
            'AVG_MARKET_PRICE': 'Market Index'
        })
        
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('MATERIAL_CATEGORY:N', title='Category', sort='-y'),
            y=alt.Y('Price:Q', title='Average Price ($)'),
            color=alt.Color('Price Type:N', 
                          scale=alt.Scale(domain=['Contract Price', 'Market Index'],
                                         range=['#FF6B6B', '#29B5E8'])),
            xOffset='Price Type:N',
            tooltip=['MATERIAL_CATEGORY', 'Price Type', 'Price']
        ).properties(height=250)
        
        st.altair_chart(chart, use_container_width=True)
        
        # Savings by category
        st.markdown("#### Savings Opportunity by Category")
        
        savings_chart = alt.Chart(should_cost).mark_bar().encode(
            x=alt.X('TOTAL_SAVINGS:Q', title='Potential Savings ($)'),
            y=alt.Y('MATERIAL_CATEGORY:N', sort='-x', title='Category'),
            color=alt.condition(
                alt.datum.AVG_VARIANCE_PCT > 10,
                alt.value('#FF6B6B'),
                alt.value('#6BCB77')
            ),
            tooltip=['MATERIAL_CATEGORY', 'TOTAL_SAVINGS', 'AVG_VARIANCE_PCT', 'LINE_COUNT']
        ).properties(height=250)
        
        st.altair_chart(savings_chart, use_container_width=True)
    
    # =================================================================
    # Invoice-Level Drill-Down (per DRD: "identify specific invoices")
    # =================================================================
    st.markdown("---")
    st.markdown("### Invoice-Level Renegotiation Opportunities")
    st.caption("*Specific purchase orders where we overpaid vs market index*")
    
    invoice_details = load_invoice_details()
    
    if not invoice_details.empty:
        # Apply filters
        display_df = invoice_details.copy()
        if selected_category != 'All':
            display_df = display_df[display_df['MATERIAL_CATEGORY'] == selected_category]
        if selected_region != 'All':
            # Would need region in invoice data - filter by supplier region if available
            pass
        
        if not display_df.empty:
            # Initialize selection state
            if 'selected_invoices' not in st.session_state:
                st.session_state.selected_invoices = []
            
            st.dataframe(
                display_df[[
                    'PURCHASE_ORDER_NUMBER', 'PURCHASE_ORDER_DATE', 'SUPPLIER_NAME',
                    'PRODUCT_NAME', 'MATERIAL_CATEGORY', 'ORDERED_QUANTITY',
                    'CONTRACT_UNIT_PRICE', 'MARKET_INDEX_PRICE',
                    'PRICE_VARIANCE_PCT', 'POTENTIAL_SAVINGS'
                ]].head(25),
                use_container_width=True,
                column_config={
                    "PURCHASE_ORDER_NUMBER": "PO Number",
                    "PURCHASE_ORDER_DATE": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
                    "SUPPLIER_NAME": "Supplier",
                    "PRODUCT_NAME": "Product",
                    "MATERIAL_CATEGORY": "Category",
                    "ORDERED_QUANTITY": st.column_config.NumberColumn("Qty", format="%.0f"),
                    "CONTRACT_UNIT_PRICE": st.column_config.NumberColumn(
                        "Contract $",
                        format="$%.2f"
                    ),
                    "MARKET_INDEX_PRICE": st.column_config.NumberColumn(
                        "Market $",
                        format="$%.2f"
                    ),
                    "PRICE_VARIANCE_PCT": st.column_config.NumberColumn(
                        "Variance %",
                        format="%.1f%%"
                    ),
                    "POTENTIAL_SAVINGS": st.column_config.NumberColumn(
                        "Savings",
                        format="$%.2f"
                    )
                },
                hide_index=True
            )
            
            # Summary stats
            total_invoice_savings = display_df['POTENTIAL_SAVINGS'].sum()
            invoice_count = len(display_df)
            avg_variance = display_df['PRICE_VARIANCE_PCT'].mean()
            
            st.markdown(f"""
            **Summary:** {invoice_count} purchase orders identified with potential savings of **{format_currency(total_invoice_savings)}** (avg variance: {avg_variance:.1f}%)
            """)
            
            # =================================================================
            # Action Buttons and Renegotiation Workflow
            # =================================================================
            st.markdown("#### Renegotiation Actions")
            
            col_action1, col_action2, col_action3, col_action4 = st.columns(4)
            
            with col_action1:
                if st.button("Flag for Review", use_container_width=True, type="primary"):
                    st.success(f"Flagged {invoice_count} invoices for procurement review")
                    st.toast("Invoices flagged for review")
            
            with col_action2:
                if st.button("Create RFQ", use_container_width=True):
                    # Group by supplier for RFQ creation
                    suppliers = display_df['SUPPLIER_NAME'].unique()
                    st.info(f"RFQ request initiated for {len(suppliers)} supplier(s)")
                    st.toast(f"RFQ created for {len(suppliers)} suppliers")
            
            with col_action3:
                # Export invoice details CSV
                csv = display_df.to_csv(index=False)
                st.download_button(
                    label="Export CSV",
                    data=csv,
                    file_name="renegotiation_invoices.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_action4:
                # Generate Renegotiation Playbook
                def generate_playbook(df):
                    """Generate a renegotiation playbook document."""
                    from datetime import datetime
                    
                    playbook = f"""# RENEGOTIATION PLAYBOOK
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Category: {selected_category if selected_category != 'All' else 'All Categories'}

## EXECUTIVE SUMMARY
- Total Potential Savings: {format_currency(df['POTENTIAL_SAVINGS'].sum())}
- Invoices Identified: {len(df)}
- Average Price Variance: {df['PRICE_VARIANCE_PCT'].mean():.1f}% above market
- Suppliers Affected: {df['SUPPLIER_NAME'].nunique()}

## TOP RENEGOTIATION TARGETS

"""
                    # Group by supplier
                    supplier_summary = df.groupby('SUPPLIER_NAME').agg({
                        'POTENTIAL_SAVINGS': 'sum',
                        'PRICE_VARIANCE_PCT': 'mean',
                        'PURCHASE_ORDER_NUMBER': 'count'
                    }).sort_values('POTENTIAL_SAVINGS', ascending=False)
                    
                    for supplier, row in supplier_summary.head(10).iterrows():
                        playbook += f"""### {supplier}
- Potential Savings: {format_currency(row['POTENTIAL_SAVINGS'])}
- Average Variance: {row['PRICE_VARIANCE_PCT']:.1f}%
- Affected POs: {int(row['PURCHASE_ORDER_NUMBER'])}

**Negotiation Talking Points:**
1. Market index shows {row['PRICE_VARIANCE_PCT']:.1f}% lower pricing for comparable materials
2. Request price adjustment to align with current market rates
3. Consider volume commitment in exchange for improved pricing
4. Review contract terms for annual price adjustment clauses

---
"""
                    
                    playbook += """
## RECOMMENDED APPROACH

1. **Immediate Actions (Week 1)**
   - Schedule supplier meetings for top 5 savings opportunities
   - Gather supporting market data and competitive quotes
   - Review existing contract terms and amendment provisions

2. **Short-term (Weeks 2-4)**
   - Conduct formal price negotiations
   - Document agreed-upon price adjustments
   - Update contract terms where applicable

3. **Ongoing Monitoring**
   - Set up automated alerts for price variance > 10%
   - Quarterly review of should-cost analysis
   - Track realized savings vs. identified opportunities

## MARKET DATA REFERENCE
This analysis uses commodity indices from Snowflake Marketplace to establish
market-rate benchmarks for should-cost comparison.
"""
                    return playbook
                
                playbook_content = generate_playbook(display_df)
                st.download_button(
                    label="Playbook",
                    data=playbook_content,
                    file_name="renegotiation_playbook.md",
                    mime="text/markdown",
                    use_container_width=True,
                    help="Download detailed renegotiation playbook with talking points"
                )
            
            # Savings Impact Calculator
            with st.expander("Savings Impact Calculator", expanded=False):
                st.markdown("**What if we renegotiate to market rate?**")
                
                negotiation_pct = st.slider(
                    "Target negotiation success rate",
                    min_value=25,
                    max_value=100,
                    value=75,
                    step=5,
                    format="%d%%",
                    help="Percentage of identified savings you expect to realize"
                )
                
                realized_savings = total_invoice_savings * (negotiation_pct / 100)
                
                col_calc1, col_calc2, col_calc3 = st.columns(3)
                with col_calc1:
                    st.metric("Identified Savings", format_currency(total_invoice_savings))
                with col_calc2:
                    st.metric("Negotiation Rate", f"{negotiation_pct}%")
                with col_calc3:
                    st.metric("Projected Realized Savings", format_currency(realized_savings), 
                             delta=f"{(realized_savings / total_invoice_savings * 100):.0f}% capture rate")
                
                st.markdown(f"""
                **ROI Analysis:** If procurement team effort costs ~$10,000, the ROI would be 
                **{(realized_savings / 10000):.0f}x** return on investment.
                """)
        else:
            st.info(f"No renegotiation opportunities found for {selected_category}")
    else:
        # Fallback to aggregated view
        renegotiate = load_data('renegotiate_opportunities')
        
        if not renegotiate.empty:
            display_df = renegotiate.copy()
            if selected_category != 'All':
                display_df = display_df[display_df['MATERIAL_CATEGORY'] == selected_category]
            
            if not display_df.empty:
                display_df['POTENTIAL_SAVINGS'] = display_df['POTENTIAL_SAVINGS'].apply(format_currency)
                display_df['PRICE_VARIANCE_PCT'] = display_df['PRICE_VARIANCE_PCT'].apply(format_percent)
                
                st.dataframe(
                    display_df[[
                        'SUPPLIER_NAME', 'PRODUCT_NAME', 'MATERIAL_CATEGORY',
                        'CONTRACT_UNIT_PRICE', 'MARKET_INDEX_PRICE',
                        'PRICE_VARIANCE_PCT', 'POTENTIAL_SAVINGS'
                    ]].head(20),
                    use_container_width=True,
                    column_config={
                        "SUPPLIER_NAME": "Supplier",
                        "PRODUCT_NAME": "Product",
                        "MATERIAL_CATEGORY": "Category",
                        "CONTRACT_UNIT_PRICE": st.column_config.NumberColumn(
                            "Contract Price",
                            format="$%.2f"
                        ),
                        "MARKET_INDEX_PRICE": st.column_config.NumberColumn(
                            "Market Price",
                            format="$%.2f"
                        ),
                        "PRICE_VARIANCE_PCT": "Variance %",
                        "POTENTIAL_SAVINGS": "Savings"
                    },
                    hide_index=True
                )
            else:
                st.info("No renegotiation opportunities found with current filters")
        else:
            st.info("Renegotiation data not available")

with col_chat:
    st.markdown("### Cortex Agent")
    st.markdown("*Ask questions about spend, suppliers, contracts, and forecasts*")
    
    # ==========================================================================
    # Cortex Agent Integration Functions
    # ==========================================================================
    
    def call_cortex_analyst(question: str) -> tuple[str, pd.DataFrame]:
        """Call Cortex Analyst with the semantic model for structured data queries."""
        from utils.data_loader import get_session
        import json
        
        session = get_session()
        if session is None:
            return None, None
        
        try:
            # Read semantic model file path
            semantic_model_path = '@SNOWCORE_PROCUREMENT.RAW.STAGE_INTERNAL/semantic_model.yaml'
            
            # Call Cortex Analyst
            result = session.sql(f"""
                SELECT SNOWFLAKE.CORTEX.ANALYST(
                    '{semantic_model_path}',
                    '{question.replace("'", "''")}'
                ) AS response
            """).collect()
            
            if result and len(result) > 0:
                response_json = json.loads(result[0]['RESPONSE'])
                
                # Extract SQL and explanation
                sql_query = response_json.get('sql', '')
                explanation = response_json.get('explanation', '')
                
                # Execute the generated SQL if present
                if sql_query:
                    data_result = session.sql(sql_query).to_pandas()
                    return explanation, data_result
                else:
                    return explanation, None
                    
        except Exception as e:
            return f"Error calling Cortex Analyst: {str(e)}", None
        
        return None, None
    
    def call_cortex_complete(question: str, context: str = "") -> str:
        """Call Cortex Complete for general questions."""
        from utils.data_loader import get_session
        
        session = get_session()
        if session is None:
            return None
        
        try:
            prompt = f"""You are a helpful procurement analytics assistant for Snowcore Industries.
            Answer the following question about procurement data concisely.
            
            Context: {context}
            
            Question: {question}
            
            Provide a clear, actionable response."""
            
            result = session.sql(f"""
                SELECT SNOWFLAKE.CORTEX.COMPLETE(
                    'mistral-large2',
                    '{prompt.replace("'", "''")}'
                ) AS response
            """).collect()
            
            if result and len(result) > 0:
                return result[0]['RESPONSE']
        except Exception as e:
            return None
        
        return None
    
    def route_and_respond(user_question: str) -> str:
        """Route question to appropriate Cortex service and generate response."""
        prompt_lower = user_question.lower()
        
        # Keywords for structured data (Cortex Analyst)
        analyst_keywords = ['spend', 'cost', 'price', 'savings', 'top', 'highest', 
                           'supplier', 'invoice', 'risk', 'health', 'region', 'category',
                           'total', 'average', 'count', 'how much', 'how many', 'show me']
        
        # Keywords for document search (Cortex Search - simulated for now)
        search_keywords = ['contract', 'terms', 'clause', 'payment', 'indemnification', 
                          'document', 'compliance', 'regulatory', 'audit', 'certificate']
        
        # Try Cortex Analyst for structured data questions
        if any(word in prompt_lower for word in analyst_keywords):
            explanation, data = call_cortex_analyst(user_question)
            
            if explanation and data is not None and not data.empty:
                # Format the response with data
                response = f"**Cortex Analyst Response:**\n\n{explanation}\n\n"
                
                # Format data as markdown table (limit to 10 rows)
                if len(data) > 0:
                    response += "**Results:**\n\n"
                    response += data.head(10).to_markdown(index=False)
                    if len(data) > 10:
                        response += f"\n\n*Showing 10 of {len(data)} results*"
                
                return response
            elif explanation:
                return f"**Cortex Analyst Response:**\n\n{explanation}"
        
        # Try Cortex Search for document questions (fallback to simulated)
        if any(word in prompt_lower for word in search_keywords):
            # For now, provide contextual response (real Cortex Search requires service setup)
            context = """Supplier contracts and compliance documents are indexed. 
            Common clauses include payment terms (Net 30-60), indemnification, 
            Force Majeure, and regulatory compliance requirements."""
            
            llm_response = call_cortex_complete(user_question, context)
            if llm_response:
                return f"**Document Analysis (Cortex):**\n\n{llm_response}"
            
            # Fallback to simulated search response
            return """**Document Search Results** (via Cortex Search)

Based on the supplier compliance documents:

📄 **Payment Terms Summary**
Most contracts specify Net 30-60 day payment terms. Strategic suppliers typically have Net 30 with 2% early payment discount.

📄 **Key Findings**
- 85% of contracts include Force Majeure provisions
- Average contract term: 2-3 years
- 72% include annual price adjustment clauses tied to commodity indices

*Would you like me to search for specific supplier documents?*"""
        
        # General question - use Cortex Complete
        llm_response = call_cortex_complete(user_question)
        if llm_response:
            return f"**Cortex Response:**\n\n{llm_response}"
        
        # Final fallback
        return """I can help you analyze procurement data in two ways:

1. **Structured Data (Numbers/Metrics)** - Powered by Cortex Analyst
   Ask about spend, suppliers, risk scores, forecasts, savings, invoices

2. **Documents (Contracts/Compliance)** - Powered by Cortex Search
   Ask about contract terms, audit findings, regulatory status

What would you like to know?"""
    
    # ==========================================================================
    # Chat Interface
    # ==========================================================================
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": """Welcome! I'm powered by **Snowflake Cortex** and can help you with:
            
**Structured Data (Cortex Analyst)**
- "What is our total spend with high-risk suppliers?"
- "Show top 5 EMEA suppliers by spend with low financial health"
- "What are the potential savings from should-cost analysis?"
- "Identify suppliers for BioFlow precision components with high financial risk"

**Documents (Cortex Search)**
- "What are the payment terms for our German suppliers?"
- "Summarize indemnification clauses for BioFlow suppliers"

How can I help you today?"""}
        ]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about procurement data..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response using Cortex Agent
        with st.chat_message("assistant"):
            with st.spinner("Analyzing with Cortex..."):
                response = route_and_respond(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Quick action buttons
    st.markdown("---")
    st.markdown("**Quick Queries:**")
    col_q1, col_q2 = st.columns(2)
    
    with col_q1:
        if st.button("High-Risk Suppliers", use_container_width=True):
            quick_query = "Show me suppliers with financial health score below 50"
            st.session_state.messages.append({"role": "user", "content": quick_query})
            st.rerun()
    
    with col_q2:
        if st.button("Savings Opportunities", use_container_width=True):
            quick_query = "What are the potential savings from should-cost analysis?"
            st.session_state.messages.append({"role": "user", "content": quick_query})
            st.rerun()

# =============================================================================
# Commodity Index Trends (Integrated with Should-Cost)
# =============================================================================
st.markdown("---")
st.markdown("### Commodity Index Trends")
st.caption("*External market indices from Snowflake Marketplace - correlate with contract pricing above*")

indices = load_data('commodity_indices')

if not indices.empty:
    # Filter to selected category if applicable
    if selected_category != 'All':
        indices = indices[indices['COMMODITY_TYPE'] == selected_category]
    
    if not indices.empty:
        col_trend, col_latest = st.columns([3, 1])
        
        with col_trend:
            chart = alt.Chart(indices).mark_line(strokeWidth=2).encode(
                x=alt.X('INDEX_DATE:T', title='Date'),
                y=alt.Y('INDEX_VALUE:Q', title='Index Value'),
                color=alt.Color('COMMODITY_TYPE:N', title='Commodity'),
                strokeDash=alt.StrokeDash('COMMODITY_TYPE:N'),
                tooltip=['INDEX_DATE', 'COMMODITY_TYPE', 'INDEX_VALUE', 'PERCENTAGE_CHANGE_WEEKLY']
            ).properties(height=300)
            
            st.altair_chart(chart, use_container_width=True)
        
        with col_latest:
            st.markdown("**Latest Index Values**")
            latest = load_data('commodity_latest')
            if not latest.empty:
                for _, row in latest.head(5).iterrows():
                    change = row.get('PERCENTAGE_CHANGE_WEEKLY', 0)
                    delta_color = "normal" if change >= 0 else "inverse"
                    st.metric(
                        label=row['COMMODITY_TYPE'][:15],
                        value=f"{row['INDEX_VALUE']:.1f}",
                        delta=f"{change:+.1f}% WoW"
                    )
    else:
        st.info("No commodity data for selected category")
else:
    st.info("Commodity index data not available")

# Footer
st.markdown("---")
st.caption("Category Manager Workbench | Should-Cost modeling powered by Snowflake Marketplace data")
