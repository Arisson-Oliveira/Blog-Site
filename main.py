from flask import Flask, render_template


# Inicialização da Função
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

if __name__ == '__main__':
    app.run(debug=True)