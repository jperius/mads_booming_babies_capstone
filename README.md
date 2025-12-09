<h1>MADS Capstone - The Booming Babies</h1>
<h3>Jacob Perius, Thomas Lucas & Sean Seddique</h3>

<h2>About</h2>

This analysis uses the National Center for Health Statistics multi-year U.S. natality dataset to develop scalable machine learning models to predict maternal morbidity from demographic, clinical, and pregnancy-specific risk factor features. 

Identification of elevated risk and potential mediators can support targeted interventions, improved decision-making, and more equitable delivery of care. To this end, our project identified two distinct goals to provide actionable insights to improve healthcare outcomes. 

The first is to identify key features that can be altered during pregnancy to reduce the risk of maternal morbidity, such as the number of pre-natal visits, medical providers, or risk mediators. This will provide insights into the types of actions that can be taken to improve healthcare outcomes. The second goal will be to identify specific demographics that are associated with higher risk of maternal morbidity. These populations can then be targeted for additional support identified in part one. 

<h2>Installing the Environment</h2>

We've used Poetry as our dependency manager / .venv. Once you clone the repo, you can run 'poetry install' in your terminal after navigating to the root dir for the repo. If you don't have Poetry installed, you can follow the instructions for your OS here: https://python-poetry.org/docs/ (or you can ask GPT / Claude).

Note: if you have trouble locating the virtual environment in Jupyter, you can explicitly create a kernel using the command below:

python -m ipykernel install --user --name=capstone --display-name “capstone”

<h2>Using py-tetrad</h2>

py-tetrad is a Python interface for the Java code that runs under the hood. Therefore, to run any code for the py-tetrad DAG-generating files, you must have Java installed. You can download it here: https://www.oracle.com/java/technologies/downloads/. However, it may be better to download via CLI using whatever system package manager you use (i.e. homebrew for Mac). You may have to run additional commands to point to the correct Java path depending on your OS user or IDE settings. We opted not to complicate this with Docker, as the scope was a more academic causal / association analysis, rather than a production pipeline.

<h2>Access Our Datasets & Samples</h2>

To avoid having to run all of our data collection, sampling and some of the cleaning code, you can access our datasets in GCS. gcloud is installed as a dependency in our
repo, and the datasets can be accessed using the download_dataset_samples.py.

- Place the service account key in the project root dir.
- Update the keyname variable with the actual name of the key.
- Run the script and it will download the files to the appropriate place.

Note 1: The raw yearly datasets are not stored in the bucket - it would frankly take the same amount of time to download them from GCS as it would to run the download_files.ipynb file.
Note 2: Access is limited to the bucket, and the GCP project will be deleted after the final grades have posted. Reach out to Jacob P at jperius@umich.edu or via Slack if there are any issues!

<h2>Order of Operations</h2>

If you run the data collection -> modeling notebooks end-to-end, there is a general order of operations to follow. The steps are outlines below:

<h3>Collect, Clean & Merge</h3>

Option A:

1. Run download_files.ipynb in the data_collection directory to collect the raw .csv files from the host site.
2. Run generate_natality_7yr_test_data.ipynb and generate_10pct_sample_data.ipynb.

Option B:

1. You can skip the above two steps by running download_dataset_samples.py using the instructions provided above.

Note: after either method is wrapped up, you can run the other files available in this repo.

<h3>recall_optimized_modeling, dag_generation, and variable_selection</h3>

These subdirectories each have a 'prep_data_*' notebook that prepares the data for the given task being executed. The visualization notebooks (if present) are the last to run (if you are so inclined to do so).
