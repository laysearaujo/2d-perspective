import cv2
import numpy as np

global points, method_choice
points = []  
method_choice = None 

# Função para capturar os pontos do mouse
def select_points(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Ponto selecionado: {(x, y)}")
        
        # Desenha o ponto selecionado
        cv2.circle(temp_image, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Selecione os pontos", temp_image)

    if method_choice == "2" and len(points) == 3: 
        print("3 pontos selecionados. Você pode agora aplicar a transformação.")
        cv2.setMouseCallback("Selecione os pontos", lambda *args: None)
    elif method_choice != "2" and len(points) == 4: 
        print("4 pontos selecionados. Você pode agora aplicar a transformação.")
        cv2.setMouseCallback("Selecione os pontos", lambda *args: None)

# Função para ordenar os pontos selecionados
def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # Top-left
    rect[2] = pts[np.argmax(s)]  # Bottom-right

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # Top-right
    rect[3] = pts[np.argmax(diff)]  # Bottom-left
    return rect

# Função personalizada para calcular a matriz de transformação de perspectiva
def manual_perspective_transform(src_pts, dst_pts):
    A = []
    B = []
    
    # Verifica se os pontos de entrada estão no formato correto
    if len(src_pts) != 4 or len(dst_pts) != 4:
        raise ValueError("Deve haver exatamente 4 pontos de origem e 4 de destino.")
    
    for i in range(4):
        x, y = src_pts[i]
        u, v = dst_pts[i]
        
        # Equações de perspectiva para cada ponto
        A.append([x, y, 1, 0, 0, 0, -x*u, -y*u])
        A.append([0, 0, 0, x, y, 1, -x*v, -y*v])
        B.append(u)
        B.append(v)
    
    A = np.array(A, dtype="float32")
    B = np.array(B, dtype="float32")
    
    # Resolvendo o sistema de equações (Ax = B)
    M = np.linalg.lstsq(A, B, rcond=None)[0]
    
    # A matriz de transformação é reorganizada para uma matriz 3x3
    matrix = np.array([
        [M[0], M[1], M[2]],
        [M[3], M[4], M[5]],
        [M[6], M[7], 1]
    ], dtype="float32")
    
    return matrix

# Função personalizada para aplicar a transformação de perspectiva
def warp_perspective(image, matrix, dimensions):
    # Inicializando a imagem resultante com fundo branco
    result = np.ones((dimensions[1], dimensions[0], 3), dtype=np.uint8) * 255

    # Calculando a inversa da matriz de transformação
    inv_matrix = np.linalg.inv(matrix)
    
    # Percorrendo todos os pixels da imagem de saída
    for y in range(dimensions[1]):  # y -> altura
        for x in range(dimensions[0]):  # x -> largura
            # Calculando as coordenadas no espaço original da imagem
            src_pt = np.dot(inv_matrix, np.array([x, y, 1]))
            
            # Normalizando as coordenadas para o sistema de coordenadas da imagem original
            src_x, src_y = src_pt[0] / src_pt[2], src_pt[1] / src_pt[2]

            # Verificando se o ponto calculado está dentro dos limites da imagem original
            if 0 <= src_x < image.shape[1] and 0 <= src_y < image.shape[0]:
                # Usando interpolação bilinear para obter o valor do pixel
                src_x_int = int(src_x)
                src_y_int = int(src_y)
                
                # Caso de interpolação bilinear simples
                dx, dy = src_x - src_x_int, src_y - src_y_int
                if src_x_int + 1 < image.shape[1] and src_y_int + 1 < image.shape[0]:
                    top_left = image[src_y_int, src_x_int]
                    top_right = image[src_y_int, src_x_int + 1]
                    bottom_left = image[src_y_int + 1, src_x_int]
                    bottom_right = image[src_y_int + 1, src_x_int + 1]
                    
                    # Calculando a interpolação bilinear
                    top = (1 - dx) * top_left + dx * top_right
                    bottom = (1 - dx) * bottom_left + dx * bottom_right
                    pixel_value = (1 - dy) * top + dy * bottom
                    result[y, x] = pixel_value
                else:
                    # Caso sem interpolação (simples atribuição de valor)
                    result[y, x] = image[src_y_int, src_x_int]

    return result

# Função para aplicar a transformação afim
def affine_with_params(image, points, trans_x, trans_y, scale_factor, angle):
    # Criando a matriz de transformação afim
    rows, cols = image.shape[:2]
    
    # Calculando o centro da imagem para aplicar a rotação
    center = (cols // 2, rows // 2)

    # Gerando a matriz de rotação
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale_factor)
    
    # Adicionando a translação à matriz de rotação
    rotation_matrix[0, 2] += trans_x
    rotation_matrix[1, 2] += trans_y
    
    # Aplicando a transformação afim
    result = cv2.warpAffine(image, rotation_matrix, (cols, rows))
    return result

# Função para aplicar a transformação de perspectiva
def perspective_transform(image, points):
    ordered_pts = order_points(np.array(points, dtype="float32"))
    width, height = 500, 500

    dst_points = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")

    # Calculando a matriz de transformação de perspectiva
    matrix = manual_perspective_transform(ordered_pts, dst_points)
    result = warp_perspective(image, matrix, (width, height))
    return result

# Menu principal
def main():
    global points, temp_image, method_choice

    image_path = "tabuleiro.jpeg"  # Altere conforme sua imagem
    image = cv2.imread(image_path)
    if image is None:
        print("Erro ao carregar a imagem!")
        return

    while True:
        print("\nEscolha o método de retificação:")
        print("1 - Retificação Perspectiva")
        print("2 - Transformada Afim")
        print("0 - Sair")
        
        choice = input("Digite sua escolha: ")
        if choice == "0":
            break

        points = []
        temp_image = image.copy()
        method_choice = choice

        cv2.imshow("Selecione os pontos", temp_image)
        if choice == "2":
            print("\nSelecione 3 pontos para a transformação afim.")
        else:  
            print("\nSelecione 4 pontos para a transformação.")
        
        cv2.setMouseCallback("Selecione os pontos", select_points)

        while (len(points) < 3 and choice == "2") or (len(points) < 4 and choice != "2"):  
            cv2.waitKey(1) 

        # Ordenando os pontos corretamente para transformação
        ordered_points = order_points(np.array(points, dtype="float32"))

        if choice == "2" and len(points) == 3:
            try:
                trans_x = float(input("Digite a translação no eixo X: "))
                trans_y = float(input("Digite a translação no eixo Y: "))
                scale_factor = float(input("Digite o fator de escala: "))
                angle = float(input("Digite o ângulo de rotação (em graus): "))
            except ValueError:
                print("Entrada inválida. Por favor, insira números válidos.")
                continue

            result = affine_with_params(image, ordered_points, trans_x, trans_y, scale_factor, angle)
            output_filename = "resultado_afim.jpeg"
        
        elif choice == "1" and len(points) == 4:
            # Use os pontos ordenados para calcular a transformação de perspectiva
            result = perspective_transform(image, ordered_points)
            output_filename = "resultado_perspectiva.jpeg"
        else:
            print("Seleção inválida ou pontos insuficientes!")
            continue

        if result is not None:
            cv2.imshow("Resultado da Retificação", result)
            cv2.imwrite(output_filename, result)
            print(f"Imagem resultante salva como {output_filename}")

            print("\nPressione qualquer tecla na imagem para voltar ao menu.")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Não foi possível aplicar a transformação.")

if __name__ == "__main__":
    main()
