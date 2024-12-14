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

---

## **Organização dos Resultados**
Para cada método:
1. Utilize a imagem **tabuleiro.jpeg** como entrada.
2. Salve o resultado em arquivos nomeados conforme o método aplicado:
   - `resultado_perspectiva.jpeg`
   - `resultado_afim.jpeg`
