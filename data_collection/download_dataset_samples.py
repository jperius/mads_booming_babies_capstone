
if __name__ == "__main__":
    from google.cloud import storage
    from pathlib import Path

    key_name = "service_account.json"

    BASE_DIR = Path().resolve().parent

    try:
        client = storage.Client.from_service_account_json(
            Path(BASE_DIR / key_name))
    except Exception:
        print(
            'Failed to initialize the storage client using the service account key!')

    bucket = client.bucket("capstone-datasets-25")

    try:
        blob = bucket.blob("natality_7yr_test_data.csv")
        blob.download_to_filename(
            Path(BASE_DIR / "data_main" / "natality_7yr_test_data.csv"))
    except Exception:
        print('natality_7yr_test_data.csv failed to download!')

    try:
        blob2 = bucket.blob("natality_aligned_10pct_sample.csv")
        blob2.download_to_filename(
            Path(BASE_DIR / "data_main" / "natality_aligned_10pct_sample.csv"))
    except Exception:
        print('natality_aligned_10pct_sample.csv failed to download!')
