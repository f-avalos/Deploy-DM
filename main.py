from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():

    data = {
        "message": "Hello, World!",
        "status": "success"
    }

    return jsonify(data)

@app.route('/index')
def index():
    return render_template('content.html')

if __name__ == '__main__':
    app.run(debug=True)