# Webscraper de filmes em cartaz no site do Estação Net Botafogo (apoie seu cinema de rua local!)

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    pagina = browser.new_page()

    pagina.goto("https://grupoestacao.com.br/em-cartaz/", wait_until="networkidle")

    resultados = {}  # Dicionário de filmes agrupados por categoria

    # Localiza todos os cabeçalhos de categoria (h3) que não estão ocultos
    elementos_categoria = pagina.locator('h3.col-sm-12:not([style*="display: none"])')

    for elemento_categoria in elementos_categoria.all():
        categoria = elemento_categoria.text_content().strip()  # Nome da categoria
        resultados[categoria] = []  # Lista de filmes da categoria

        # Constrói um XPath para selecionar os containers de filme relevantes após o cabeçalho da categoria.
        elementos_container_filme = pagina.locator(
            f'//h3[contains(@class, "col-sm-12") and not(contains(@style, "display: none")) and normalize-space()="{categoria}"]/following-sibling::div[contains(@class, "filme") and not(contains(@class, "pub"))][count(preceding-sibling::h3[contains(@class, "col-sm-12") and not(contains(@style, "display: none"))]) = count(//h3[contains(@class, "col-sm-12") and not(contains(@style, "display: none")) and normalize-space()="{categoria}"]/preceding-sibling::h3[contains(@class, "col-sm-12") and not(contains(@style, "display: none"))]) + 1]'
        )

        for container_filme in elementos_container_filme.all():
            elemento_titulo = container_filme.locator('h2.blacktitle')  # Título do filme.
            titulo_filme = elemento_titulo.text_content().strip() # Texto do título.

            # Verifica se o título é válido e se ainda não foi adicionado (evita duplicatas entre categorias).
            if titulo_filme and titulo_filme not in resultados[categoria]:
                resultados[categoria].append(titulo_filme)

    browser.close()

with open("filmes.txt", "w", encoding="utf-8") as f:
    for categoria, filmes in resultados.items():
        f.write(f"[{categoria}]\n")  # Escreve o cabeçalho da categoria.
        f.write("\n".join(filmes))   # Escreve a lista de filmes da categoria.
        f.write("\n\n")              # Adiciona linhas em branco para separar as categorias.