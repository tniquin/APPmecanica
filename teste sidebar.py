import flet as ft


def main(page: ft.Page):
    page.title = "App de Busca com Rotas"

    # Função para montar a tela inicial (com barra de busca)
    def home_view():
        search_box = ft.TextField(label="Buscar", width=300, hint_text="Digite 'fruta' para ir à tela fruta")

        def on_search(e):
            query = search_box.value.strip().lower()
            if query == "fruta":
                page.go("/fruta")
            else:
                page.go("/nome")

        search_button = ft.ElevatedButton(text="Buscar", on_click=on_search)

        return ft.Column([
            ft.Text("Tela de Busca", size=30),
            search_box,
            search_button
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Tela /fruta
    def fruta_view():
        return ft.Column([
            ft.Text("Você está na tela FRUTA!", size=30),
            ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/"))
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Tela /nome
    def nome_view():
        return ft.Column([
            ft.Text("vc não fez o que fala e vc parou aqui!", size=30),
            ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/"))
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Roteamento de páginas
    def route_change(route):
        page.views.clear()
        if route == "/":
            page.views.append(ft.View("/", [home_view()]))
        elif route == "/fruta":
            page.views.append(ft.View("/fruta", [fruta_view()]))
        elif route == "/nome":
            page.views.append(ft.View("/nome", [nome_view()]))
        else:
            page.views.append(ft.View("/", [home_view()]))
        page.update()

    page.on_route_change = lambda route: route_change(page.route)
    page.on_view_pop = lambda view: page.go("/")

    # Começa na rota "/"
    page.go(page.route or "/")


ft.app(target=main)
