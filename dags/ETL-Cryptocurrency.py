from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago

# Cryptocurrency (Bitcoin) example - using CoinGecko API
CRYPTOCURRENCY_ID = 'bitcoin'  # Bitcoin as an example
POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'coin_gecko_api'

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}

# DAG definition
with DAG(dag_id='crypto_etl_pipeline',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    @ task()
    def extract_crypto_data():
        """Extract cryptocurrency data from CoinGecko API using Airflow Connection."""
        
        # Use HTTP Hook to get connection details from Airflow connection
        http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')

        # Build the API endpoint for CoinGecko to fetch Bitcoin data
        endpoint = f'/api/v3/simple/price?ids={CRYPTOCURRENCY_ID}&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true'

        # Make the request via the HTTP Hook
        response = http_hook.run(endpoint)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch cryptocurrency data: {response.status_code}")
    
    @task()
    def transform_crypto_data(crypto_data):
        """Transform the extracted cryptocurrency data."""
        crypto_info = crypto_data[CRYPTOCURRENCY_ID]
        transformed_data = {
            'crypto_id': CRYPTOCURRENCY_ID,
            'price_usd': crypto_info['usd'],
            'market_cap_usd': crypto_info['usd_market_cap'],
            'volume_24h_usd': crypto_info['usd_24h_vol'],
        }
        return transformed_data
    
    @task()
    def load_crypto_data(transformed_data):
        """Load transformed cryptocurrency data into PostgreSQL."""
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS crypto_data (
            crypto_id VARCHAR,
            price_usd FLOAT,
            market_cap_usd FLOAT,
            volume_24h_usd FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Insert transformed data into the table
        cursor.execute("""
        INSERT INTO crypto_data (crypto_id, price_usd, market_cap_usd, volume_24h_usd)
        VALUES (%s, %s, %s, %s)
        """, (
            transformed_data['crypto_id'],
            transformed_data['price_usd'],
            transformed_data['market_cap_usd'],
            transformed_data['volume_24h_usd']
        ))

        conn.commit()
        cursor.close()

    # DAG Workflow - ETL Pipeline
    crypto_data = extract_crypto_data()
    transformed_data = transform_crypto_data(crypto_data)
    load_crypto_data(transformed_data)