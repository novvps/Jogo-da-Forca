from flask import Flask, render_template, request, redirect, url_for, flash, session # importa o flask e suas funções

app = Flask('__name__') # define app
app.secret_key = 'DDS2JOGO' # chave secreta para poder usar o session

# ROTA PRINCIPAL (ESCOLHER PALAVRA E DICA)
@app.route('/', methods=['GET', 'POST']) # a rota principal e seus métodos
@app.route('/index', methods=['GET', 'POST']) # repetimos o processo de rota para evitar erros
def index(): # define index, ou seja, rota principal
    if request.method == 'POST': # verifica se o método é post (enviar informações)
        palavra = request.form.get('palavra') # pega a palavra que foi escrita no html
        dica = request.form.get('dica') # a mesma coisa com a dica

        if palavra and dica: # se houver palavra e dica
            # salva as informações no session para mandar para os cookies do navegador
            session['palavra'] = palavra.upper()  # Mantém as palavras em maiúsculas
            session['dica'] = dica
            session['palavra_escondida'] = ['-' if char != ' ' else ' ' for char in palavra]  # Tratar espaços, se não for espaço vai ser hífen
            session['chances'] = len(palavra.replace(' ', '')) + 2  # Considerar o número de letras, não o número de espaços
            session['letras_tentadas'] = []
            return redirect(url_for('jogo')) # redireciona o jogador para a tela do jogo

    return render_template('index.html') # renderiza o template (html) do jogo

# ROTA DO JOGO
@app.route('/jogo', methods=['GET', 'POST']) # aqui a rota é /jogo porque não é a principal, no caso só a barra (/)
def jogo(): # definimos jogo
    palavra = session.get('palavra', '').upper() # pegamos lá no session a palavra e deixamos ela maiúscula, senão ela fica vazia
    dica = session.get('dica', '') # mesma coisa com dica e os demais abaixo
    palavra_escondida = session.get('palavra_escondida', []) 
    chances = session.get('chances', 0)
    letras_tentadas = session.get('letras_tentadas', [])

    if not palavra or not dica: # se não tiver palavra e nem dica
        return redirect(url_for('index')) # redireciona de volta para o index, porque precisa desses elementos para jogar

    if request.method == 'POST': # verificamos se o método é post
        tipo_palpite = request.form.get('tipo_palpite') # verificamos o tipo do palpite lá no html, isso é fora do jogo

        if tipo_palpite == 'letra':  # Tentativa de uma única letra, caso o submit envie o valor "letra"
            palpite = request.form.get('palpite', '').upper() # pega o palpite de letra que o usuário escreveu no front e deixa maiúscula, senão fica vazio

            if len(palpite) != 1 or not palpite.isalpha(): # se o jogador escrever mais de uma letra ou escrever símbolos
                flash("Digite apenas UMA letra válida!") # vai alertar com o flash e vai invalidar a jogada
            elif palpite in letras_tentadas: # mas caso o palpite já tenha sido tentado
                flash("Você já tentou essa letra.") # vai alertar também
            else: # senão
                letras_tentadas.append(palpite) # vai adicionar o palpite na lista de letras tentadas
                if palpite in palavra: # caso o palpite esteja na palavra
                    flash("Letra correta!") # alertará que o jogador acertou a letra
                    for i, letra in enumerate(palavra): # vai percorrer a palavra
                        if letra == palpite: # caso a letra seja igual ao palpite
                            palavra_escondida[i] = palpite # substitui a letra em sua devida localização
                else: # caso o palpite não esteja na palavra
                    chances -= 1 # tira uma chance do jogador
                    flash(f"Letra incorreta. Você tem {chances} chances restantes.") # alerta que a letra está incorreta e quantas restam

        elif tipo_palpite == 'palavra':  # Tentativa de adivinhar a palavra inteira, caso o valor que o submit enviou seja "palavra"
            chute = request.form.get('palpite', '').upper() # a pessoa vai chutar uma palavra lá no front (html) e o back pega esse chute e deixa maiúsculo

            if chute == palavra: # caso o chute seja igual a palavra
                flash(f"Parabéns! Você acertou a palavra: {palavra}") # o jogador recebe o flash de que ganhou e acertou a palavra, no final mostrando qual era
                return redirect(url_for('index')) # retorna para a página inicial
            else: # caso tenha errado a palavra
                flash(f"Você errou! A palavra era: {palavra}") # ele perde a partida e mostra a palavra que era, tudo isso usando o flash
                return redirect(url_for('index')) # retorna para a página inicial

        # Atualiza a sessão com os novos valores
        session['palavra_escondida'] = palavra_escondida
        session['chances'] = chances
        session['letras_tentadas'] = letras_tentadas
        session.modified = True # sessões modificadas

        # Verifica se o jogador ganhou ou perdeu
        if '-' not in palavra_escondida: # caso não tenha mais hífen na palavra escondida, quer dizer que o jogador ganhou
            flash(f"Parabéns! Você descobriu a palavra: {palavra}") # o jogador ganha a partida e vê a palavra final
            return redirect(url_for('index')) # volta para a página index
        elif chances == 0: # mas caso as chances tenham zerado
            flash(f"Você perdeu! A palavra era: {palavra}") # o jogador perde a partida
            return redirect(url_for('index')) # volta para o index

    return render_template('jogo.html', # renderizamos o html
        palavra_escondida=''.join(palavra_escondida), # colocamos as variáveis para serem passadas para o html do jogo.html
        dica=dica, 
        chances=chances, 
        letras_tentadas=letras_tentadas
    )

# verificamos se é o main
if __name__ == '__main__':
    app.run(debug=True) # executamos o app
