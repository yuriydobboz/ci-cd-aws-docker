from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "¡Hola, mundo desde Flask!"

@app.route('/status')
def status():
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
