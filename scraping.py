import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

print("Travel")

sesion = requests.Session()
sesion.headers.update({"User-Agent": "Mozilla/5.0"})


def obtener_html(url):
    try:
        respuesta = sesion.get(url, timeout=10)
        respuesta.raise_for_status()
        return respuesta.text
    except Exception as error:
        print(f"Error al obtener la URL {url}: {error}")
        return None


def obtener_productos_de_pagina(url_pagina, html):
    sopa = BeautifulSoup(html, "html.parser")
    productos = []

    articulos = sopa.find_all("article", class_="product_pod")

    for articulo in articulos:
        enlace = articulo.select_one("h3 a")
        if not enlace or not enlace.get("href"):
            continue

        nombre = enlace.get("title", "").strip()
        url_producto = urljoin(url_pagina, enlace["href"])

        etiqueta_precio = articulo.find("p", class_="price_color")
        precio = etiqueta_precio.get_text(strip=True) if etiqueta_precio else ""

        etiqueta_stock = articulo.find("p", class_="instock availability")
        stock = (
            etiqueta_stock.get_text(strip=True) if etiqueta_stock else "No disponible"
        
        )
    
            
 

        info_producto = {
            "url": url_producto,
            "categoria": "Travel",
            "nombre": nombre,
            "precio": precio,
            "stock": stock,
        }
        

        print(f"Título: {info_producto['nombre']}")
        print(f"Precio: {info_producto['precio']}")
        print(f"Stock: {info_producto['stock']}")
        print(f"URL: {info_producto['url']}")
        print("-" * 40)

        productos.append(info_producto)

    return productos


def scrapear_todas_las_paginas(url_inicial):
    url_actual = url_inicial
    todos_los_productos = []
    contador_paginas = 0

    while url_actual:
        html = obtener_html(url_actual)
        if not html:
            break

        contador_paginas += 1
        print(f"\n=== PÁGINA {contador_paginas} ===\n")

        productos_pagina = obtener_productos_de_pagina(url_actual, html)
        todos_los_productos.extend(productos_pagina)

        sopa = BeautifulSoup(html, "html.parser")
        enlace_siguiente = sopa.select_one("li.next a")

        if enlace_siguiente and enlace_siguiente.get("href"):
            url_actual = urljoin(url_actual, enlace_siguiente["href"])
        else:
            url_actual = None

    return todos_los_productos, contador_paginas


url_inicial = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"

productos, total_paginas = scrapear_todas_las_paginas(url_inicial)

print(f"\nTotal de páginas: {total_paginas}")
print(f"Total de libros extraídos: {len(productos)}")
