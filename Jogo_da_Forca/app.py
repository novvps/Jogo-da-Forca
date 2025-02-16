from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask('__name__')
app.secret_key = 'DDS2JOGO'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        palavra = request.form.get('palavra')
        dica = request.form.get('dica')

        if palavra and dica:
            session['palavra'] = palavra.upper()  # Para garantir que tudo fique em maiúsculas
            session['dica'] = dica
            session['palavra_escondida'] = ['-' for _ in palavra]
            session['chances'] = len(palavra) + 2
            session['letras_tentadas'] = []
            return redirect(url_for('jogo'))

    return render_template('index.html')

@app.route('/jogo', methods=['GET', 'POST'])
def jogo():
    palavra = session.get('palavra', '').upper()
    quantidade = len(palavra)
    dica = session.get('dica', '')
    palavra_escondida = session.get('palavra_escondida', [])
    chances = session.get('chances', 0)
    letras_tentadas = session.get('letras_tentadas', [])

    if not palavra or not dica:
        return redirect(url_for('index'))

    if request.method == 'POST':
        tipo_palpite = request.form.get('tipo_palpite')  # Identifica o tipo de palpite

        if tipo_palpite == 'letra':  # Tentativa de uma única letra
            palpite = request.form.get('palpite', '').upper()

            if len(palpite) != 1 or not palpite.isalpha():
                flash("Digite apenas UMA letra válida!")
            elif palpite in letras_tentadas:
                flash("Você já tentou essa letra.")
            else:
                letras_tentadas.append(palpite)
                if palpite in palavra:
                    flash("Letra correta!")
                    for i, letra in enumerate(palavra):
                        if letra == palpite:
                            palavra_escondida[i] = palpite
                else:
                    chances -= 1
                    flash(f"Letra incorreta. Você tem {chances} chances restantes.")

        elif tipo_palpite == 'palavra':  # Tentativa de chutar a palavra inteira
            chute = request.form.get('chute', '').upper()

            if chute == palavra:
                flash(f"Parabéns! Você acertou a palavra: {palavra}")
                return redirect(url_for('index'))
            else:
                flash(f"Você errou! A palavra era: {palavra}")
                return redirect(url_for('index'))

        # Atualiza a sessão com os novos valores
        session['palavra_escondida'] = palavra_escondida
        session['chances'] = chances
        session['letras_tentadas'] = letras_tentadas
        session.modified = True

        # Verifica se o jogador ganhou ou perdeu
        if '-' not in palavra_escondida:
            flash(f"Parabéns! Você descobriu a palavra: {palavra}")
            return redirect(url_for('index'))
        elif chances == 0:
            flash(f"Você perdeu! A palavra era: {palavra}")
            return redirect(url_for('index'))

    return render_template('jogo.html', 
        palavra_escondida=''.join(palavra_escondida), 
        dica=dica, 
        chances=chances, 
        letras_tentadas=letras_tentadas, 
        quantidade=quantidade
    )

if __name__ == '__main__':
    app.run(debug=True)
