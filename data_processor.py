import pandas as pd
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
 
ZONE_LOOKUP_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"
 
DATA_FOLDER = "sample_data"
#LOCAL_PATH = "sample_data/yellow_tripdata_last12m"
 
 
def load_zone_lookup():
    return pd.read_csv(ZONE_LOOKUP_URL)
 
 
def generate_month_urls(months=12):
 
    urls = []
 
    current = datetime.now() -relativedelta(months=2)
 
    for i in range(months):
 
        dt = current - relativedelta(months=i)
 
        year = dt.year
        month = str(dt.month).zfill(2)
 
        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month}.parquet"
 
        urls.append(url)
 
    return urls
 
 
def download_and_load_data():
 
    os.makedirs(DATA_FOLDER, exist_ok=True)
 
    all_dfs = []
 
    urls = generate_month_urls(12)
 
    for url in urls:
 
        file_name = url.split("/")[-1]
        local_path = os.path.join(DATA_FOLDER, file_name)
 
        try:
 
            if not os.path.exists(local_path):
 
                print(f"Downloading {file_name}...")
 
                df = pd.read_parquet(url)
 
                # Sample for performance
                df = df.sample(n=min(10000, len(df)), random_state=42)
 
                df.to_parquet(local_path)
 
            df = pd.read_parquet(local_path)
 
            all_dfs.append(df)
 
        except Exception as e:
 
            print(f"Skipping {file_name}: {e}")
 
    final_df = pd.concat(all_dfs, ignore_index=True)
 
    return final_df
 
 
def load_data():
 
    df = download_and_load_data()
 
    # Datetime conversion
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
 
    df["pickup_date"] = df["tpep_pickup_datetime"].dt.date
 
    df["pickup_hour"] = df["tpep_pickup_datetime"].dt.hour
 
    # Load zone lookup
    zone_lookup = load_zone_lookup()
 
    # Merge pickup zones
    df = df.merge(
        zone_lookup[["LocationID", "Zone"]],
        left_on="PULocationID",
        right_on="LocationID",
        how="left"
    )
 
    return df
 
def compute_kpis(df):
 
    kpis = {}
 
    # Total trips
    kpis["total_trips"] = len(df)
 
    # Average fare
    kpis["avg_fare"] = round(df["fare_amount"].mean(), 2)
 
    # Average trip distance
    kpis["avg_distance"] = round(df["trip_distance"].mean(), 2)
 
    # Most popular pickup zone
    top_zones = (
    df["Zone"]
    .value_counts()
    .head(10)
    .reset_index()
    ) 
    top_zones.columns = ["Zone", "trip_count"]
    top_zones = top_zones.sort_values(
        by="trip_count",
        ascending=False
    )
 
    kpis["top_zones"] = top_zones
 
    # Trips by date
    daily_trips = (
        df.groupby("pickup_date")
        .size()
        .reset_index(name="trip_count")
    )
 
    kpis["daily_trips"] = daily_trips
    
    # Trips by hour
    trips_by_hour = (
        df.groupby("pickup_hour")
        .size()
        .reset_index(name="trip_count")
    )
    
    kpis["trips_by_hour"] = trips_by_hour
 
 
    return kpis


if __name__=="__main__":
    df=load_data()
    print(df.head())
    print(df.shape)
    print(df.info(memory_usage="deep"))