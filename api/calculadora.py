import html
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs


# ==========================================
# CATALOGO DE PRODUCTOS
# ==========================================

PRODUCTOS = {
    "conjunto_urbano": {
        "nombre": "Conjunto Urbano",
        "precio": 90000
    },

    "vestido_sensacion": {
        "nombre": "Vestido Sensación",
        "precio": 80000
    },

    "outfit_chic": {
        "nombre": "Outfit Chic",
        "precio": 75000
    },

    "set_flower": {
        "nombre": "Set flower",
        "precio": 97000
    }
}


# ==========================================
# CODIGOS DE DESCUENTO
# ==========================================

DESCUENTOS = {
    "URBANIA20": 20
}


# ==========================================
# FUNCION PARA FORMATEAR PRECIOS
# ==========================================

def formato_pesos(valor):
    return "$" + format(valor, ",").replace(",", ".")


# ==========================================
# PLANTILLA HTML PARA LOS RESULTADOS
# ==========================================

def crear_pagina(contenido):

    return f"""<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Resultado de compra | Urbania Girls</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">

    <style>

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            padding: 30px 15px;
            background: #fff8f5;
            color: #40343a;
            font-family: 'Poppins', Arial, sans-serif;
        }}

        .contenedor {{
            width: 100%;
            max-width: 650px;
            margin: 35px auto;
            padding: 35px;
            background: white;
            border-radius: 22px;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.10);
            border-top: 5px solid #e8a6b8;
        }}

        h1 {{
            color: #b66d89;
            font-family: 'Playfair Display', serif;
            font-size: 32px;
            text-align: center;
        }}

        h2 {{
            color: #40343a;
            font-size: 19px;
        }}

        p {{
            line-height: 1.7;
        }}

        .detalle {{
            display: flex;
            justify-content: space-between;
            gap: 15px;
            padding: 14px 0;
            border-bottom: 1px solid #f0e4e9;
        }}

        .detalle strong {{
            color: #40343a;
        }}

        .total {{
            margin-top: 25px;
            padding: 22px;
            background: #fff0f4;
            border-radius: 14px;
            text-align: center;
        }}

        .total strong {{
            display: block;
            margin-top: 8px;
            color: #b66d89;
            font-size: 30px;
        }}

        .mensaje {{
            margin-top: 20px;
            padding: 14px;
            background: #fff8f5;
            border-radius: 10px;
            font-size: 14px;
        }}

        .boton {{
            display: block;
            margin-top: 25px;
            padding: 14px;
            background: #b66d89;
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 30px;
            font-weight: 600;
            transition: background 0.3s;
        }}

        .boton:hover {{
            background: #96536e;
        }}

        @media (max-width: 480px) {{

            .contenedor {{
                padding: 22px;
                margin: 10px auto;
            }}

            h1 {{
                font-size: 26px;
            }}

            .detalle {{
                font-size: 14px;
            }}

            .total strong {{
                font-size: 25px;
            }}

        }}

    </style>

</head>

<body>

    <main class="contenedor">

        {contenido}

        <a href="/#calculadora" class="boton">
            Volver a la calculadora
        </a>

    </main>

</body>
</html>"""


# ==========================================
# FUNCION PRINCIPAL DE VERCEL
# ==========================================

