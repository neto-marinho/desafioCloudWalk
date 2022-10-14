import json

players = []
mortes = []
mortesfinal = []
aAssassinatos = []
Assassinatos = []

# Adiciona o jogador que entrou na partida
def addPlayer(nomejogador):

    if nomejogador not in players:
        players.append(nomejogador)

# Acrescenta os jogadores que morreram em uma lista
def morreu(morto):

    mortes.append(morto)

# Realiza a contagem de quantas vezes o jogador morreu na partida
def contMorte():

    qtdadeMortes = (dict( (l, mortes.count(l) ) for l in set (mortes)))  
    mortesfinal.append(qtdadeMortes)    

# Lista com todos os jogadores que mataram outro jogador na partida
def assassinos(assasino):
    if assasino != "<world>":
        aAssassinatos.append(assasino)

# Realiza a contagem de mortes do joagador na partida, sem descontar a morte do jogador pelo <world>
def contAssinos():
        
    assassinatosFinal = (dict( (l, aAssassinatos.count(l) ) for l in set (aAssassinatos)))
    Assassinatos.append(assassinatosFinal)

# Finalizando a partida e montando o relatorio.
def finish(game_count, total_kills, game_list):

    contMorte()
    contAssinos()
    
    minhalista = {
        'game': game_count,
        'total_kills' : total_kills,
        'players' : players,
        'killed' : mortesfinal,
        'killer' : Assassinatos
    }

    game_list.append(minhalista)



def main():
    #Variaveis
    global players
    global nomejogador
    global mortes
    global mortesfinal
    global Assassinatos
    game_count = 0
    total_kills = 0
    game_list = []
    
    
    #Abre o arquivo de texto
    with open("/Projetos/DesafioQuake/Desafio/logDesafio.txt", "r") as arquivo:
        quake_lines = arquivo.readlines()

    #Loop que analisa as linhas
    for line in quake_lines:
        line = line.strip()
        line = line.split(" ", 3)

             
        if line[1] == "ClientUserinfoChanged:":
            line[3] = line[3].split("\\")                      
            nomejogador = (str(line[3][1]))  

            addPlayer(nomejogador)
            
         #Termina um jogo e começa o proximo   
        elif line[1] == "InitGame:":
            if game_count == 0:
                game_count += 1
                
            else:
                finish(game_count, total_kills, game_list)
                total_kills = 0
                players = [] 
                game_count += 1
                mortes = []
                mortesfinal = []
                Assassinatos = []
                        
            
         #Contabiliza as mortes
        elif line[1] == "Kill:":
            line[3] = line[3].split(" ", 5)

            morto = line[3][4]
            assassino = line[3][2]

            morreu(morto)
            assassinos(assassino)

            total_kills += 1

    #Escreve o dicionario de jogos em um .json
    with open('LogClouldWalk.json', "w") as arq_json:
        json.dump(game_list, arq_json, indent=4)

main()            
            