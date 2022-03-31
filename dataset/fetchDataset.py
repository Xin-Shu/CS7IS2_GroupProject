import requests
# Define the remote file to retrieve
remote_url = 'https://www.kaggle.com/datasets/bryanpark/sudoku/download'
# Define the local filename to save data
local_file = 'sudoku.csv'
# Make http request for remote file data
data = requests.get(remote_url)
# Save file data to local copy
with open(local_file, 'wb')as file:
    file.write(data.content)