# make sure to download flask first: pip install flash
from flask import Flask
import os

app = Flask(__name__)

# Defining the /home endpoint with the GET method.
# Function to handle the /home endpoint: trying to check the server rresponse here
@app.route('/home', methods=['GET'])
def home():
    server_id = os.environ.get('SERVER_ID', '1')
    return f'Hello from Server: {server_id}'

# running the Flask app
if __name__ == '__main__':
    app.run(port=5000)

#run: export SERVER_ID=1 ,in the terminal first
#after running that and accessing the link, add the /home in the browser
