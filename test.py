import cv2
import numpy as np

global points, method_choice
points = []  
method_choice = None 

# Função para capturar os pontos do mouse
def select_points(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN and len(points) < 4:
        points.append((x, y))
        print(f"Ponto selecionado: {(x, y)}")
        
        # Desenha o ponto selecionado
        cv2.circle(temp_image, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Selecione os pontos", temp_image)

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
    width, height = 500, 500  # Dimensão desejada para a saída

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

    pts_src = np.array(points[:3], dtype="float32")  # Pega os 3 primeiros pontos
    pts_dst = np.array([
        [0, 0],
        [300, 0],
        [0, 300]
    ], dtype="float32")

    matrix = cv2.getAffineTransform(pts_src, pts_dst)
    result = cv2.warpAffine(image, matrix, (300, 300))
    return result

# 3. Transformada de Escala e Rotação (Manual)
def scale_and_rotate(image, scale_factor, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    
    matrix = cv2.getRotationMatrix2D(center, angle, scale_factor)
    result = cv2.warpAffine(image, matrix, (w, h))
    return result

# Menu principal
def main():
    global points, temp_image

    image_path = "tabuleiro.jpeg"  # Altere conforme sua imagem
    image = cv2.imread(image_path)
    if image is None:
        print("Erro ao carregar a imagem!")
        return

    while True:
        print("\nEscolha o método de retificação:")
        print("1 - Retificação Perspectiva")
        print("2 - Transformada Afim")
        print("3 - Escala e Rotação Manual")
        print("0 - Sair")
        
        choice = input("Digite sua escolha: ")
        if choice == "0":
            break

        points = []
        temp_image = image.copy()
        cv2.imshow("Selecione os pontos", temp_image)
        cv2.setMouseCallback("Selecione os pontos", select_points)

        print("\nSelecione os pontos na imagem com o mouse.")
        cv2.waitKey(0)

        # Executa o método escolhido
        if choice == "1" and len(points) == 4:
            result = perspective_transform(image, points)
        elif choice == "2" and len(points) >= 3:
            result = affine_transform(image, points)
        elif choice == "3":
            scale = float(input("Fator de escala (ex: 1.2): "))
            angle = float(input("Ângulo de rotação (graus): "))
            result = scale_and_rotate(image, scale, angle)
        else:
            print("Seleção inválida ou pontos insuficientes!")
            continue

        if result is not None:
            cv2.imshow("Resultado da Retificacao", result)
            cv2.imwrite("resultado_retificacao.jpeg", result)
            print("Imagem salva como resultado_retificacao.jpeg")
        else:
            print("Não foi possível aplicar a transformação.")

        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
