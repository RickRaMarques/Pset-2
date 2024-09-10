# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo:Ricardo Ramalho Marques
#    Matrícula:202308031
#    Turma:CC3M-B
#    Email: rickramalhomarques@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO
from PIL import Image as PILImage


# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels

    def get_pixel(self, x, y):
        # Trata os índices fora dos limites da imagem
        # Se a coordenada x estiver fora do intervalo [0, largura da imagem - 1], ajusta para os limites
        if x < 0:
            x = 0
        elif x >= self.largura:
            x = self.largura - 1

        # Se a coordenada y estiver fora do intervalo [0, altura da imagem - 1], ajusta para os limites
        if y < 0:
            y = 0
        elif y >= self.altura:
            y = self.altura - 1

        # Calcula o índice do pixel no vetor de pixels da imagem
        indice = x + y * self.largura 
        
        # Obtém o valor do pixel corrigido
        pixel_value = self.pixels[indice]

        # Garante que o valor do pixel esteja no intervalo [0, 255]
        if pixel_value < 0:
            return 0
        elif pixel_value > 255:
            return 255
        else:
            return pixel_value



    def set_pixel(self, x, y, c):
        # Calcula o índice do pixel no vetor de pixels da imagem
        indice = x + y * self.largura 

        # Define o valor do pixel no vetor de pixels da imagem
        self.pixels[indice] = c


    def aplicar_por_pixel(self, func):
        
        resultado = Imagem.nova(self.largura, self.altura)

        # Itera sobre cada pixel na imagem
        for x in range(resultado.largura):
            for y in range(resultado.altura):
                # Obtém a cor do pixel original na posição (x, y)
                cor = self.get_pixel(x, y)
                # Aplica a função 'func' à cor do pixel
                nova_cor = func(cor)
                # Define a nova cor para o pixel na posição (x, y) na imagem resultante
                resultado.set_pixel(x, y, nova_cor)

    
        return resultado


    def kernel_aplicador(self, kernel):
        # Lista para armazenar os novos pixels resultantes da aplicação do kernel
        pixel_novo = []

        # Itera sobre as linhas da imagem
        for y in range(self.altura):
            # Itera sobre as colunas da imagem
            for x in range(self.largura):
                # Inicializa a soma dos produtos do kernel com os pixels da região
                soma_do_kernel = 0 

                # Itera sobre as linhas do kernel
                for kernel_y in range(len(kernel)):
                    # Itera sobre as colunas do kernel
                    for kernel_x in range(len(kernel[0])):
                        # Calcula as coordenadas do pixel na imagem original correspondente à posição do kernel
                        px_kernel = x + kernel_x - len(kernel[0]) // 2
                        py_kernel = y + kernel_y - len(kernel) // 2

                        # Corrige os índices para garantir que estejam dentro dos limites da imagem
                        px_kernel = max(0, min(px_kernel, self.largura - 1))
                        py_kernel = max(0, min(py_kernel, self.altura - 1))

                        # Obtém o valor do pixel na posição ajustada
                        pixel = self.get_pixel(px_kernel, py_kernel)

                        # Realiza a multiplicação do pixel pelo valor correspondente no kernel e soma ao total
                        soma_do_kernel += pixel * kernel[kernel_y][kernel_x]

                # Arredonda o valor resultante da aplicação do kernel
                resultado_pixel_novo = round(soma_do_kernel)     

                # Garante que o valor esteja entre 0 e 255
                resultado_pixel_novo = max(0, min(resultado_pixel_novo, 255))

                # Adiciona o valor arredondado e limitado ao intervalo à lista de novos pixels
                pixel_novo.append(int(resultado_pixel_novo))

        # Retorna uma nova imagem com os pixels resultantes da aplicação do kernel
        return Imagem(self.largura, self.altura, pixel_novo)


    def invertida(self):
        # Aplica uma função lambda a cada pixel da imagem para inverter sua intensidade
        return self.aplicar_por_pixel(lambda c: 255 - c)


    def borrada(self, n):
        # Cria um kernel de convolução para o filtro de borramento
        kernel = [[1/(n*n) for _ in range(n)] for _ in range(n)]
        
        # Aplica o kernel de convolução à imagem atual
        resultado = self.kernel_aplicador(kernel)
        
        # Aplica uma função lambda a cada pixel da imagem resultante
        # para garantir que os valores estejam no intervalo [0, 255]
        resultado = resultado.aplicar_por_pixel(lambda c: max(min(round(c), 255), 0))
        
        # Retorna a imagem resultante após o borramento
        return resultado


    def focada(self, n):
        # Fator de multiplicação
        fator = 2

        # Arredonda o valor do filtro 
        n_arredondado = round(n)

        # Borrar a imagem utilizando a função já definida
        imagem_borrada = self.borrada(n_arredondado)

        # Nova imagem para armazenar o resultado
        imagem_nitida = Imagem.nova(self.largura, self.altura)

        # Aplicar a operação de nitidez para cada pixel
        for y in range(self.altura):
            for x in range(self.largura):
                # Obter o valor do pixel original
                Ixy = self.get_pixel(x, y)
                # Obter o valor do pixel borrado
                Bxy = imagem_borrada.get_pixel(x, y)

                # Aplicar a fórmula de nitidez
                Sxy = fator * Ixy - Bxy

                # Verificar se o resultado é negativo e ajustar se necessário
                if Sxy < 0:
                    Sxy = 0

                # Verificar se o resultado ultrapassa 255 e ajustar se necessário
                elif Sxy > 255:
                    Sxy = 255

                # Definir o pixel na nova imagem
                imagem_nitida.set_pixel(x, y, round(Sxy))

        return imagem_nitida





# Neste filtro bordas eu apesar de conseguir chegar num valor de resultado aproximado, não consegui chegar no valor exato desejado pelo teste 

    def bordas(self):
        # Define os kernels Kx e Ky para detecção de bordas
        kx = [[-1, 0, 1],
            [-2, 0, 2], 
            [-1, 0, 1]]

        ky = [[-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]]

        # Calcula as bordas horizontais e verticais
        borda_H = self.kernel_aplicador(kx)
        borda_V = self.kernel_aplicador(ky)

        # Nova imagem para armazenar o resultado
        resultado = Imagem.nova(self.largura, self.altura)

        # Itera sobre cada pixel da imagem
        for x in range(self.largura):
            for y in range(self.altura):
                # Obtém os valores de bordas horizontais e verticais
                ox = borda_H.get_pixel(x, y)
                oy = borda_V.get_pixel(x, y)
                # Calcula a magnitude da borda
                magnitude = round(math.sqrt(ox ** 2 + oy ** 2))
                # Garante que o valor esteja entre 0 e 255
                magnitude = max(min(magnitude, 255), 0)
                # Define o pixel na nova imagem
                resultado.set_pixel(x, y, magnitude)

        # Retorna a imagem resultante com as bordas detectadas
        return resultado

  

    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.width, event.height), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.height, width=e.width))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.
    
    i = Imagem.carregar('test_images/mushroom.png')
    resultado = i.bordas()
    resultado.salvar('banana.png')
    resultado.mostrar()

    pass


    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()