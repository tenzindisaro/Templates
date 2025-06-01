from flask import Flask, render_template
import os

# Importante: o template_folder agora é o próprio diretório onde está o app.py
app = Flask(__name__, template_folder=".")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/jogar")
def jogar():
    os.system("python game/main.py")
    return "Jogo executado localmente."

if __name__ == "__main__":
    app.run(debug=True)
