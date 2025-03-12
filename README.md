# Gerador de QR Code para Itens
A funcionalidade nova consiste em uma arquitetura serverless na AWS que gera QR Codes para itens identificados por UUIDs. Quando a função generateContent é chamada, ela gera um UUID para o item, chama a função generateQrCodeFunction para criar um QR Code, salva a imagem no S3 e retorna no response o caminho da imagem junto com as informações do item.

## Como Funciona
### Fluxo do Sistema
1. Utilização do sistema:
    - A url pre assinada é gerada
    - O usuario envia a imagem na url pre assinada
    - Os dados irão para a fila SQS
    - A função generateContent é acionada de acordo com a quantidade de itens na fila. 
    - Um UUID4 é gerado para o item.
    - A lambda generateQrContent é chamada passando o uuid por parametro (payload)
    - O qr code é gerado e salvo no bucket s3 do qrcode e o path retornado para a lambda anterior (generateContent).
    - As informações do item são salvas em um banco de dados junto com o path do qrcode.
    - O usuario pode usar a lambda de get products para visualizar as informações

2. Geração do QR Code:
    - A lambda generateContent aciona a lambda generateQrCode passando o uuid por payload
    - A função generateQrCodeFunction recebe o UUID4.
    - Um QR Code é gerado contendo o UUID4.
    - A imagem do QR Code é salva em um bucket S3.
    - O caminho (path) da imagem no S3 é retornado para a função generateContent para salvar posteriormente.

3. Resposta Final:
    - A função generateContent recebe o caminho do QR Code.
    - As informações do item e o caminho do QR Code são salvos no bucket.

## Instruções para Testes
- Gerar o QR Code:  Apenas realizar a chamada padrão
    1. Gerar a url pre assinada\
    `https://eqztu7afs5.execute-api.us-east-2.amazonaws.com/Prod/presigned-url?fileName=nomedoarquivo.png&contentType=image/png`
    2. Enviar a imagem na url pre assinada (de preferência em formato .png)
    3. O response retornará o caminho que a imagem foi gerada e salva no item "qrcode" e o usuário poderá visualizar a imagem no navegador.
- Chamada ao "Get All"
    1. A url termina com "/products"\
    `https://eqztu7afs5.execute-api.us-east-2.amazonaws.com/Prod/products`
- Chamada a um item "Get By Id", por exemplo:
    1. A url termina com "/products/{id}"\
    `https://eqztu7afs5.execute-api.us-east-2.amazonaws.com/Prod/products/37e96b3d-cf70-4995-b6b1-dddab5211be8`