from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task  ## ADDED THIS IMPORT TO FIX NAMEERROR
from airflow.utils.dates import days_ago
import json

## define DAG
with DAG(
    dag_id = 'nasa_apod_postgres',
    start_date=days_ago(1),
    schedule='@daily',
    catchup=False,
) as dag:
    
    ## step 1: Create the table if it does not exists
    @task
    def create_table():
        ## initialize the Postgreshook
        postgres_hook=PostgresHook(postgres_conn_id="my_postgres_connection")
        
        ## sql query to create the table
        create_table_query="""
        CREATE TABLE IF NOT EXISTS apod_data(
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        );
        """
        
        ## execute this table createion query
        postgres_hook.run(create_table_query)
    
    ## step 2: Extract the NASA API(APOD) - Astronomy Picture Of The Day[Extract pipeline]
    ## here is the API - https://api.nasa.gov/planetary/apod?api_key=E9fd77a4v5uxOJFAU7eTF47vMThmv8YxP7taW9Sp 
    
    extract_apod = HttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',  # Connection ID defined in Airflow for NASA API
        endpoint='planetary/apod', # NASA API endpoint for Astronomy Picture of the Day
        method='GET', 
        # Use Jinja templating to securely pull the API key from the connection's extra field
        data={'api_key': '{{ conn.nasa_api.extra_dejson.api_key }}'},   
        response_filter=lambda response: response.json(), 
    )

    ## step 3: transform the data(pick the information that i need to save) 
    @task
    def transform_apod_data(response: dict):
        """
        Transform raw APOD API response
        """
        transformed_data = {
            "title": response.get("title", ""),
            "explanation": response.get("explanation", ""),
            "url": response.get("url", ""),
            "date": response.get("date", ""),
            "media_type": response.get("media_type", "")
        }

        return transformed_data

    ## step 4: Load the data into Postgress Sql
    @task
    def load_data_to_postgres(apod_data):
        postgres_hook=PostgresHook(postgres_conn_id="my_postgres_connection")
        
        # define the insert the data into table
        # I am using %s placeholders to prevent SQL Injection. we have another option is drectly fill the column title
        # This ensures that user input is treated as data, not as a command.
        insert_query = """
            INSERT INTO apod_data(title, explanation, url, date, media_type)
            VALUES (%s, %s, %s, %s, %s); 
        """
        
        ## execute the sql query
        postgres_hook.run(insert_query, parameters=(
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type'],
        ))

    ## step 6: Define dependencies 
    # 1. Create the table first
    create_table_task = create_table()
    
    # 2. Extract after table is ready
    create_table_task >> extract_apod
    api_response = extract_apod.output
    
    #Transform
    transformed_data = transform_apod_data(api_response)
    #Load
    load_data_to_postgres(transformed_data)
