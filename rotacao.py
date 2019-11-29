from PIL import Image
import math

#Abre uma imagem
def abrir_imagem(nome_img):
    img = Image.open(nome_img)
    return img

#Converte a imagem original para a escala de cinza
def converter_para_escala_de_cinza(img):
    img = img.convert('L')
    return img


#Cria nova imagem toda branca com o dobro do tamanho da imagem original
#para ser preenchida posteriormente
def nova_imagem_reducao(img):
    new_img = Image.new('L',(int(img.width/2),int(img.height/2)), color='white')
    return new_img


#Cria nova imagem toda branca com o dobro do tamanho da imagem original
#para ser preenchida posteriormente
def nova_imagem_ampliacao(img):
    new_img = Image.new('L',(img.width*2,img.height*2), color='white')
    return new_img

def nova_imagem_semelhante(img):
    new_img = Image.new('L',(img.width,img.height), color='white')
    return new_img

def rotacao(img, ang):
    new_img = nova_imagem_semelhante(img)
    pix = new_img.load()
    pix2 = img.load()
    xm = int(img.width/2)
    ym = int(img.height/2)
    for i in range(0,img.height):
        for j in range(0,img.width):
            x = i-xm
            y = ym -j
            nx = x*math.cos(ang) - y*math.sin(ang)
            ny = x*math.sin(ang) + y*math.cos(ang)
            print(nx,ny)
            if(nx>=-xm and nx < xm):
                if(ny>=-ym and ny < ym):
                    pix[nx+xm,ym-ny] = pix2[i,j]
    
    #new_img.save('imagem_rotacionada_em_'+ang+'_graus.png')
    return new_img

def main(ang):
    img = abrir_imagem('UEA.jpg')
    img = converter_para_escala_de_cinza(img)
    img.show()
    new_img = rotacao(img,ang)
    new_img.show()
    
    
if(__name__ == '__main__'):
    ang = 30
    angRad = math.pi * ang/180
    print(math.sin(angRad))
    main(angRad)
    '''
    print('1 - Interpolação vizinho mais próximo Redução')
    print('2 - Interpolação vizinho mais próximo Ampliação')
    print('3 - Interpolação bilinear Redução')
    print('4 - Interpolação bilinear Ampliação\n')
    inp = input("Escolha uma opção: ")
    main(inp)
    '''