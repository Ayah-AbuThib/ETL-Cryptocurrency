# 💰Crypto ETL Pipeline 

This project demonstrates a simple ETL (Extract, Transform, Load) pipeline using Apache Airflow to fetch, process, and store cryptocurrency data. Specifically, it pulls Bitcoin data from the CoinGecko API and loads the transformed data into a PostgreSQL database.

## Project Structure 📂
- **🗂 dags/ETL-Cryptocurrency.py**: Main DAG defining the ETL process.
- **🐳 Dockerfile**: Configuration for Astro runtime Docker image.
- **📄 requirements.txt**: Python dependencies.
- **🐳 docker-compose.yml**: Defines Docker services for local Airflow.
- **🌀 airflow_settings.yaml**: Configures Airflow connections and variables.

## Features ⚙️
- **🔍 Extract**: Fetch Bitcoin data from the CoinGecko API.
- **🔄 Transform**: Process and structure the data for storage.
- **📥 Load**: Insert the transformed data into a 🐘PostgreSQL database.

## Setup and Run Locally 🛠️
1. Clone the repository. 
2. Install dependencies with `pip install -r requirements.txt`.
3. Start Airflow locally:
   ```bash
   astro dev start
   ```
4. Access the Airflow UI at [http://localhost:8080](http://localhost:8080), using `admin` for both the username and password. 🔑

