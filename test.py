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

# Funções para cada método de retificação
# 1. Retificação Perspectiva
def perspective_transform(image, points):
    ordered_pts = order_points(np.array(points, dtype="float32"))
    width, height = 500, 500

    dst_points = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")

    matrix = cv2.getPerspectiveTransform(ordered_pts, dst_points)
    result = cv2.warpPerspective(image, matrix, (width, height))
    return result

# 2. Retificação Afim (Affine Transform)
def affine_transform(image, points):
    if len(points) < 3:
        print("A transformação afim requer exatamente 3 pontos.")
        return None

    pts_src = np.array(points[:3], dtype="float32")
    pts_dst = np.array([
        [0, 0],
        [300, 0],
        [0, 300]
    ], dtype="float32")

    matrix = cv2.getAffineTransform(pts_src, pts_dst)
    result = cv2.warpAffine(image, matrix, (300, 300))
    return result

# Função para aplicar translação, escala e rotação na transformação afim
def affine_with_params(image, points, trans_x, trans_y, scale_factor, angle):
    # Validando os valores de translação, escala e rotação
    if not isinstance(trans_x, (int, float)) or not isinstance(trans_y, (int, float)):
        print("A translação precisa ser um número.")
        return None
    if not isinstance(scale_factor, (int, float)) or scale_factor <= 0:
        print("O fator de escala precisa ser um número positivo.")
        return None
    if not isinstance(angle, (int, float)):
        print("O ângulo precisa ser um número.")
        return None

    pts_src = np.array(points[:3], dtype="float32")
    pts_dst = np.array([
        [0, 0],
        [300, 0],
        [0, 300]
    ], dtype="float32")
    
    matrix = cv2.getAffineTransform(pts_src, pts_dst)
    matrix_3x3 = np.vstack([matrix, [0, 0, 1]])

    # Criando matriz de rotação e escala
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    rot_scale_matrix = cv2.getRotationMatrix2D(center, angle, scale_factor)
    rot_scale_matrix_3x3 = np.vstack([rot_scale_matrix, [0, 0, 1]])
    combined_matrix = np.dot(rot_scale_matrix_3x3, matrix_3x3)

    combined_matrix[0, 2] += trans_x
    combined_matrix[1, 2] += trans_y

    result = cv2.warpAffine(image, combined_matrix[:2], (w, h))
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

        # Menu para parâmetros de translação, escala e rotação para a transformação afim
        if choice == "2":
            try:
                trans_x = float(input("Digite a translação no eixo X: "))
                trans_y = float(input("Digite a translação no eixo Y: "))
                scale_factor = float(input("Digite o fator de escala: "))
                angle = float(input("Digite o ângulo de rotação (em graus): "))
            except ValueError:
                print("Entrada inválida. Por favor, insira números válidos.")
                continue

            result = affine_with_params(image, points, trans_x, trans_y, scale_factor, angle)
            output_filename = "resultado_afim.jpeg"
        
        # Executa o método escolhido
        elif choice == "1" and len(points) == 4:
            result = perspective_transform(image, points)
            output_filename = "resultado_perspectiva.jpeg"
        else:
            print("Seleção inválida ou pontos insuficientes!")
            continue

        if result is not None:
            cv2.imshow("Resultado da Retificação", result)
            cv2.imwrite(output_filename, result)
            print(f"Imagem salva como {output_filename}")

            # Espera até o usuário pressionar qualquer tecla para voltar ao menu
            print("\nPressione qualquer tecla para voltar ao menu.")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Não foi possível aplicar a transformação.")

if __name__ == "__main__":
    main()
