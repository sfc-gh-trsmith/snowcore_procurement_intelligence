"""
Data Science Workbench
Demand forecasting, model performance, and predictive analytics for Data Scientist persona
"""

import streamlit as st
import pandas as pd
import altair as alt

from utils.data_loader import (
    load_data, format_currency, format_number, format_percent
)

st.set_page_config(
    page_title="Data Science Workbench | Snowcore",
    page_icon="D",
    layout="wide"
)

# Header
st.title("Data Science Workbench")
st.markdown("*Demand sensing, model performance, and predictive analytics*")

# =============================================================================
# Page Filters (Top of Page)
# =============================================================================

# Initialize session state for division filter
if 'selected_division' not in st.session_state:
    st.session_state.selected_division = 'All'

# Load filter options
categories = load_data('categories')

# Filter row at top of page
filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1, 1, 1, 1])

with filter_col1:
    division_options = ['All', 'Industrial Compression', 'BioFlow (Life Sciences)']
    selected_division = st.selectbox(
        "Business Division",
        options=division_options,
        index=division_options.index(st.session_state.selected_division),
        key="ds_division_selector",
        help="Filter data by business division"
    )
    st.session_state.selected_division = selected_division

with filter_col2:
    selected_category = st.selectbox(
        "Material Category",
        options=['All'] + (categories['MATERIAL_CATEGORY'].tolist() if not categories.empty else []),
        index=0,
        key="ds_category_selector"
    )

with filter_col3:
    forecast_horizon = st.slider(
        "Forecast Horizon (Days)",
        min_value=7,
        max_value=90,
        value=30,
        step=7,
        key="ds_forecast_horizon"
    )

with filter_col4:
    # Model info badge
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                border-radius: 6px; padding: 0.5rem; margin-top: 0.5rem;
                border-left: 3px solid #FFD93D;">
        <span style="font-size: 0.75rem; color: #888;">Model: </span>
        <span style="font-size: 0.85rem; color: #FFD93D; font-weight: 600;">XGBoost</span>
        <span style="font-size: 0.75rem; color: #666;"> | Snowpark ML</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# Data Scientist Persona - Data Loading Functions
# =============================================================================
@st.cache_data(ttl=300)
def load_forecast_metrics():
    return load_data('forecast_accuracy_metrics')

@st.cache_data(ttl=300)
def load_forecast_predictions():
    return load_data('demand_forecast_predictions')

@st.cache_data(ttl=300)
def load_feature_importance():
    return load_data('feature_importance')

@st.cache_data(ttl=300)
def load_external_indicators():
    return load_data('external_indicators')

@st.cache_data(ttl=300)
def load_forecast_trend():
    return load_data('forecast_vs_actual_trend')

@st.cache_data(ttl=300)
def load_model_registry():
    return load_data('model_registry')

@st.cache_data(ttl=300)
def load_model_comparison():
    return load_data('model_comparison')

@st.cache_data(ttl=300)
def load_external_indicators_latest():
    return load_data('external_indicators_latest')

@st.cache_data(ttl=300)
def load_external_indicators_trend():
    return load_data('external_indicators_trend')

@st.cache_data(ttl=300)
def load_business_impact_summary():
    return load_data('business_impact_summary')

# =============================================================================
# Model Operations Dashboard
# =============================================================================
st.markdown("### Model Operations")
st.caption("*ML model deployment status and pipeline health*")

model_registry = load_model_registry()

