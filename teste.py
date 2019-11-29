#A MAIN do programa está no final


from PIL import Image
import math

RAIZ2 = math.sqrt(2)
CAMINHO_IMG = 'Paisagem.jpg'
NOME_IMG = CAMINHO_IMG.split('.')[-2]

#Abre uma imagem, dado seu caminho
def abrir_imagem(nome_img):
    img = Image.open(nome_img)
    return img

#Converte a imagem original para a escala de cinza
def converter_para_escala_de_cinza(img):
    img = img.convert('L')
    return img

#Cria nova imagem toda branca com metade do tamanho da imagem original
#para ser preenchida posteriormente
def nova_imagem_reducao(img):
    new_img = Image.new('L',(int(img.width/2),int(img.height/2)), color='white')
    return new_img

#Cria nova imagem toda branca com o dobro do tamanho da imagem original
#para ser preenchida posteriormente
def nova_imagem_ampliacao(img):
    new_img = Image.new('L',(img.width*2,img.height*2), color='white')
    return new_img

#Cria nova imagem toda branca com o tamanho certo para a rotação
#para ser preenchida posteriormente
def nova_imagem_rotacao(img, sizeX, sizeY):
    new_img = Image.new('L',(sizeX,sizeY), color='white')
    return new_img



#======================REDIMENSIONAMENTO=============================#
#Passa a imagem original como parametro
#Retorna a nova imagem reduzida/ampliada preenchida com novos valores
def interpolacao_vizinho_mais_proximo_reducao(img):

    '''
    Reducao usando interpolação pelo vizinho mais proximo
    Ocorre repetição de um dos pixels vizinhos na redução

    01 02 03 04 -> 01 03
    05 06 07 08 -> 09 11
    09 10 11 12
    13 14 15 16

    '''

    new_img = nova_imagem_reducao(img) #Cria uma imagem em branco
    pix = new_img.load()               #Matriz de pixels da nova imagem
    pix2 = img.load()                  #Matriz de pixels da imagem original
    

    k = 0
    l = 0
    
    for i in range(0,img.width,2):
        for j in range(0,img.height,2):
            try:
                pix[k,l] = pix2[i,j]
                l+=1
            except:
                continue
        
        l=0
        k+=1
    
    new_img.save('imagem_reduzida_vizinho_mais_proximo.png')
    return new_img


def interpolacao_vizinho_mais_proximo_ampliacao(img):

    '''
    Ampliação usando interpolação pelo vizinho mais proximo
    Ocorre repetição dos pixels vizinhos para preencher espaço

    1 2 3  -> 1 1 2 2 3 3
    4 5 6  -> 1 1 2 2 3 3
    7 8 9  -> 4 4 5 5 6 6
              4 o 5 5 6 6
              7 7 8 8 9 9
              7 o 8 o 9 9

    '''

    new_img = nova_imagem_ampliacao(img)#Cria uma nova imagem em branco
    pix = new_img.load()                #Matriz de pixels da nova imagem
    pix2 = img.load()                   #Matriz de pixels da imagem original
    
    for i in range(0,img.width):
        for j in range(0,img.height):
            try:
                pix[2*i     , 2*j    ] = pix2[i,j]
                pix[2*i + 1 , 2*j    ] = pix2[i,j]
                pix[2*i     , 2*j + 1] = pix2[i,j]
                pix[2*i + 1 , 2*j + 1] = pix2[i,j]
            except: continue
    new_img.save('imagem_ampliada_vizinho_mais_proximo.png')
    return new_img


def interpolacao_bilinear_reducao(img):

    '''
    Redução usando interpolação bilinear
    O pixel da imagem reduzida é o inteiro da media dos pixels adjacentes da imagem original
    Obs: Por utilizar média, ocorre uma suavixação na imagem
    Ex: 1 2 -> (1+2+3+4)/4 -> 2,5 -> 2
        3 4

    01 02 03 04 -> 03 05
    05 06 07 08 -> 11 13
    09 10 11 12
    13 14 15 16

    '''

    new_img = nova_imagem_reducao(img)#Cria uma nova imagem em branco
    pix = new_img.load()              #Matriz de pixels da nova imagem
    pix2 = img.load()                 #Matriz de pixels da imagem original


    k = 0
    l = 0

    for i in range(0,img.width,2):
        for j in range(0,img.height,2):
            try:
                x = (pix2[i,j] + pix2[i,j+1] + pix2[i+1, j] + pix2[i+1, j+1])/4
                pix[k,l] = int(x)
                l+=1
            except: continue
        l=0
        k+=1
    
    new_img.save('imagem_reduzida_bilinear.png')
    return new_img