class handler(BaseHTTPRequestHandler):

    # --------------------------------------
    # ENVIAR RESPUESTA HTML
    # --------------------------------------

    def enviar_html(self, contenido, estado=200):

        pagina = crear_pagina(contenido)
        datos = pagina.encode("utf-8")

        self.send_response(estado)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(datos))
        )

        self.end_headers()

        self.wfile.write(datos)


    # --------------------------------------
    # CUANDO SE ABRE EL ENDPOINT
    # --------------------------------------

    def do_GET(self):

        contenido = """
        <h1>Urbania Girls</h1>

        <p>
            Para calcular el valor de tu compra,
            regresa a la tienda y completa el formulario.
        </p>
        """

        self.enviar_html(contenido)


    # --------------------------------------
    # RECIBIR Y PROCESAR EL FORMULARIO
    # --------------------------------------

    def do_POST(self):

        try:

            # Leer los datos enviados desde HTML
            longitud = int(self.headers.get("Content-Length", 0))

            cuerpo = self.rfile.read(longitud).decode("utf-8")

            formulario = parse_qs(cuerpo)

            # Obtener los valores del formulario
            producto_id = formulario.get("producto", [""])[0]

            cantidad_texto = formulario.get("cantidad", [""])[0]

            codigo = formulario.get("descuento", [""])[0].strip().upper()


            # ----------------------------------
            # VALIDAR EL PRODUCTO
            # ----------------------------------

            if producto_id not in PRODUCTOS:

                raise ValueError(
                    "Debes seleccionar un producto válido."
                )


            # ----------------------------------
            # VALIDAR LA CANTIDAD
            # ----------------------------------

            try:

                cantidad = int(cantidad_texto)

            except ValueError:

                raise ValueError(
                    "La cantidad debe ser un número entero."
                )


            if cantidad < 1 or cantidad > 99:

                raise ValueError(
                    "La cantidad debe estar entre 1 y 99."
                )


            # ----------------------------------
            # OBTENER PRODUCTO Y PRECIO
            # ----------------------------------

            producto = PRODUCTOS[producto_id]

            nombre = producto["nombre"]

            precio = producto["precio"]


            # ----------------------------------
            # CALCULAR SUBTOTAL
            # ----------------------------------

            subtotal = precio * cantidad


            # ----------------------------------
            # VALIDAR DESCUENTO
            # ----------------------------------

            porcentaje = 0

            mensaje_descuento = "No se aplicó ningún descuento."

            if codigo:

                if codigo in DESCUENTOS:

                    porcentaje = DESCUENTOS[codigo]

                    mensaje_descuento = (
                        "¡Código de descuento aplicado correctamente!"
                    )

                else:

                    mensaje_descuento = (
                        "El código ingresado no es válido. "
                        "Se calculó el pedido sin descuento."
                    )


            # ----------------------------------
            # CALCULAR DESCUENTO Y TOTAL
            # ----------------------------------

            descuento = subtotal * porcentaje // 100

            total = subtotal - descuento


            # ----------------------------------
            # MOSTRAR RESULTADO
            # ----------------------------------

            contenido = f"""
            <h1>¡Tu compra está calculada!</h1>

            <p>
                Este es el resumen de tu pedido en Urbania Girls.
            </p>

            <h2>Detalle de la compra</h2>

            <div class="detalle">
                <strong>Producto:</strong>
                <span>{html.escape(nombre)}</span>
            </div>

            <div class="detalle">
                <strong>Precio unitario:</strong>
                <span>{formato_pesos(precio)}</span>
            </div>

            <div class="detalle">
                <strong>Cantidad:</strong>
                <span>{cantidad}</span>
            </div>

            <div class="detalle">
                <strong>Subtotal:</strong>
                <span>{formato_pesos(subtotal)}</span>
            </div>

            <div class="detalle">
                <strong>Descuento:</strong>
                <span>{porcentaje}%</span>
            </div>

            <div class="detalle">
                <strong>Valor descontado:</strong>
                <span>{formato_pesos(descuento)}</span>
            </div>

            <div class="total">
                Total estimado de tu pedido:

                <strong>{formato_pesos(total)}</strong>
            </div>

            <p class="mensaje">
                {html.escape(mensaje_descuento)}
            </p>

            <p class="mensaje">
                Gracias por elegir Urbania Girls.
                ¡Esperamos que disfrutes tu nuevo look!
            </p>
            """

            self.enviar_html(contenido)


        # --------------------------------------
        # MANEJO DE ERRORES DE VALIDACION
        # --------------------------------------

        except ValueError as error:

            contenido = f"""
            <h1>No pudimos calcular tu compra</h1>

            <p class="mensaje">
                {html.escape(str(error))}
            </p>
            """

            self.enviar_html(contenido, 400)


        # --------------------------------------
        # MANEJO DE OTROS ERRORES
        # --------------------------------------

        except Exception:

            contenido = """
            <h1>Ocurrió un inconveniente</h1>

            <p class="mensaje">
                No fue posible procesar tu compra.
                Regresa al formulario e inténtalo nuevamente.
            </p>
            """

            self.enviar_html(contenido, 500)