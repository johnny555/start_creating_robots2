from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def serve_home():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run()