def interpolacao_bilinear_ampliacao(img):

    '''
    Ampliação usando interpolação bilinear
    Cada x recebe a media de seus 2 adjacentes, com exceção dos que estão nas laterais
    Cada o recebe a media das 4 mais proximas diagonais, com exceção dos que estão nas laterais
    
    Os x que estão nas laterais apenas repetem o pixel mais próximo
    Os o que estão nas laterais recebem a média de seus 2 pixels diagonais mais próximos

    Obs: Por utilizar média, ocorre uma suavixação na imagem
    1 2 3  -> 1 x 2 x 3 x
    4 5 6  -> x o x o x o
    7 8 9  -> 4 x 5 x 6 x
              x o x o x o
              7 x 8 x 9 x
              x o x o x o
    '''

    new_img = nova_imagem_ampliacao(img)
    pix = new_img.load()
    pix2 = img.load()

    for i in range(0,2*img.width,2):
        for j in range(0,2*img.height,2):
            try:
                pix[i,j] = pix2[int(i/2),int(j/2)]
                
                if((j+2 == 2*img.width) and (i+2 == 2*img.height)):#O canto inferior direito
                    pix[i+1,j] = pix2[int(i/2),int(j/2)]
                    pix[i,j+1] = pix2[int(i/2),int(j/2)]
                    pix[i+1,j+1] = pix2[int(i/2),int(j/2)]

                elif(j+2 == 2*img.width):#Não é o canto, mas é lateral direita
                    pix[i+1,j] = int((pix2[int(i/2),int(j/2)] + pix2[int((i+2)/2),int(j/2)])/2)
                    pix[i,j+1] = int(pix2[int(i/2),int(j/2)])
                    pix[i+1,j+1] = int((pix2[int(i/2),int(j/2)] + pix2[int((i+2)/2),int(j/2)])/2)

                elif(i+2 == 2*img.height):#Não é o canto, mas é a parte inferior
                    pix[i+1,j] = int(pix2[int(i/2),int(j/2)])
                    pix[i,j+1] = int((pix2[int(i/2),int(j/2)] + pix2[int(i/2),int((j+2)/2)])/2)
                    pix[i+1,j+1] = int((pix2[int(i/2),int(j/2)] + pix2[int(i/2),int((j+2)/2)])/2)

                else:#Caso geral, calcula conforme dito anteriormente
                    pix[i+1,j] = int((pix2[int(i/2),int(j/2)] + pix2[int((i+2)/2),int(j/2)])/2)
                    pix[i,j+1] = int((pix2[int(i/2),int(j/2)] + pix2[int(i/2),int((j+2)/2)])/2)
                    pix[i+1,j+1] = int((pix2[int(i/2),int(j/2)] + pix2[int((i+2)/2),int(j/2)] + pix2[int(i/2),int(j/2)] + pix2[int(i/2),int((j+2)/2)])/4)
            except: continue    
    new_img.save('imagem_ampliada_bilinear.png')
    return new_img

#==============================ROTAÇÃO==============================#
#As funções seno e cosseno são necessárias para realizar a rotação,
#e em Python o angulo precisa estar em radiano, por isso, a função
#abaixo transforma um ângulo de graus para radianos
def rad(ang):
    return math.pi * int(ang)/180

#Dada uma imagem, que é representada como uma matriz de pixels
#verifica se a posição (i,j) existe na imagem, se não existe,
#retorna -1, se existe, verifica se a cor em (i,j) é igual a
#255 (branco), se for, retorna 0, se não for, retorna 1

def verificaPx(img,i,j):
    pix = img.load()
    if(i<0 or i>=img.width or j<0 or j>=img.height): return -1
    if(pix[i,j] == 255):
        return 0
    return 1

#A rotação pode usar ou não, interpolação

def rotacao_sem_interpolacao(img,ang):
    #Definindo a largura e altura da imagem rotacionada
    #para não precisar cortar alguma parte da imagem, já que
    #quando rotaciona-se uma imagem, altura e largura mudam
    '''
    Mais ou menos assim:
   (Img Orig) (Img Rot)  (0 = "buracos", apenas para melhor mostrar q o tamanho mudou)
                 1    ->    1
               1   1  ->  10001
    1 1 1 ->  1  1  1 -> 1001001
    1 1 1 ->   1   1  ->  10001 
    1 1 1 ->     1    ->    1
    '''
    ang = ang%360
    angRad = rad(ang)
    senn = math.sin(angRad) if(int(ang/90)%2  ==0) else math.cos(rad(ang-90))
    coss = math.cos(angRad) if(int(ang/90)%2  ==0) else math.sin(rad(ang-90))

    xx = img.width
    yy = img.height
    sizeX = int(abs(yy*senn+xx*coss))
    sizeY = int(abs(yy*coss+xx*senn))
    

    #Rotação em si
    new_img = nova_imagem_rotacao(img, sizeX,sizeY) #Cria uma imagem em branco com os novos tamanhos
    pix = new_img.load()                            #Matriz de pixels da nova imagem
    pix2 = img.load()                               #Matriz de pixels da imagem original
                        
    #A rotação é feita no centro da imagem (xm,ym)
    xm = int(img.width/2) 
    ym = int(img.height/2)

    for i in range(0,img.width):
        for j in range(0,img.height):
            #Encontrando os pontos equivalentes na nova imagem, (x,y) -> (nx,ny)
            #Relembrando que são em relação ao centro da imagem
            x = i-xm
            y = ym -j
            nx = x*math.cos(angRad) - y*math.sin(angRad)
            ny = x*math.sin(angRad) + y*math.cos(angRad)

            try: pix[nx+int(sizeX/2),int(sizeY/2)-ny] = pix2[i,j]
            except: continue
    
    new_img.save(NOME_IMG+'_sem_interpolacao_'+str(ang)+'°.png')
    return new_img

