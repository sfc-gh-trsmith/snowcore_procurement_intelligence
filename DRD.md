# Demo Requirements Document (DRD): Snowcore Industries Intelligent Sourcing Hub

GITHUB REPO NAME: `snowcore_procurement_intelligence` GITHUB REPO DESCRIPTION: A GenAI-powered procurement optimization platform integrating rationalized multi-ERP spend data with Snowflake Marketplace intelligence (Risk, Commodities, ESG) to drive predictive sourcing and "Should-Cost" modeling.

## 1\. Strategic Overview

* **Problem Statement:** Snowcore Industries has expanded rapidly through M\&A, resulting in a fragmented landscape of 50+ legacy ERPs across its Industrial Compression and newly acquired "BioFlow" (Life Sciences) divisions. This data sprawl creates silos that obscure global spend visibility, making it difficult to manage supply chain disruptions, validate "medical-grade" supplier premiums, and optimize costs against market indices.  
    
* **Target Business Goals (KPIs):**  
    
* **Material Cost Reduction:** Reduce purchase price variance (PPV) by 5-8% through "Should-Cost" modeling against market indices.  
    
* **Risk Mitigation:** Increase Supplier Risk Coverage by 100% using external financial and geopolitical data.  
    
* **Inventory Optimization:** Improve Demand Forecast Accuracy by 12% by incorporating external demand drivers (construction starts, pharma R\&D trends).  
    
* **The "Wow" Moment:** A user asks Cortex Analyst, "Identify suppliers for BioFlow precision components with high financial risk scores," and the system instantly returns a list, calculates the revenue at risk, and proactively recommends alternative validated suppliers from the Snowflake Marketplace.

## 2\. User Personas & Stories

*Demonstrating platform breadth from C-Suite to Shop Floor.*

| Persona Level | Role Title | Key User Story (Demo Flow) |
| :---- | :---- | :---- |
| **Strategic** | **Chief Procurement Officer (CPO)** | "As a CPO, I want to see a consolidated view of global spend across all 50+ ERPs, normalized to verify we are meeting our ESG sustainability targets." |
| **Operational** | **Category Manager (Metals)** | "As a Category Manager, I want to compare our contracted alloy rates against real-time global spot indices to identify specific invoices where we overpaid." |
| **Technical** | **Supply Chain Data Scientist** | "As a Data Scientist, I want to train a demand sensing model in Snowpark using internal consumption history and external macro-economic indicators to predict Q3 raw material needs." |

## 3\. Data Architecture & Snowpark ML (Backend)

* **Data Architecture Layers:**  
    
* `RAW`: Ingestion of legacy ERP dumps (SAP, Oracle, Proprietary) and Snowflake Marketplace feeds.  
    
* `ATOMIC`: Normalized Enterprise Data Model (Dynamic Tables used here for continuous transformation).  
    
* `PROCUREMENT_MART`: Aggregated views for Streamlit consumption.  
    
* **Structured Data (Inferred Schema):**  
    
* `PO_HISTORY_GLOBAL`: Consolidated purchase orders (columns: `po_id`, `supplier_id`, `material_sku`, `unit_price`, `erp_source_system`, `consumption_date`).  
    
* `MARKETPLACE_INDICATORS`: External features (columns: `date`, `industrial_construction_index`, `global_alloy_price`, `supplier_financial_health_score`, `geopolitical_risk_level`).  
    
* **Unstructured Data (Tribal Knowledge):**  
    
* **Source Material:** Supplier Contracts (PDFs), Regulatory Compliance Letters (BioFlow Division), Supplier Audit Reports, Logistics Email Logs.  
    
* **Purpose:** Used to answer qualitative questions regarding Force Majeure clauses or regulatory compliance history via Cortex Search.  
    
* **ML Notebook Specification:**  
    
* **Objective:** Demand Sensing & Predictive Procurement.  
    
* **Target Variable:** `forecasted_material_demand_qty`  
    
* **Algorithm Choice:** XGBoost Regressor (utilizing `Snowpark ML` libraries).  
    
* **Feature Engineering:** Lag features on internal consumption \+ External features (Construction Starts, Clinical Trial Spend).  
    
* **Inference Output:** Predictions written to table `DEMAND_FORECAST_PREDICTIONS`.

## 4\. Cortex Intelligence Specifications

### Cortex Analyst (Structured Data / SQL)

* **Semantic Model Scope:**  
    
* **Measures:** `Total_Spend_Amount`, `Purchase_Price_Variance`, `On_Time_Delivery_Rate`, `Carbon_Footprint_MT`.  
    
* **Dimensions:** `Supplier_Name`, `Material_Category` (e.g., Thermal Systems vs. Bio-Robotics), `Region`, `Risk_Level`.  
    
* **Golden Query (Verification):**  
    
* *User Prompt:* "Show me the top 5 suppliers by spend in the EMEA region who have a financial health score below 50."  
    
* *Expected SQL Operation:* `SELECT Supplier_Name, SUM(Total_Spend_Amount) FROM PROCUREMENT_MART WHERE Region = 'EMEA' AND Financial_Health_Score < 50 GROUP BY Supplier_Name ORDER BY 2 DESC LIMIT 5`

### Cortex Search (Unstructured Data / RAG)

* **Service Name:** `SUPPLIER_COMPLIANCE_SEARCH_SERVICE`  
    
* **Indexing Strategy:**  
    
* **Document Attribute:** Indexing by `supplier_id` and `document_type` (Contract, Audit, Regulatory Finding).  
    
* **Sample RAG Prompt:** "Summarize the indemnification clauses for our primary BioFlow reagent supplier and check if they have any recent regulatory warning letters regarding contamination."

## 5\. Streamlit Application UX/UI

* **Layout Strategy:**  
    
* **Page 1 (Executive Control Tower):** A "Command Center" view showing a global map of suppliers. Color-coded dots represent risk levels (Red \= High Risk). Key metrics: Total Spend, Risk Exposure ($), ESG Score.  
    
* **Page 2 (Category Manager Workbench):** Split view. Left side: Interactive "Should-Cost" charts (Contract Price vs. Market Index). Right side: Cortex Agent Chat interface.  
    
* **Component Logic:**  
    
* **Visualizations:** Altair multi-line chart comparing `PO_Unit_Price` vs `Market_Index_Price` over time to visualize savings opportunities.  
    
* **Chat Integration:** A unified Cortex Agent entry point. If the user asks for numbers ("How much did we spend?"), it routes to Analyst. If the user asks for text ("What are the payment terms?"), it routes to Search.

## 6\. Success Criteria

* **Technical Validator:** The Cortex Agent successfully routes a compound query ("Which suppliers are high risk and what do their contracts say about termination?") to both Analyst and Search, synthesizing the answer in \< 5 seconds.  
* **Business Validator:** The demo clearly shows how combining external Marketplace data with internal ERP data allows for a proactive "intervention" (e.g., changing a supplier before a disruption occurs), reducing time-to-insight from weeks (manual spreadsheets) to seconds.
