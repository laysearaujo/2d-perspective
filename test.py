import cv2
import numpy as np

# Função para capturar os pontos do mouse
points = []
selection_complete = False  # Variável para controlar quando a seleção estiver completa

def select_points(event, x, y, flags, param):
    global points, selection_complete, temp_image
    if not selection_complete and event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Ponto selecionado: {(x, y)}")

        # Desenhar os pontos e as linhas na imagem temporária
        temp_image = image.copy()  # Restaurar a imagem original para desenhar cada vez
        for i, point in enumerate(points):
            cv2.circle(temp_image, point, 20, (0, 0, 255), -1)  # Desenhar o ponto
        if len(points) > 1:
            for i in range(len(points) - 1):
                cv2.line(temp_image, points[i], points[i + 1], (0, 255, 0), 2)  # Linha verde
        if len(points) == 4:
            cv2.line(temp_image, points[0], points[1], (255, 0, 0), 2)
            cv2.line(temp_image, points[1], points[2], (255, 0, 0), 2)
            cv2.line(temp_image, points[2], points[3], (255, 0, 0), 2)
            cv2.line(temp_image, points[3], points[0], (255, 0, 0), 2)
            selection_complete = True

        # Atualizar a janela com os desenhos
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

    temp_image = image.copy()  # Criar uma cópia temporária para exibir os desenhos
    original_image = image.copy()  # Manter uma versão da imagem original para desenhar o quadrado final

    # Exibir a imagem e capturar os pontos
    cv2.imshow("Imagem - Selecione 4 pontos", temp_image)
    cv2.setMouseCallback("Imagem - Selecione 4 pontos", select_points)

    print("Selecione 4 pontos na imagem para alinhar a perspectiva.")
    while not selection_complete:
        cv2.waitKey(1)

    # Desenhar o quadrado final na imagem original
    cv2.line(original_image, points[0], points[1], (255, 0, 0), 2)
    cv2.line(original_image, points[1], points[2], (255, 0, 0), 2)
    cv2.line(original_image, points[2], points[3], (255, 0, 0), 2)
    cv2.line(original_image, points[3], points[0], (255, 0, 0), 2)

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

    # Exibir as três janelas
    # cv2.imshow("Imagem - Selecione 4 pontos", temp_image)  # Janela de seleção (finalizada)
    cv2.destroyAllWindows()
    cv2.imshow("Imagem Original com Quadrado", original_image)  # Original com o quadrado
    cv2.imshow("Imagem Retificada - Perspectiva Alinhada", transformed_image)  # Transformada
    cv2.waitKey(0)
    cv2.destroyAllWindows()