import os
palavra_escolhida = [] # lista
palavra_escondida = [] # lista
acertou = False # o jogador ainda não venceu
i = 0

print('            JOGO DA FORCA       \n')

# PRÉ JOGO
palavra = input('Digite uma palavra: ') # o jogador digita uma palavra
for letra in palavra: # para cada letra na palavra que o jogador escolheu
    palavra_escolhida.append(letra) # essas letras ficarão separadas (Ex.: Uva = U, v, a)

dica = input('Digite uma dica: ') # digita a dica

for i in range(len(palavra_escolhida)): # para cada caracter na palavra escolhida
    palavra_escondida += '-' # vai ter um traço, como se fosse para esconder (Ex.: Uva = - - -)

os.system('cls') or None # limpa o terminal

# INICIO DO JOGO
print('Dica da palavra: ',dica) # a dica digitada aparece no terminal

chances = len(palavra) + 2 # as chances serão baseadas na quantidade de letras da palavra e para ficar mais justo será adicionado mais duas chances

while acertou == False and chances > 0: # enquanto a pessoa não acertar e as chances forem maiores que zero
    print('\n',palavra_escondida) # mostra a palavra escondida (os traços)

    palpite = input('\nDigite uma letra: ') # a pessoa digitará um palpite

    if palpite in palavra_escolhida: # se esse palpite estiver dentro da palavra escolhida
        print('Isso aí!\n') # isso aparece no terminal
        for i in range(len(palavra_escolhida)): # para cada caracter dentro da palavra escolhida
            if palavra_escolhida[i] == palpite: # caso a letra da palavra escolhida seja igual ao palpite
                palavra_escondida[i] = palpite # vai substituir o traço no local exato da letra da palavra

        print('Chances restantes: ',chances) # aparece no terminal a quantidade de chances

        if palavra_escondida == palavra_escolhida: # se a palavra escondida estiver completa de forma correta, ou seja, igual a palavra escolhida
            print('Parabéns! Acertou a palavra!\n',palavra_escolhida) # irá printar a palavra
            acertou = True # mudará a variável booleana, assim encerrando o loop, pois o jogador venceu

        if chances == 0: # porém se as chances forem zero
            print('Suas chances acabaram. A palavra era: ',palavra_escolhida) # o jogador perde, encerrando o loop
    
    else: # caso o palpite esteja incorreto
        print('Letra incorreta.')
        chances -= 1 # o jogador perde uma chance
        print('Chances restantes: ',chances) # as chances que restam aparece no terminal