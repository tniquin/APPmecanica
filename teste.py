import requests
def ExemploApi():
    url=f"http://10.135.232.28:5000/listarClientes"
    Resposta = requests.get(url)

    if Resposta.status_code == 200:
        lista_clientes=Resposta.json()
        for cliente in lista_clientes:
            print(f"nome {cliente['nome']}")
            print(f"cpf {cliente['cpf']}")
            print(f"telefone {cliente['telefone']}")
            print(f"endereco {cliente['endereco']}")
            print("-" * 20)
    else:
        print(f"Erro Numero invalido {Resposta.status_code}")

def ExemploPost():
    url=f"http://10.135.232.28:5000/adicionarVeiculo"

    nova_postagem = {
        "cliente_id": 1,  # Inteiro válido de um cliente já cadastrado
        "marca": "agaga",
        "modelo": "agua",
        "placa": "23345",
        "ano_fabricacao": 2000
    }

    resposta=requests.post(url, json=nova_postagem)
    if resposta.status_code == 201:
        dados_veiculo = resposta.json()
        print(dados_veiculo['mensagem'])
    else:
        print(f"Erro Número: {resposta.status_code}")
        print(resposta.json())  # Para mostrar a mensagem de erro do backend



def editar_cliente(id):
    url = f"http://10.135.232.28:5000/editarClients/{id}"  # Altere se sua API estiver em outra porta ou host

    novos_dados = {
        "nome": "João da Silva",
        "cpf": "12345678901",
        "telefone": "18991234567",
        "endereco": "Rua das Laranjeiras, 123"
    }


    resposta = requests.put(url, json=novos_dados)

    try:
        dados = resposta.json()
    except Exception:
        print("❌ Resposta não é JSON!")
        print("Resposta bruta:", resposta.text)
        return

    if resposta.status_code == 200:
        print("✅ Cliente editado com sucesso!")
        print("Resposta do servidor:", dados)
    else:
        print(f"❌ Erro ao editar cliente. Código {resposta.status_code}")
        print("Mensagem do servidor:", dados.get("mensagem", "Sem mensagem"))


#editar_cliente(1)
#ExemploApi()
#ExemploPost()
