import flet as ft
import requests


def main(page: ft.Page):
    page.title = "Gerenciador de Clientes"
    page.theme_mode = "light"
    page.padding = 30

    token = None

    def get_token():
        global token
        return token

    def set_token(new_token):
        global token
        token = new_token



    #CLIENTE
    def ir_para_clientes(e):
        page.go("/clientes")

    def ir_listar_clientes(e):
        page.go("/listar_clientes")

    def ir_para_adicionar(e):
        page.go("/adicionar")

    def ir_para_editar(e):
        page.go("/editar")

    #VEICULO

    def ir_para_veiculos(e):
        page.go("/veiculos")

    def listar_veiculos(e):
        page.go("/listar_veiculos")

    def adicionar_veiculo(e):
        page.go("/adicionar_veiculo")

    def editar_veiculo(e):
        page.go("/editar_veiculo")


    #SERVIÇÕS
    def ir_para_servico(e):
        page.go("/servicos")

    def listar_servicos(e):
        page.go("/listar_servicos")

    def adicionar_servico(e):
        page.go("/adicionar_servico")

    def editar_servico(e):
        page.go("/editar_servico")


    #Usuario
    def usuario(e):
        page.go("/usuario")

    def cadastro(e):
        page.go("/cadastro")

    def login(e):
        page.go("/login")

    def listar_usuario(e):
        page.go("/listar_usuarios")


    def rota_mudou(route):
        page.views.clear()

        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    controls=[
                        ft.Text("Bem-vindo!", size=30),
                        ft.ElevatedButton("Clientes", on_click=ir_para_clientes),
                        ft.ElevatedButton("Veiculos", on_click=ir_para_veiculos),
                        ft.ElevatedButton("Serviços", on_click=ir_para_servico),
                        ft.ElevatedButton("Usuario", on_click=usuario),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        if page.route == "/login":
            # Tela de Login
            email = ft.TextField(label="Email", autofocus=True)
            password = ft.TextField(label="Senha", password=True)
            login_result = ft.Text("")

            def verificar_login(e):
                dados = {
                    "email": email.value,
                    "senha": password.value,
                }
                try:
                    resposta = requests.post("http://10.135.232.28:5000/login", json=dados)
                    print(resposta.text)
                    if resposta.status_code == 200:
                        set_token(resposta.json().get('token'))
                        page.go("/home")  # Redireciona para a tela de clientes
                    else:
                        login_result.value = f"Erro: {resposta.status_code} - {resposta.text}"
                except requests.exceptions.RequestException as err:  # Tratamento de erros de requisição
                    login_result.value = f"Erro na requisição: {err}"
                except ValueError:  # Tratamento de erros de JSON
                    login_result.value = "Erro: Resposta inválida do servidor"
                except Exception as err:
                    login_result.value = f"Erro inesperado: {err}"
                except Exception as err:
                    login_result.value = f"Erro inesperado: {err}", 500
                page.update()

            page.views.append(
                ft.View(
                    "/login",
                    controls=[
                        ft.Text("Login", size=30, weight="bold"),
                        email, password,
                        ft.ElevatedButton("Entrar", on_click=verificar_login),
                        login_result,
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        elif page.route == "/clientes":
            page.views.append(
                ft.View(
                    controls=[
                        ft.Text("clientes!", size=30),
                        ft.ElevatedButton("Ver Clientes", on_click=ir_listar_clientes),
                        ft.ElevatedButton("Adicionar Cliente", on_click=ir_para_adicionar),
                        ft.ElevatedButton("Editar Cliente", on_click=ir_para_editar),
                        ft.ElevatedButton("HOME", on_click=lambda e: page.go("/home")),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                )

            ),


        elif page.route == "/listar_clientes":
            try:
                resposta = requests.get("http://10.135.232.28:5000/listarClientes",
                                        headers={"Authorization": f"Bearer {get_token()}"})
                dados = resposta.json()
                clientes = [
                    ft.Text(
                        f"Nome: {c['nome']} | CPF: {c['cpf']} | Tel: {c['telefone']} | Endereço: {c['endereco']}"
                    )
                    for c in dados
                ]
            except Exception as err:
                clientes = [ft.Text(f"Erro ao buscar clientes: {err}")]

            page.views.append(
                ft.View(
                    "/clientes",
                    controls=[
                        ft.Text("Lista de Clientes", size=25, weight="bold"),
                        ft.Column(clientes, scroll=ft.ScrollMode.ALWAYS),
                        ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/clientes")),
                    ],
                )
            )

        elif page.route == "/adicionar":

            nome = ft.TextField(label="Nome")
            cpf = ft.TextField(label="CPF")
            telefone = ft.TextField(label="Telefone")
            endereco = ft.TextField(label="Endereço")
            resultado = ft.Text("")

            def enviar_dados(e):
                dados = {
                    "nome": nome.value,
                    "cpf": cpf.value,
                    "telefone": telefone.value,
                    "endereco": endereco.value,
                }
                try:
                    r = requests.post("http://10.135.232.28:5000/adicionarClientes", json=dados,
                                      headers={"Authorization": f"Bearer {get_token()}"})
                    if r.status_code == 201:
                        resultado.value = "Cliente cadastrado com sucesso!"
                    else:
                        resultado.value = f"Erro: {r.json().get('mensagem', r.text)}"
                except Exception as err:
                    resultado.value = f"Erro na requisição: {err}"
                page.update()

            page.views.append(
                ft.View(
                    "/adicionar",
                    controls=[
                        ft.Text("Adicionar Novo Cliente", size=25, weight="bold"),
                        nome, cpf, telefone, endereco,
                        ft.ElevatedButton("Enviar", on_click=enviar_dados),
                        resultado,
                        ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/clientes")),
                    ],
                )
            )

        elif page.route == "/editar":
            id_cliente = ft.TextField(label="ID do Cliente para editar", width=200)
            nome = ft.TextField(label="Nome")
            cpf = ft.TextField(label="CPF")
            telefone = ft.TextField(label="Telefone")
            endereco = ft.TextField(label="Endereço")
            resultado = ft.Text("")

            def buscar_cliente(e):
                try:
                    r = requests.get(f"http://10.135.232.28:5000/listarClientes",
                                     headers={"Authorization": f"Bearer {get_token()}"})
                    if r.status_code == 200:
                        clientes = r.json()
                        cliente = next((c for c in clientes if c["id_cliente"] == int(id_cliente.value)), None)
                        if cliente:
                            nome.value = cliente["nome"]
                            cpf.value = cliente["cpf"]
                            telefone.value = cliente["telefone"]
                            endereco.value = cliente["endereco"]
                            resultado.value = "Cliente encontrado. Edite os dados e clique em salvar."
                        else:
                            resultado.value = "Cliente não encontrado."
                    else:
                        resultado.value = f"Erro ao buscar cliente: {r.status_code}"
                except Exception as err:
                    resultado.value = f"Erro: {err}"
                page.update()

            def salvar_edicao(e):
                if not id_cliente.value.strip():
                    resultado.value = "Informe o ID do cliente para editar."
                    page.update()
                    return

                dados = {
                    "nome": nome.value,
                    "cpf": cpf.value,
                    "telefone": telefone.value,
                    "endereco": endereco.value,
                }
                try:
                    r = requests.put(f"http://10.135.232.28:5000/editarClients/{id_cliente.value}", json=dados,
                                     headers={"Authorization": f"Bearer {get_token()}"})
                    if r.status_code == 200:
                        resultado.value = "Cliente editado com sucesso!"
                    elif r.status_code == 404:
                        resultado.value = "Cliente não encontrado."
                    else:
                        resultado.value = f"Erro: {r.json().get('mensagem', r.text)}"
                except Exception as err:
                    resultado.value = f"Erro na requisição: {err}"
                page.update()

            page.views.append(
                ft.View(
                    "/editar",
                    controls=[
                        ft.Text("Editar Cliente", size=25, weight="bold"),
                        id_cliente,
                        ft.ElevatedButton("Buscar Cliente", on_click=buscar_cliente),
                        nome, cpf, telefone, endereco,
                        ft.ElevatedButton("Salvar", on_click=salvar_edicao),
                        resultado,
                        ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/clientes")),
                    ],
                )
            )

        elif page.route == "/veiculos":
            page.views.append(
                ft.View(
                    controls=[
                        ft.Text("Veiculos!", size=30),
                        ft.ElevatedButton("Ver veiculos", on_click=listar_veiculos),
                        ft.ElevatedButton("Adicionar veiculo", on_click=adicionar_veiculo),
                        ft.ElevatedButton("Editar veiculo", on_click=editar_veiculo),
                        ft.ElevatedButton("HOME", on_click=lambda e: page.go("/")),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )

            ),


        elif page.route == "/listar_veiculos":
            try:
                resposta = requests.get("http://10.135.232.28:5000/listarVeiculos",  headers={"Authorization": f"Bearer {get_token()}"})
                dados = resposta.json()
                veiculos = [
                    ft.Text(
                        f"Modelo: {v['modelo']} | Marca: {v['marca']} | Placa: {v['placa']} | é do cliente: {v['cliente_id']}"
                    )
                    for v in dados
                ]
            except Exception as err:
                veiculos = [ft.Text(f"Erro ao buscar veiculos: {err}")]

            page.views.append(
                ft.View(
                    "/listar_veiculos",
                    controls=[
                        ft.Text("Lista de Veiculos", size=25, weight="bold"),
                        ft.Column(veiculos, scroll=ft.ScrollMode.ALWAYS),
                        ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/veiculos")),
                    ],
                )
            )
        elif page.route == "/adicionar_veiculo":
            modelo = ft.TextField(label="Modelo")
            marca = ft.TextField(label="Marca ")
            placa = ft.TextField(label="Placa")
            ano_fabricacao = ft.TextField(label="Ano de Fabricação ")
            cliente_id = ft.TextField(label="Qual o id do cliente?")
            resultado = ft.Text("")

            def enviar_dados(e):
                dados = {
                    "modelo": modelo.value,
                    "marca": marca.value,
                    "placa": placa.value,
                    "ano_fabricacao": ano_fabricacao.value,
                    "cliente_id": cliente_id.value,
                }
                try:
                    r = requests.post("http://10.135.232.28:5000/adicionarVeiculo", json=dados,
                                      headers={"Authorization": f"Bearer {get_token()}"})
                    if r.status_code == 201:
                        resultado.value = "carro cadastrado com sucesso!"
                    else:
                        resultado.value = f"Erro: {r.json().get('mensagem', r.text)}"
                except Exception as err:
                    resultado.value = f"Erro na requisição: {err}"
                page.update()

            page.views.append(
                ft.View(
                    "/adicionar_veiculo",
                    controls=[
                        ft.Text("Adicionar Novo veiculo", size=25, weight="bold"),
                        modelo, marca, placa, ano_fabricacao, cliente_id,
                        ft.ElevatedButton("Enviar", on_click=enviar_dados),
                        resultado,
                        ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/veiculos")),
                    ],
                )
            )
        elif page.route == "/editar_veiculo":
            id_veiculo = ft.TextField(label="ID do veiculo para editar", width=250)
            modelo = ft.TextField(label="Modelo")
            marca = ft.TextField(label="Marca ")
            placa = ft.TextField(label="Placa")
            ano_fabricacao = ft.TextField(label="Ano de Fabricação ")

            resultado = ft.Text("")

            def buscar_veiculo(e):
                try:
                    r = requests.get(f"http://10.135.232.28:5000/listarVeiculos",
                                     headers={"Authorization": f"Bearer {get_token()}"})
                    if r.status_code == 200:
                        veiculos = r.json()
                        veiculo = next((v for v in veiculos if v["id_veiculo"] == int(id_veiculo.value)), None)
                        if veiculo:
                            modelo.value = veiculo["modelo"]
                            marca.value = veiculo["marca"]
                            ano_fabricacao.value = veiculo["ano_fabricacao"]
                            placa.value = veiculo["placa"]
                            resultado.value = "Veiculo encontrado. Edite os dados e clique em salvar."
                        else:
                            resultado.value = "veiculo não encontrado."
                    else:
                        resultado.value = f"Erro ao buscar veiculo: {r.status_code}"
                except Exception as err:
                    resultado.value = f"Erro: {err}"
                page.update()

            def salvar_edicao(e):
                if not id_veiculo.value.strip():
                    resultado.value = "Informe o ID do veiculo para editar."
                    page.update()
                    return

                dados = {
                    "modelo": modelo.value,
                    "marca": marca.value,
                    "placa": placa.value,
                    "ano_fabricacao": ano_fabricacao.value,
                }
                try:
                    r = requests.put(f"http://10.135.232.28:5000/editarVeiculos/{id_veiculo.value}", json=dados,
                                     headers={"Authorization": f"Bearer {get_token()}"})
                    if r.status_code == 200:
                        resultado.value = "Veiculo editado com sucesso!"
                    elif r.status_code == 404:
                        resultado.value = "Veiculo não encontrado."
                    else:
                        resultado.value = f"Erro: {r.json().get('mensagem', r.text)}"
                except Exception as err:
                    resultado.value = f"Erro na requisição: {err}"
                page.update()

            page.views.append(
                ft.View(
                    "/editar_veiculo",
                    controls=[
                        ft.Text("Editar veiculo", size=25, weight="bold"),
                        id_veiculo,
                        ft.ElevatedButton("Buscar veiculo", on_click=buscar_veiculo),
                        modelo, marca, placa, ano_fabricacao,
                        ft.ElevatedButton("Salvar", on_click=salvar_edicao),
                        resultado,
                        ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/veiculos")),
                    ],
                )
            )

        elif page.route == "/servicos":
            page.views.append(
                ft.View(
                    controls=[
                        ft.Text("serviços!", size=30),
                        ft.ElevatedButton("Ver serviços", on_click=listar_servicos),
                        ft.ElevatedButton("Adicionar serviços", on_click=adicionar_servico),
                        ft.ElevatedButton("Editar serviços", on_click=editar_servico),
                        ft.ElevatedButton("HOME", on_click=lambda e: page.go("/")),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                )

            ),
        elif page.route == "/listar_servicos":
            try:
                resposta = requests.get("http://10.135.232.28:5000/listarOrdemServicos",  headers={"Authorization": f"Bearer {get_token()}"})
                dados = resposta.json()
                servicos = [
                    ft.Text(
                        f"Data de abertura: {s['data_abertura']} "
                        f"| descricao de servico: {s['descricao_servico']}"
                        f" | status: {s['status']}"
                        f" | valor estimado {s['valor_estimado']} "
                        f"| id do veiculo: {s['veiculo_id']}"
                    )
                    for s in dados
                ]
            except Exception as err:
                servicos = [ft.Text(f"Erro ao buscar clientes: {err}")]

            page.views.append(
                ft.View(
                    "/listar_servicos",
                    controls=[
                        ft.Text("Lista de Serviços", size=25, weight="bold"),
                        ft.Column(servicos, scroll=ft.ScrollMode.ALWAYS),
                        ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/servicos")),
                    ],
                )
            )

        elif page.route == "/adicionar_servico":
            valor_estimado = ft.TextField(label="valor estimado")
            status = ft.TextField(label="status")
            descricao_servico = ft.TextField(label="descricao do servico")
            data_abertura = ft.TextField(label="data de abertura ")
            veiculo_id = ft.TextField(label="Qual o id do veiculo?")
            resultado = ft.Text("")

            def enviar_dados(e):
                dados = {
                    "valor_estimado": valor_estimado.value,
                    "status": status.value,
                    "descricao_servico": descricao_servico.value,
                    "data_abertura": data_abertura.value,
                    "veiculo_id": veiculo_id.value,
                }
                try:
                    r = requests.post("http://10.135.232.28:5000/adicionarOrdemServico", json=dados,
                                      headers={"Authorization": f"Bearer {get_token()}"})
                    if r.status_code == 201:
                        resultado.value = "serviço cadastrado com sucesso!"
                    else:
                        resultado.value = f"Erro: {r.json().get('mensagem', r.text)}"
                except Exception as err:
                    resultado.value = f"Erro na requisição: {err}"
                page.update()

            page.views.append(
                ft.View(
                    "/adicionar_servico",
                    controls=[
                        ft.Text("Adicionar Novo serviço", size=25, weight="bold"),
                        valor_estimado, status, descricao_servico, data_abertura, veiculo_id,
                        ft.ElevatedButton("Enviar", on_click=enviar_dados),
                        resultado,
                        ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/servicos")),
                    ],
                )
            )

        elif page.route == "/editar_servico":
            id_servico = ft.TextField(label="ID do servico para editar", width=250)
            valor_estimado = ft.TextField(label="Valor estimado")
            descricao_servico = ft.TextField(label="Descricao do servico")
            data_abertura = ft.TextField(label="Data de abertura")
            status = ft.TextField(label="Status ")

            resultado = ft.Text("")

            def buscar_servico(e):
                try:
                    r = requests.get(f"http://10.135.232.28:5000/listarOrdemServicos",
                                     headers={"Authorization": f"Bearer {get_token()}"})
                    if r.status_code == 200:
                        servicos = r.json()
                        servico = next((s for s in servicos if s["id_servico"] == int(id_servico.value)), None)
                        if servico:
                            valor_estimado.value = servico["valor_estimado"]
                            status.value = servico["status"]
                            descricao_servico.value = servico["descricao_servico"]
                            data_abertura.value = servico["data_abertura"]
                            resultado.value = "Veiculo encontrado. Edite os dados e clique em salvar."
                        else:
                            resultado.value = "veiculo não encontrado."
                    else:
                        resultado.value = f"Erro ao buscar veiculo: {r.status_code}"
                except Exception as err:
                    resultado.value = f"Erro: {err}"
                page.update()

            def salvar_edicao(e):
                if not id_servico.value.strip():
                    resultado.value = "Informe o ID do veiculo para editar."
                    page.update()
                    return

                dados = {
                    "valor_estimado": valor_estimado.value,
                    "status": status.value,
                    "descricao_servico": descricao_servico.value,
                    "data_abertura": data_abertura.value,
                }
                try:
                    r = requests.put(f"http://10.135.232.28:5000/editarServico/{id_servico.value}", json=dados,
                                     headers={"Authorization": f"Bearer {get_token()}"})
                    if r.status_code == 200:
                        resultado.value = "servico editado com sucesso!"
                    elif r.status_code == 404:
                        resultado.value = "servico não encontrado."
                    else:
                        resultado.value = f"Erro: {r.json().get('mensagem', r.text)}"
                except Exception as err:
                    resultado.value = f"Erro na requisição: {err}"
                page.update()

            page.views.append(
                ft.View(
                    "/editar_servico",
                    controls=[
                        ft.Text("Editar veiculo", size=25, weight="bold"),
                        id_servico,
                        ft.ElevatedButton("Buscar veiculo", on_click=buscar_servico),
                        valor_estimado, status, descricao_servico, data_abertura,
                        ft.ElevatedButton("Salvar", on_click=salvar_edicao),
                        resultado,
                        ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/servicos")),
                    ],
                )
            )

        elif page.route == "/usuario":
            page.views.append(
                ft.View(
                    controls=[
                        ft.Text("usuarios!", size=30),
                        ft.ElevatedButton("Ver usuarios", on_click=listar_usuario),
                        ft.ElevatedButton("Cadastrar usuarios", on_click=cadastro),
                        ft.ElevatedButton("login", on_click=login),
                        ft.ElevatedButton("HOME", on_click=lambda e: page.go("/")),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                )

            ),

        elif page.route == "/cadastro":
            nome = ft.TextField(label="Nome")
            email = ft.TextField(label="Email ")
            cpf = ft.TextField(label="CPF")
            password = ft.TextField(label="Senha")
            papel=ft.TextField(label="Papel")
            resultado = ft.Text("")

            def enviar_dados(e):
                dados = {
                    "nome": nome.value,
                    "email": email.value,
                    "cpf": cpf.value,
                    "password": password.value,
                    "papel": papel.value,
                }
                try:
                    r = requests.post("http://10.135.232.28:5000/cadastro_usuario", json=dados)
                    if r.status_code == 201:
                        resultado.value = "usuario cadastrado com sucesso!"
                    else:
                        resultado.value = f"Erro: {r.json().get('mensagem', r.text)}"
                except Exception as err:
                    resultado.value = f"Erro na requisição: {err}"
                page.update()

            page.views.append(
                ft.View(
                    "/cadastro",
                    controls=[
                        ft.Text("Adicionar Novo Usuario", size=25, weight="bold"),
                        nome, email, cpf, password, papel,
                        ft.ElevatedButton("Enviar", on_click=enviar_dados),
                        resultado,
                        ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/usuario")),
                    ],
                )
            )

        elif page.route == "/listar_usuarios":
            try:
                resposta = requests.get("http://10.135.232.28:5000/listarUsuario",
                                        headers={"Authorization": f"Bearer {get_token()}"})
                dados = resposta.json()
                usuarios = [
                    ft.Text(
                        f"Nome: {u['nome']} | CPF: {u['cpf']} | Email: {u['email']} | Função: {u['papel']}"
                    )
                    for u in dados
                ]
            except Exception as err:
                usuarios = [ft.Text(f"Erro ao buscar usuario: {err}")]

            page.views.append(
                ft.View(
                    "/listar_usuarios",
                    controls=[
                        ft.Text("Lista de Usuarios", size=25, weight="bold"),
                        ft.Column(usuarios, scroll=ft.ScrollMode.ALWAYS),
                        ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/usuario")),
                    ],
                )
            )



        elif page.route == "/home":
            page.views.append(
                ft.View(
                    "/home",
                    controls=[
                        ft.Text("Bem-vindo!", size=30),
                        ft.ElevatedButton("Clientes", on_click=ir_para_clientes),
                        ft.ElevatedButton("Veiculos", on_click=ir_para_veiculos),
                        ft.ElevatedButton("Serviços", on_click=ir_para_servico),
                        ft.ElevatedButton("Usuario", on_click=usuario),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

        page.update()

    page.on_route_change = rota_mudou
    page.go("/")


ft.app(target=main)
