import cv2
import numpy as np

# Função para capturar os pontos do mouse
points = []
def select_points(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Ponto selecionado: {(x, y)}")
    # Desenhar os pontos e as linhas enquanto os pontos estão sendo selecionados
    if len(points) > 0:
        temp_image = image.copy()  # Copiar a imagem original para desenhar nela
        # Desenhar todos os pontos já selecionados
        for i, point in enumerate(points):
            cv2.circle(temp_image, point, 5, (0, 0, 255), -1)  # Desenha um ponto vermelho
        # Se houver pelo menos dois pontos, desenhar linhas entre eles
        if len(points) > 1:
            for i in range(len(points) - 1):
                cv2.line(temp_image, points[i], points[i + 1], (0, 255, 0), 2)  # Linha verde
        # Se houver 4 pontos, desenhar o quadrado
        if len(points) == 4:
            cv2.line(temp_image, points[0], points[1], (255, 0, 0), 2)
            cv2.line(temp_image, points[1], points[2], (255, 0, 0), 2)
            cv2.line(temp_image, points[2], points[3], (255, 0, 0), 2)
            cv2.line(temp_image, points[3], points[0], (255, 0, 0), 2)
        # Exibir a imagem com os desenhos em tempo real
        cv2.imshow("Imagem - Selecione 4 pontos", temp_image)

# Função principal
if __name__ == "__main__":
    # Carregar a imagem PNG usando OpenCV
    try:
        image = cv2.imread('testando.png')  # Substitua pelo caminho do arquivo PNG
        if image is None:
            raise FileNotFoundError("Imagem não encontrada ou formato não suportado.")
    except Exception as e:
        print(f"Erro ao carregar a imagem PNG: {e}")
        exit()

    # Exibir a imagem e capturar os pontos
    cv2.imshow("Imagem - Selecione 4 pontos", image)
    cv2.setMouseCallback("Imagem - Selecione 4 pontos", select_points)

    print("Selecione 4 pontos na imagem para alinhar a perspectiva.")
    while len(points) < 4:
        cv2.waitKey(1)

    cv2.destroyAllWindows()

    # Definindo um tamanho fixo para a imagem transformada
    dst_width = 800  # Largura desejada após a transformação
    dst_height = 600  # Altura desejada após a transformação
    dst_points = [
        (0, 0),  # Canto superior esquerdo
        (dst_width - 1, 0),  # Canto superior direito
        (dst_width - 1, dst_height - 1),  # Canto inferior direito
        (0, dst_height - 1)  # Canto inferior esquerdo
    ]

    # Certificando-se que os pontos estão na ordem correta (horário ou anti-horário)
    points = np.array(points, dtype=np.float32)
    dst_points = np.array(dst_points, dtype=np.float32)

    # Calcular a matriz de transformação de perspectiva
    perspective_matrix = cv2.getPerspectiveTransform(points, dst_points)

    # Aplicar a transformação de perspectiva em toda a imagem
    transformed_image = cv2.warpPerspective(image, perspective_matrix, (dst_width, dst_height))

    # Exibir as imagens original e transformada
    cv2.imshow("Imagem Original", image)
    cv2.imshow("Imagem Retificada - Perspectiva Alinhada", transformed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
