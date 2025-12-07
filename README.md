



<h2>Access Our Datasets & Samples</h2>

To avoid having to run all of our data collection, sampling and some of the cleaning code, you can access our datasets in GCS. gcloud is installed as a dependency in our
repo, and the datasets can be accessed using the download_dataset_samples.py.

- Place the service account key in the project root dir.
- Update the keyname variable with the actual name of the key.
- Run the script and it will download the files to the appropriate place.

Note: Access is limited to the bucket, and the GCP project will be deleted after the final grades have posted. Reach out to Jacob P at jperius@umich.edu or via Slack if there are any issues!