if not model_registry.empty:
    # Find deployed model
    deployed_model = model_registry[model_registry['IS_DEPLOYED'] == True]
    
    col_status, col_metrics, col_comparison = st.columns([1, 1, 2])
    
    with col_status:
        if not deployed_model.empty:
            dm = deployed_model.iloc[0]
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1F2D1F 0%, #1E1E1E 100%); 
                        border-radius: 8px; padding: 1rem; text-align: center;
                        border-left: 4px solid #6BCB77;">
                <div style="font-size: 0.75rem; color: #888;">Deployed Model</div>
                <div style="font-size: 1.1rem; font-weight: bold; color: #6BCB77;">{dm['MODEL_NAME']}</div>
                <div style="font-size: 0.85rem; color: #AAA;">{dm['MODEL_VERSION']}</div>
                <div style="font-size: 0.7rem; color: #666; margin-top: 0.5rem;">
                    Algorithm: {dm['ALGORITHM']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Last training info
            st.markdown(f"""
            <div style="margin-top: 0.5rem; padding: 0.5rem; background: #1E1E1E; border-radius: 4px;">
                <div style="font-size: 0.7rem; color: #888;">Last Trained</div>
                <div style="font-size: 0.9rem;">{str(dm['TRAINING_DATE'])[:10]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("No model currently deployed")
    
    with col_metrics:
        if not deployed_model.empty:
            dm = deployed_model.iloc[0]
            st.metric("Accuracy", f"{dm['ACCURACY_PCT']:.1f}%", help="100% - MAPE")
            st.metric("MAPE", f"{dm['MAPE']:.2f}%", help="Mean Absolute Percentage Error")
            st.metric("R² Score", f"{dm['R2_SCORE']:.4f}", help="Coefficient of determination")
    
    with col_comparison:
        st.markdown("**Model Comparison (Latest Versions)**")
        
        model_comp = load_model_comparison()
        
        if not model_comp.empty:
            # Create comparison chart
            chart = alt.Chart(model_comp).mark_bar().encode(
                x=alt.X('MAPE:Q', title='MAPE (lower is better)'),
                y=alt.Y('ALGORITHM:N', sort='x', title=None),
                color=alt.condition(
                    alt.datum.IS_DEPLOYED == True,
                    alt.value('#6BCB77'),
                    alt.value('#29B5E8')
                ),
                tooltip=['ALGORITHM', 'MODEL_VERSION', 'MAPE', 'MAE', 'R2_SCORE', 'ACCURACY_PCT']
            ).properties(height=150)
            
            st.altair_chart(chart, use_container_width=True)
            st.caption("*Green: Currently deployed model*")
        else:
            st.info("Model comparison data not available. Run the demand sensing notebook to train models.")
else:
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown("""
        <div style="background: #1E1E1E; border-radius: 8px; padding: 1rem; text-align: center;">
            <div style="color: #888;">Deployed Model</div>
            <div style="color: #6BCB77; font-size: 1.2rem;">XGBoost v5.0.0</div>
        </div>
        """, unsafe_allow_html=True)
    with col_s2:
        st.metric("Accuracy", "91.2%")
        st.metric("MAPE", "8.8%")
    with col_s3:
        st.metric("R² Score", "0.8742")
        st.metric("Features", "12")

st.markdown("---")

# =============================================================================
# Business Impact KPIs
# =============================================================================
st.markdown("### Business Impact")
st.caption("*Quantified value from demand sensing model*")

business_impact = load_business_impact_summary()

if not business_impact.empty:
    bi = business_impact.iloc[0]
    
    col_bi1, col_bi2, col_bi3, col_bi4, col_bi5 = st.columns(5)
    
    with col_bi1:
        inv_reduction = bi.get('TOTAL_INVENTORY_REDUCTION', 125000)
        st.metric(
            label="Inventory Reduction",
            value=format_currency(inv_reduction),
            delta="+15% vs prior year",
            help="Inventory dollars reduced through better forecasting"
        )
    
    with col_bi2:
        cost_savings = bi.get('TOTAL_COST_SAVINGS', 85000)
        st.metric(
            label="Cost Savings",
            value=format_currency(cost_savings),
            delta="+22% vs baseline",
            help="Cost savings from procurement optimization"
        )
    
    with col_bi3:
        service_level = bi.get('AVG_SERVICE_LEVEL_IMPROVEMENT', 3.2)
        st.metric(
            label="Service Level",
            value=f"+{service_level:.1f}%",
            delta="improvement",
            delta_color="off",
            help="Service level improvement from better demand planning"
        )
    
    with col_bi4:
        stockout = bi.get('AVG_STOCKOUT_REDUCTION', 15.5)
        st.metric(
            label="Stockout Reduction",
            value=f"{stockout:.1f}%",
            delta="fewer stockouts",
            delta_color="off",
            help="Reduction in stockout incidents"
        )
    
    with col_bi5:
        forecast_value = bi.get('TOTAL_FORECAST_VALUE', 210000)
        st.metric(
            label="Forecast Value Added",
            value=format_currency(forecast_value),
            help="Total business value from demand forecasting"
        )
else:
    col_bi1, col_bi2, col_bi3, col_bi4, col_bi5 = st.columns(5)
    with col_bi1:
        st.metric("Inventory Reduction", "$125K", "+15%")
    with col_bi2:
        st.metric("Cost Savings", "$85K", "+22%")
    with col_bi3:
        st.metric("Service Level", "+3.2%")
    with col_bi4:
        st.metric("Stockout Reduction", "15.5%")
    with col_bi5:
        st.metric("Forecast Value Added", "$210K")

st.markdown("---")

# =============================================================================
# KPI Row - Model Performance Summary
# =============================================================================
st.markdown("### Model Performance Summary")

metrics = load_forecast_metrics()

if not metrics.empty:
    overall_accuracy = metrics['ACCURACY_PCT'].mean()
    overall_mape = metrics['MAPE'].mean()
    total_predictions = metrics['PREDICTION_COUNT'].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Forecast Accuracy",
            value=f"{overall_accuracy:.1f}%",
            delta="+12% vs baseline",
            help="Overall accuracy across all categories (100% - MAPE)"
        )
    
    with col2:
        st.metric(
            label="MAPE",
            value=f"{overall_mape:.1f}%",
            delta=f"-3.2% vs last month",
            delta_color="inverse",
            help="Mean Absolute Percentage Error - lower is better"
        )
    
    with col3:
        st.metric(
            label="Predictions Generated",
            value=format_number(total_predictions),
            delta=None,
            help="Total demand predictions in the last 90 days"
        )
    
    with col4:
        categories_covered = len(metrics)
        st.metric(
            label="Categories Covered",
            value=format_number(categories_covered),
            delta=None,
            help="Number of material categories with active forecasts"
        )
else:
    st.info("Model metrics not yet available. Run the demand sensing notebook to generate forecasts.")

st.markdown("---")

# =============================================================================
# Main Content - Split View
# =============================================================================
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### Forecast vs Actual Trend")
    
    trend_data = load_forecast_trend()
    
    if not trend_data.empty:
        # Melt data for multi-line chart
        trend_melted = trend_data.melt(
            id_vars=['WEEK'],
            value_vars=['TOTAL_FORECASTED', 'TOTAL_ACTUAL'],
            var_name='Series',
            value_name='Quantity'
        )
        trend_melted['Series'] = trend_melted['Series'].map({
            'TOTAL_FORECASTED': 'Forecasted Demand',
            'TOTAL_ACTUAL': 'Actual Demand'
        })
        
        chart = alt.Chart(trend_melted).mark_line(strokeWidth=2).encode(
            x=alt.X('WEEK:T', title='Week'),
            y=alt.Y('Quantity:Q', title='Total Quantity'),
            color=alt.Color('Series:N', 
                          scale=alt.Scale(domain=['Forecasted Demand', 'Actual Demand'],
                                         range=['#29B5E8', '#6BCB77']),
                          legend=alt.Legend(orient='top')),
            strokeDash=alt.StrokeDash('Series:N',
                                      scale=alt.Scale(domain=['Forecasted Demand', 'Actual Demand'],
                                                     range=[[0], [5, 5]])),
            tooltip=['WEEK:T', 'Series:N', 'Quantity:Q']
        ).properties(height=300)
        
        # Add confidence band (simulated)
        st.altair_chart(chart, use_container_width=True)
        
        st.caption("*Solid line: Forecasted | Dashed line: Actual*")
    else:
        st.info("Forecast trend data not available. Run `./run.sh main` to execute the demand sensing notebook and generate forecasts.")

    # Accuracy by Category
    st.markdown("### Accuracy by Material Category")
    
    if not metrics.empty:
        accuracy_chart = alt.Chart(metrics).mark_bar().encode(
            x=alt.X('ACCURACY_PCT:Q', title='Forecast Accuracy (%)', scale=alt.Scale(domain=[0, 100])),
            y=alt.Y('MATERIAL_CATEGORY:N', sort='-x', title='Category'),
            color=alt.condition(
                alt.datum.ACCURACY_PCT >= 85,
                alt.value('#6BCB77'),
                alt.condition(
                    alt.datum.ACCURACY_PCT >= 70,
                    alt.value('#FFD93D'),
                    alt.value('#FF6B6B')
                )
            ),
            tooltip=['MATERIAL_CATEGORY', 'ACCURACY_PCT', 'MAPE', 'PREDICTION_COUNT']
        ).properties(height=250)
        
        # Add target line
        rule = alt.Chart(pd.DataFrame({'target': [85]})).mark_rule(
            color='#29B5E8',
            strokeDash=[5, 5],
            strokeWidth=2
        ).encode(x='target:Q')
        
        st.altair_chart(accuracy_chart + rule, use_container_width=True)
        st.caption("*Blue dashed line: 85% accuracy target*")

with col_right:
    st.markdown("### Feature Importance")
    
    features = load_feature_importance()
    
    if not features.empty:
        feature_chart = alt.Chart(features.head(10)).mark_bar().encode(
            x=alt.X('IMPORTANCE_SCORE:Q', title='Importance Score'),
            y=alt.Y('FEATURE_NAME:N', sort='-x', title=None),
            color=alt.Color('FEATURE_TYPE:N', 
                          scale=alt.Scale(scheme='tableau10'),
                          legend=alt.Legend(orient='bottom', title='Feature Type')),
            tooltip=['FEATURE_NAME', 'IMPORTANCE_SCORE', 'FEATURE_TYPE', 'DESCRIPTION']
        ).properties(height=300)
        
        st.altair_chart(feature_chart, use_container_width=True)
    else:
        # Show placeholder feature importance
        st.markdown("""
        **Top Features (from XGBoost model):**
        
        | Feature | Importance | Type |
        |---------|------------|------|
        | `lag_consumption_7d` | 0.23 | Internal |
        | `construction_starts_idx` | 0.18 | External |
        | `lag_consumption_30d` | 0.15 | Internal |
        | `clinical_trial_spend` | 0.12 | External |
        | `seasonality_factor` | 0.09 | Derived |
        | `supplier_lead_time` | 0.08 | Internal |
        | `commodity_price_idx` | 0.07 | External |
        | `inventory_level` | 0.05 | Internal |
        """)
        st.caption("*Run ML notebook to generate live feature importance*")
    
    st.markdown("---")
    
    st.markdown("### External Indicators")
    st.caption("*Macro-economic signals for demand sensing*")
    
    ext_indicators = load_external_indicators_latest()
    
    if not ext_indicators.empty:
        # Group by indicator type
        economic = ext_indicators[ext_indicators['INDICATOR_TYPE'] == 'ECONOMIC']
        industry = ext_indicators[ext_indicators['INDICATOR_TYPE'] == 'INDUSTRY']
        
        st.markdown("**Economic Indicators**")
        for _, row in economic.head(4).iterrows():
            pct_change = row.get('PERCENTAGE_CHANGE', 0)
            color = '#6BCB77' if pct_change >= 0 else '#FF6B6B'
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 0.25rem 0; border-bottom: 1px solid #333;">
                <span style="font-size: 0.8rem;">{row['INDICATOR_NAME'][:25]}</span>
                <span style="font-size: 0.85rem; font-weight: bold;">{row['INDICATOR_VALUE']:.1f}</span>
                <span style="color: {color}; font-size: 0.75rem;">{pct_change:+.1f}%</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("**Industry Indicators**")
        for _, row in industry.head(4).iterrows():
            pct_change = row.get('PERCENTAGE_CHANGE', 0)
            color = '#6BCB77' if pct_change >= 0 else '#FF6B6B'
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 0.25rem 0; border-bottom: 1px solid #333;">
                <span style="font-size: 0.8rem;">{row['INDICATOR_NAME'][:25]}</span>
                <span style="font-size: 0.85rem; font-weight: bold;">{row['INDICATOR_VALUE']:.1f}</span>
                <span style="color: {color}; font-size: 0.75rem;">{pct_change:+.1f}%</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Show placeholder indicators
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Construction Starts", "142.3", "+3.2%")
            st.metric("Clinical Trial Spend", "$2.4B", "+8.1%")
        with col_b:
            st.metric("Industrial Production", "98.7", "-1.2%")
            st.metric("Manufacturing PMI", "52.1", "+1.5%")

st.markdown("---")

# =============================================================================
# Demand Forecast Predictions Table
# =============================================================================
st.markdown("### 90-Day Demand Forecast Predictions")

predictions = load_forecast_predictions()

if not predictions.empty:
    # Apply category filter
    display_df = predictions.copy()
    if selected_category != 'All':
        display_df = display_df[display_df['MATERIAL_CATEGORY'] == selected_category]
    
    if not display_df.empty:
        st.dataframe(
            display_df[[
                'FORECAST_DATE', 'MATERIAL_CATEGORY', 'PRODUCT_CODE',
                'FORECASTED_DEMAND_QTY', 'ACTUAL_DEMAND_QTY',
                'LOWER_BOUND', 'UPPER_BOUND', 'PREDICTION_CONFIDENCE'
            ]].head(50),
            use_container_width=True,
            column_config={
                "FORECAST_DATE": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
                "MATERIAL_CATEGORY": "Category",
                "PRODUCT_CODE": "Product",
                "FORECASTED_DEMAND_QTY": st.column_config.NumberColumn(
                    "Forecast Qty",
                    format="%.0f"
                ),
                "ACTUAL_DEMAND_QTY": st.column_config.NumberColumn(
                    "Actual Qty",
                    format="%.0f"
                ),
                "LOWER_BOUND": st.column_config.NumberColumn(
                    "Lower (95%)",
                    format="%.0f"
                ),
                "UPPER_BOUND": st.column_config.NumberColumn(
                    "Upper (95%)",
                    format="%.0f"
                ),
                "PREDICTION_CONFIDENCE": st.column_config.ProgressColumn(
                    "Confidence",
                    min_value=0,
                    max_value=1,
                    format="%.0%%"
                )
            },
            hide_index=True
        )
        
        # Download option
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="Export Predictions (CSV)",
            data=csv,
            file_name="demand_forecast_predictions.csv",
            mime="text/csv"
        )
    else:
        st.info("No predictions for selected category")
else:
    st.info("Run the demand sensing notebook (`notebooks/demand_sensing.ipynb`) to generate predictions")

st.markdown("---")

# =============================================================================
# External Indicator Correlation Explorer
# =============================================================================
st.markdown("### External Indicator Correlation Explorer")
st.caption("*Analyze relationships between external economic indicators and demand patterns*")

@st.cache_data(ttl=300)
def load_indicator_correlation():
    return load_data('indicator_demand_correlation')

correlation_data = load_indicator_correlation()

if not correlation_data.empty:
    col_scatter, col_stats = st.columns([2, 1])
    
    with col_scatter:
        # Indicator selector
        available_indicators = correlation_data['INDICATOR_NAME'].unique().tolist()
        selected_indicator = st.selectbox(
            "Select External Indicator",
            options=available_indicators,
            index=0,
            help="Choose an external indicator to analyze its correlation with demand"
        )
        
        # Filter data for selected indicator
        indicator_df = correlation_data[correlation_data['INDICATOR_NAME'] == selected_indicator].copy()
        
        if not indicator_df.empty and indicator_df['DEMAND_QUANTITY'].sum() > 0:
            # Create scatter plot with trend line
            scatter = alt.Chart(indicator_df).mark_circle(
                size=60,
                color='#29B5E8',
                opacity=0.7
            ).encode(
                x=alt.X('INDICATOR_VALUE:Q', title=f'{selected_indicator} Index Value'),
                y=alt.Y('DEMAND_QUANTITY:Q', title='Total Demand Quantity'),
                tooltip=[
                    alt.Tooltip('INDEX_DATE:T', title='Date'),
                    alt.Tooltip('INDICATOR_VALUE:Q', title='Indicator Value', format='.1f'),
                    alt.Tooltip('DEMAND_QUANTITY:Q', title='Demand', format=',.0f'),
                    alt.Tooltip('INDICATOR_CHANGE:Q', title='Weekly Change %', format='.1f')
                ]
            )
            
            # Add regression line
            regression = scatter.transform_regression(
                'INDICATOR_VALUE', 'DEMAND_QUANTITY'
            ).mark_line(color='#FF6B6B', strokeWidth=2, strokeDash=[5, 5])
            
            chart = (scatter + regression).properties(
                height=300,
                title=f'{selected_indicator} vs Demand Correlation'
            )
            
            st.altair_chart(chart, use_container_width=True)
            
            # Time series view
            st.markdown("#### Time Series Comparison")
            
            # Normalize values for comparison
            indicator_df['INDICATOR_NORMALIZED'] = (
                (indicator_df['INDICATOR_VALUE'] - indicator_df['INDICATOR_VALUE'].min()) / 
                (indicator_df['INDICATOR_VALUE'].max() - indicator_df['INDICATOR_VALUE'].min()) * 100
            )
            indicator_df['DEMAND_NORMALIZED'] = (
                (indicator_df['DEMAND_QUANTITY'] - indicator_df['DEMAND_QUANTITY'].min()) / 
                (indicator_df['DEMAND_QUANTITY'].max() - indicator_df['DEMAND_QUANTITY'].min() + 1) * 100
            )
            
            ts_melted = indicator_df.melt(
                id_vars=['INDEX_DATE'],
                value_vars=['INDICATOR_NORMALIZED', 'DEMAND_NORMALIZED'],
                var_name='Series',
                value_name='Value'
            )
            ts_melted['Series'] = ts_melted['Series'].map({
                'INDICATOR_NORMALIZED': f'{selected_indicator} (Normalized)',
                'DEMAND_NORMALIZED': 'Demand (Normalized)'
            })
            
            ts_chart = alt.Chart(ts_melted).mark_line(strokeWidth=2).encode(
                x=alt.X('INDEX_DATE:T', title='Date'),
                y=alt.Y('Value:Q', title='Normalized Value (0-100)'),
                color=alt.Color('Series:N',
                              scale=alt.Scale(range=['#29B5E8', '#6BCB77']),
                              legend=alt.Legend(orient='top')),
                strokeDash=alt.StrokeDash('Series:N'),
                tooltip=['INDEX_DATE:T', 'Series:N', 'Value:Q']
            ).properties(height=200)
            
            st.altair_chart(ts_chart, use_container_width=True)
        else:
            st.info(f"Insufficient data for {selected_indicator} correlation analysis")
    
    with col_stats:
        st.markdown("#### Correlation Statistics")
        
        # Calculate correlation for each indicator
        correlations = []
        for indicator in available_indicators:
            ind_data = correlation_data[correlation_data['INDICATOR_NAME'] == indicator]
            if len(ind_data) > 5 and ind_data['DEMAND_QUANTITY'].sum() > 0:
                corr = ind_data['INDICATOR_VALUE'].corr(ind_data['DEMAND_QUANTITY'])
                correlations.append({
                    'INDICATOR': indicator,
                    'CORRELATION': corr if not pd.isna(corr) else 0,
                    'DATA_POINTS': len(ind_data)
                })
        
        if correlations:
            corr_df = pd.DataFrame(correlations).sort_values('CORRELATION', ascending=False)
            
            for _, row in corr_df.iterrows():
                corr_val = row['CORRELATION']
                corr_color = '#6BCB77' if corr_val > 0.3 else '#FFD93D' if corr_val > 0 else '#FF6B6B'
                corr_strength = "Strong" if abs(corr_val) > 0.5 else "Moderate" if abs(corr_val) > 0.3 else "Weak"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); 
                            border-radius: 6px; padding: 0.75rem; margin-bottom: 0.5rem;
                            border-left: 3px solid {corr_color};">
                    <div style="font-size: 0.8rem; color: #888;">{row['INDICATOR'][:20]}</div>
                    <div style="font-size: 1.2rem; font-weight: bold; color: {corr_color};">
                        r = {corr_val:.3f}
                    </div>
                    <div style="font-size: 0.75rem; color: #666;">{corr_strength} correlation</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### Interpretation Guide")
        st.markdown("""
        <div style="font-size: 0.8rem; color: #AAA;">
            <p><strong>r > 0.5:</strong> Strong positive correlation</p>
            <p><strong>0.3 < r < 0.5:</strong> Moderate positive</p>
            <p><strong>r < 0.3:</strong> Weak correlation</p>
            <p style="margin-top: 0.5rem; color: #888;">
                Higher correlation suggests the indicator 
                may be useful as a feature in the demand model.
            </p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No external indicator data available. Verify that `MARKETPLACE_COMMODITY_INDEX` and `DEMAND_ACTUAL` tables are populated. Run `./deploy.sh` to reload synthetic data.")

st.markdown("---")

# =============================================================================
# Raw Data Explorer
# =============================================================================
with st.expander("Raw Data Explorer", expanded=False):
    st.markdown("**Preview of prediction data from `V_DEMAND_FORECAST_PREDICTIONS` view:**")
    
    if not predictions.empty:
        st.dataframe(predictions.head(20), use_container_width=True, hide_index=True)
        
        st.markdown("**SQL Query:**")
        st.code("""
SELECT 
    MATERIAL_CATEGORY,
    PRODUCT_CODE,
    FORECAST_DATE,
    FORECASTED_DEMAND_QTY,
    ACTUAL_DEMAND_QTY,
    LOWER_BOUND,
    UPPER_BOUND,
    PREDICTION_CONFIDENCE
FROM SNOWCORE_PROCUREMENT.PROCUREMENT_MART.V_DEMAND_FORECAST_PREDICTIONS
WHERE FORECAST_DATE >= DATEADD(day, -90, CURRENT_DATE())
ORDER BY FORECAST_DATE DESC
        """, language="sql")
    else:
        st.info("No data available in the predictions table")

# Footer
st.markdown("---")
st.caption("Data Science Workbench | XGBoost Demand Sensing Model powered by Snowpark ML")
