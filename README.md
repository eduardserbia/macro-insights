Modern Data Platform for Economic Analytics (2010–2025)

⸻

📊 Architecture Diagrams (2025)

Presentation — Full Stack
Presentation — Data Flow
Technical — Architecture & Environments
Technical — CI/CD Reference

⸻

🗂️ DBT Project Structure

Seeds (source data):
	•	seeds/gdp.csv — base GDP dataset (2010–2025)

Staging layer (data cleaning and preparation):
	•	models/staging/stg_gdp.sql — cleans and prepares GDP data
	•	models/staging/stg_hello.sql — example staging model
	•	models/staging/schema.yml — tests and documentation for staging models

Marts layer (fact models and analytics):
	•	models/marts/fct_gdp_yoy.sql — calculates year-over-year GDP growth
	•	models/marts/fct_hello_daily.sql — demo fact table
	•	models/marts/schema.yml — tests and documentation for marts models

⸻

🔄 Data Flow
	1.	Raw GDP data is loaded from seeds/gdp.csv.
	2.	The Staging layer (stg_gdp) cleans, transforms, and normalizes the data.
	3.	The Marts layer (fct_gdp_yoy) calculates year-over-year growth metrics.
	4.	Results are available in ClickHouse Cloud and ready for BI visualization or downstream analytics.

⸻

⚙️ CI/CD Process
	•	GitHub Actions automatically rebuilds architecture diagrams whenever Python scripts change.
	•	dbt parses and validates models on every push.
	•	The manifest.json and other build artifacts are uploaded as CI outputs.
	•	This ensures that documentation, models, and data pipelines remain synchronized with the latest codebase.

⸻

🚀 Next Steps
	•	📚 Enable automatic publishing of dbt HTML documentation using GitHub Pages.
	•	☁️ Integrate AWS S3 for storing raw and historical datasets.
	•	📈 Expand marts with additional macroeconomic indicators and data sources.

⸻

🛠️ How to Run Locally

Follow these steps to set up and run the project locally on your machine:

1. Clone the repository
git clone https://github.com/eduardserbia/macro-insights.git
cd macro-insights

2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

3. Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

4. Install dbt and ClickHouse adapter
pip install dbt-core dbt-clickhouse

5. Run dbt commands
cd dbt
dbt deps          # install dependencies
dbt seed          # load seed data (gdp.csv)
dbt run           # execute all models
dbt test          # run data tests

6. Generate diagrams
python make_arch_diagrams.py

Generated diagrams will be available in the out/ folder.
⸻

💡 Macro Insights is a minimal viable product (MVP) of a modern macroeconomic data analytics platform — combining ClickHouse, dbt, CI/CD, and architectural visualization in a single repository.

A modern end-to-end data platform for macroeconomic analytics, combining dbt, ClickHouse, CI/CD, and visual data architecture.