def rotacao_interpolacao_bilinear(img, ang):

    #Definindo a largura e altura da imagem rotacionada
    #para não precisar cortar alguma parte

    #Não entrando muito em detalhes, mas:
    #Analisando matematicamente a imagem final em relação à original percebe-se
    #que se o angulo de rotação estiver nos quadrantes pares, usa-se uma fórmula
    #e se estiver nos ímpares, usa-se outra
    ang = ang%360
    angRad = rad(ang)
    senn = math.sin(angRad) if(int(ang/90)%2  ==0) else math.cos(rad(ang-90))
    coss = math.cos(angRad) if(int(ang/90)%2  ==0) else math.sin(rad(ang-90))

    xx = img.width
    yy = img.height
    sizeX = int(abs(yy*senn+xx*coss))
    sizeY = int(abs(yy*coss+xx*senn))
    
    #Rotaciona a imagem, antes de realizar a interpolação
    new_img = rotacao_sem_interpolacao(img,ang)
    pix = new_img.load() #Matriz de pixels

    '''
    Como a rotação nada mais é que uma transformação de pixels
    a quantidade de pixels permanece a mesma, mas alguns lugares na
    imagem resultante ficam com "buracos"
    
    Por esse motivo, aplicar Interpolação Bilinear deixa a imagem mais "limpa",
    porém esta interpolação é lenta, o que deixa mais lento o processo de rotação
    '''
    for i in range(0,sizeX):
        for j in range(0,sizeY):
            #Primeiro verifica se os pontos existem e se são brancos ou não,
            #Ao evitar utilizar os pixels brancos, o resultado final
            v1 = verificaPx(new_img,i+1,j)
            v2 = verificaPx(new_img,i-1,j)
            v3 = verificaPx(new_img,i,j+1)
            v4 = verificaPx(new_img,i,j-1)
            qnt = 0
            soma =0
            if(v1==1):
                qnt+=1
                soma+=pix[i+1,j]
            
            if(v2==1):
                qnt+=1
                soma+=pix[i-1,j]
            
            if(v3==1):
                qnt+=1
                soma+=pix[i,j+1]
            
            if(v4==1):
                qnt+=1
                soma+=pix[i,j-1]
            
            if(qnt == 4):pix[i,j] = int(soma/qnt)
    
    new_img.save(NOME_IMG+'_interpolacao_bilinear_'+str(ang)+'_graus.png')
    return new_img


#========================Tratamento dos valores da entrada===================#
def main(inp):
    if(not(inp>='1' and inp<='6')): print("Opção Inválida")
    else:
        new_img = ''
        img = abrir_imagem(CAMINHO_IMG)
        img = converter_para_escala_de_cinza(img)
        
        if(inp == '1'):
            #vizinho mais proximo reducao
            new_img = interpolacao_vizinho_mais_proximo_reducao(img)
        
        elif(inp == '2'):
            #vizinho mais proximo ampliacao
            new_img = interpolacao_vizinho_mais_proximo_ampliacao(img)
        
        elif(inp == '3'):
            #bilinear reducao
            new_img = interpolacao_bilinear_reducao(img)
        
        elif(inp == '4'):
            #bilinear ampliacao
            new_img = interpolacao_bilinear_ampliacao(img)
        
        else:
            g = input("De um angulo para rotacionar: ")
            if(not g.isnumeric()): print("Valor Inválido")
            elif(inp == '5'):
                #rotacao sem interpolacao
                new_img = rotacao_sem_interpolacao(img,int(g))
            elif(inp == '6'):    
                #rotacao com interpolacao bilinear
                new_img = rotacao_interpolacao_bilinear(img,int(g))
        
        if(new_img != ''): new_img.show()

#===========================LENDO A ENTRADA ===========================#
if(__name__ == '__main__'):
    
    print('1 - Interpolação vizinho mais próximo Redução')
    print('2 - Interpolação vizinho mais próximo Ampliação')
    print('3 - Interpolação bilinear Redução')
    print('4 - Interpolação bilinear Ampliação')
    print('5 - Rotacionar sem Interpolação')
    print('6 - Rotacionar com Interpolação Bilinear\n')
    inp = input("Escolha uma opção: ")
    main(inp)
    