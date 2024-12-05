import os
import zipfile

# Set the Kaggle API key location
os.environ['KAGGLE_CONFIG_DIR'] = os.path.expanduser('~/kaggle')

# Check if the file already exists to avoid re-downloading
if not os.path.exists('orders.csv'):
    os.system('kaggle datasets download ankitbansal06/retail-orders -f orders.csv')

    # Extract the downloaded zip file
    with zipfile.ZipFile('orders.csv.zip', 'r') as zip_ref:
        zip_ref.extractall()
else:
    print("Dataset already downloaded.")
