from flask import Flask, render_template, request, redirect, url_for, flash, session # importa as funções do flask

app = Flask('__name__') # isso é padrão
app.secret_key = 'DDS2JOGO' # chave de segurança para executar o session

@app.route('/', methods=['GET', 'POST']) # crio uma rota principal com seus métodos
@app.route('/index', methods=['GET', 'POST']) # na rota principal eu a nomeio de index
def index(): # defino index
    if request.method == 'POST':
        # pego os dados e transfiro para variáveis
        palavra = request.form.get('palavra') # faço uma requisição do input nomeado de palavra, ou seja, name="palavra"
        dica = request.form.get('dica') # a mesma coisa com a dica

        if palavra and dica: # caso os dados sejam válidos
            # criaremos sessões para cada informação, ou seja, ficará armazenado no site
            session['palavra'] = palavra
            session['dica'] = dica
            session['palavra_escondida'] = ['-' for _ in palavra]  # Inicializa os traços
            session['chances'] = len(palavra) + 2  # Define as chances
            session['letras_tentadas'] = []  # Inicializa as letras tentadas
            return redirect(url_for('jogo')) # redireciona para a rota jogo

    return render_template('index.html') # renderiza o template (html) do index

@app.route('/jogo', methods=['GET', 'POST']) # mesmo esquema da rota acima
def jogo(): # é definido
    palavra = session.get('palavra') # pegamos o session que foi passado lá em cima com o get
    dica = session.get('dica')
    palavra_escondida = session.get('palavra_escondida')
    chances = session.get('chances')
    letras_tentadas = session.get('letras_tentadas')

    if not palavra or not dica or palavra_escondida is None or chances is None: # caso os dados sejam inválidos ou vazios
        return redirect(url_for('index')) # a pessoa volta para a rota index

    if request.method == 'POST':
        palpite = request.form.get('palpite') # pegamos o palpite que a pessoa deu, no mesmo esquema da dica e a palavra

        if not palpite or len(palpite) != 1: # caso não tenha palpite ou seja mais de uma letra
            # o flash é uma função que funciona como um pop-up
            flash("Digite apenas uma letra!") # alertará dizendo que só pode uma letra

        elif palpite in letras_tentadas: # caso o palpite esteja na lista de letras já usadas
            flash("Você já tentou essa letra.") # alerta sobre isso
        else: # caso contrário
            letras_tentadas.append(palpite) # as letras usadas (palpites) ficarão armazenadas
            if palpite in palavra: # se o palpite estiver na palavra
                flash("Isso aí!") # a pessoa verá que acertou
                # A função enumerate() do Python é usada para acessar o valor e o índice de cada elemento de uma lista, simultaneamente.
                for i, letra in enumerate(palavra): # para cada índice
                    if letra == palpite: # se a letra é igual ao palpite
                        palavra_escondida[i] = palpite # vai substituir o traço no índice que corresponder com o palpite
                session['palavra_escondida'] = palavra_escondida # salvamos/atualizamos a sessão da palavra escondida, assim quando atualizar a palavra não terá problemas com as letras
            else: # porém, caso o palpite não esteja na palavra
                chances -= 1 # as chances diminuem
                session['chances'] = chances # salvamos/atualizamos a informação das chances em sua sessão correspondente
                flash(f'Letra incorreta. Chances restantes: {chances}') # alerta sobre a letra incorreta e a quantidade de chances

            if '-' not in palavra_escondida: # caso não haja nenhum outro traço, ou seja, a palavra estará completa
                flash(f'Parabéns! Você acertou a palavra: {palavra}') # a pessoa irá ganhar o jogo
                return redirect(url_for('index')) # e retornará ao início
            elif chances == 0: # mas se suas chances acabarem antes disso
                flash(f'Suas chances acabaram. A palavra era: {palavra}') # a pessoa perde o jogo
                return redirect(url_for('index')) # e retorna ao index

        session['letras_tentadas'] = letras_tentadas # salvamos as letras usadas em sua sessão

    return render_template('jogo.html', palavra_escondida=''.join(palavra_escondida), dica=dica, chances=chances, letras_tentadas=letras_tentadas) # levamos todas essas variáveis para o html

# roda o código
if __name__ == '__main__':
    app.run(debug=True)
