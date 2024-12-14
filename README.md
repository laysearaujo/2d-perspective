## Retificação 2D: Métodos, Exemplos e Resultados

### **1. Transformação de Perspectiva**
- **Objetivo**: Corrigir a perspectiva de uma imagem distorcida, transformando um plano inclinado para uma visão "reta".
- **Entrada**: Uma imagem inclinada, onde o usuário seleciona **4 pontos** correspondentes a um retângulo.
- **Parâmetros**: Coordenadas dos 4 pontos (mouse).
- **Resultado Final**:
   - A imagem retificada deve apresentar a região plana sem distorções.
   - Exemplo: Um tabuleiro de xadrez inclinado sendo corrigido.

#### **Exemplo**:
- **Imagem de Entrada**: Uma foto do tabuleiro com perspectiva inclinada (como a "tabuleiro.jpeg").
- **Resultado Esperado**: O tabuleiro aparece **plano e alinhado**.

#### **Implementação Manual**:
A transformação de perspectiva foi implementada manualmente para proporcionar um maior controle sobre o processo. Ao invés de usar a função `cv2.getPerspectiveTransform` e `cv2.warpPerspective` do OpenCV, a transformação foi realizada da seguinte maneira:

- **Cálculo da Matriz de Transformação**: Usamos as fórmulas para calcular a matriz de transformação de perspectiva com base nos 4 pontos selecionados pelo usuário. A matriz foi construída manualmente e aplicada à imagem para corrigir a distorção de perspectiva.

- **Aplicação da Transformação**: A transformação foi aplicada pixel por pixel, utilizando a matriz de transformação calculada.


---

### **2. Transformação Afim**
- **Objetivo**: Corrigir distorções como **translação, escala e rotação**, mas **não perspectiva**.
- **Entrada**: Uma imagem que possui algum deslocamento ou rotação.
- **Parâmetros**: **3 pontos** correspondentes entre a imagem de origem e destino.
- **Resultado Final**:
   - A imagem será corrigida para alinhar deslocamento, rotação e escala.
   - Exemplo: Uma foto levemente rotacionada sendo "endireitada".

#### **Exemplo**:
- **Imagem de Entrada**: Foto de um documento ou quadro ligeiramente inclinado.
- **Resultado Esperado**: A imagem será **alinhada horizontalmente**, mantendo sua forma retangular.

### **Implementação Manual**:
A transformação afim foi implementada manualmente para melhor controle e entendimento dos cálculos envolvidos. Ao invés de usar a função `cv2.getAffineTransform` e `cv2.warpAffine` do OpenCV, a transformação foi realizada da seguinte forma:

- **Matriz de Rotação e Escala**: Calculamos a matriz de rotação e escala manualmente, usando o centro da imagem para aplicar as transformações de rotação e escala.

- **Adição de Translação**: A translação foi integrada à matriz de transformação, ajustando a posição da imagem de acordo com os parâmetros fornecidos.

- **Aplicação da Transformação**: A transformação foi aplicada pixel por pixel, alterando as coordenadas de cada ponto da imagem com base na matriz calculada.

---

## **Organização dos Resultados**
Para cada método:
1. Utilize a imagem **tabuleiro.jpeg** como entrada.
2. Salve o resultado em arquivos nomeados conforme o método aplicado:
   - `resultado_perspectiva.jpeg`
   - `resultado_afim.jpeg`
