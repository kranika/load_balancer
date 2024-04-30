# make sure to download flask first: pip install flash
from flask import Flask

app = Flask(__name__)

# Defining the /home endpoint with the GET method.
# Function to handle the /home endpoint
@app.route('/home', methods=['GET'])
def home():
    server_id = os.environ.get('SERVER_ID', '1')
    return f'Hello from Server: {server_id}'

# Defining the /heartbeat endpoint with the GET method.
# Function to handle the /heartbeat endpoint
@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200  # Empty response with a response code of 200

# running the Flask app
if __name__ == '__main__':
    app.run(port=5000)

# Run: export SERVER_ID=1 ,in the terminal first
# After running that and accessing the link, add the /home in the browser
