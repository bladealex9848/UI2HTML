import streamlit as st
import pathlib
from PIL import Image
from openai import OpenAI
import base64
import zipfile
import os

# Cargar API Key
API_KEY = st.secrets.get('OPENAI_API_KEY')

# Si la API Key no está en st.secrets, pídela al usuario
if not API_KEY:
    API_KEY = st.text_input('OpenAI API Key', type='password')

# Si no se ha proporcionado la API Key, no permitas que el usuario haga nada más
if not API_KEY:
    st.stop()

# Crear el cliente de OpenAI
client = OpenAI(api_key=API_KEY)

# Función para enviar un mensaje al modelo
def send_message_to_model(message, image_path):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode()

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": message},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=4096
    )
    content = response.choices[0].message.content
    # Eliminar etiquetas de markdown si están presentes
    # Caso 1: ```html al inicio y ``` al final (con posibles espacios o saltos de línea)
    if content.strip().startswith("```html") and content.strip().endswith("```"):
        content = content.strip()[7:].strip()
        if content.endswith("```"):
            content = content[:-3].strip()
    # Caso 2: ``` al inicio y ``` al final (con posibles espacios o saltos de línea)
    elif content.strip().startswith("```") and content.strip().endswith("```"):
        content = content.strip()[3:].strip()
        if content.endswith("```"):
            content = content[:-3].strip()
    # Caso 3: Si comienza con <!DOCTYPE html> pero tiene etiquetas markdown
    elif "<!DOCTYPE html>" in content and ("```" in content or "```html" in content):
        # Intentar extraer solo el HTML
        import re
        html_match = re.search(r'<!DOCTYPE html>[\s\S]*?</html>', content)
        if html_match:
            content = html_match.group(0)
    return content

# Función para limpiar el HTML de etiquetas markdown
def clean_html(html_content):
    # Eliminar etiquetas markdown al inicio
    if html_content.strip().startswith("```html"):
        html_content = html_content.strip()[7:].strip()
    elif html_content.strip().startswith("```"):
        html_content = html_content.strip()[3:].strip()

    # Eliminar etiquetas markdown al final
    if html_content.strip().endswith("```"):
        html_content = html_content.strip()[:-3].strip()

    # Si hay etiquetas markdown en medio, intentar extraer solo el HTML
    if "```" in html_content and "<!DOCTYPE html>" in html_content:
        import re
        html_match = re.search(r'<!DOCTYPE html>[\s\S]*?</html>', html_content)
        if html_match:
            html_content = html_match.group(0)

    return html_content

# Framework selection
framework = "Bootstrap"  # Cambia esto a "Bootstrap" u otro framework según sea necesario

# Streamlit app
def main():
    st.title("GPT-4.1 Nano Vision, UI a Código 👨‍💻")
    st.subheader('Hecho con ❤️ by [Alexander](https://twitter.com/alexanderofadul)')

    # Mostrar información sobre la generación de código
    with st.expander("ℹ️ Información sobre la generación de código"):
        st.markdown("""
        Esta aplicación utiliza plantillas HTML personalizadas como base para mejorar la generación de código.
        Esto ayuda a que el resultado sea más fiel a la imagen original y visualmente atractivo.

        Las plantillas incluyen:
        - Librerías modernas como Tailwind CSS y DaisyUI
        - Estilos CSS personalizados para diferentes tipos de interfaces
        - SVG personalizados para los iconos
        - Estructura HTML optimizada
        - Soporte para temas claro/oscuro

        El modelo de IA detecta el tipo de interfaz y selecciona la plantilla más adecuada como referencia.
        """)

        # Selector de plantilla para previsualizar
        template_options = {
            "Moderna (General)": "template-modern.html",
            "Chat": "template-chat.html",
            "Dashboard": "template-dashboard.html"
        }

        selected_template = st.selectbox("Selecciona una plantilla para previsualizar:", list(template_options.keys()))
        template_file_path = template_options[selected_template]

        # Mostrar la plantilla seleccionada si existe
        try:
            with open(template_file_path, "r", encoding="utf-8") as template_file:
                template_html = template_file.read()
                st.code(template_html[:1000] + "...", language="html")
                st.markdown(f"*La plantilla es demasiado larga para mostrarla completa. Se muestra solo el inicio.*")
        except:
            st.warning(f"No se encontró el archivo de plantilla HTML: {template_file_path}")

    uploaded_file = st.file_uploader("Selecciona una imagen de la interfaz de usuario para convertir en código HTML.", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            # Cargar y mostrar la imagen
            image = Image.open(uploaded_file)
            st.image(image, caption='Imagen subida.', use_container_width=True)

            # Convertir la imagen al modo RGB si tiene un canal alfa
            if image.mode == 'RGBA':
                image = image.convert('RGB')

            # Guardar la imagen subida temporalmente
            temp_image_path = pathlib.Path("temp_image.jpg")
            image.save(temp_image_path, format="JPEG")

            # Generar descripción de la interfaz de usuario
            if st.button("Convertir en código HTML"):
                st.write("🧑‍💻 Analizando tu interfaz de usuario...")
                prompt = """Describe esta interfaz de usuario en detalle. Para cada elemento, proporciona:
1. Su nombre y función
2. Su posición aproximada
3. Su color exacto (usa códigos hexadecimales cuando sea posible)
4. Su forma y estilo (bordes redondeados, sombras, etc.)
5. Cualquier icono o símbolo que contenga, con su color y forma

Presta especial atención a:
- El área de entrada de texto
- Los botones y su estilo (especialmente si son redondeados o tienen forma de píldora)
- Los iconos y sus colores
- El espaciado y alineación entre elementos

Cuando hagas referencia a un elemento de la interfaz de usuario, pon su nombre y su cuadro delimitador en el formato: [nombre del objeto (y_min, x_min, y_max, x_max)].

Usa el idioma español para describir los elementos de la interfaz de usuario."""
                description = send_message_to_model(prompt, temp_image_path)
                st.write(description)

                # Refinar la descripción
                st.write("🔍 Refinando descripción con comparación visual...")
                refine_prompt = f"""Compara los elementos de la interfaz de usuario descritos con la imagen proporcionada e identifica cualquier elemento faltante o inexactitud.

Presta especial atención a los siguientes detalles:
1. Los colores exactos de cada elemento (usa códigos hexadecimales cuando sea posible)
2. La forma de los botones (especialmente si son redondeados o tienen forma de píldora)
3. Los iconos específicos y sus colores
4. El estilo del área de entrada de texto
5. El espaciado y alineación de los elementos

Proporciona una descripción refinada y precisa de los elementos de la interfaz de usuario basada en esta comparación. Incluye todos los detalles visuales que serían importantes para recrear esta interfaz con precisión.

Aquí tienes la descripción inicial: {description}"""
                refined_description = send_message_to_model(refine_prompt, temp_image_path)
                st.write(refined_description)

                # Generar HTML
                st.write("🛠️ Generando sitio web...")

                # Detectar el tipo de interfaz para seleccionar la plantilla adecuada
                interface_detection_prompt = f"""Analiza la descripción de la interfaz de usuario y determina qué tipo de interfaz es.
                Clasifícala en una de estas categorías:
                1. Chat - Si es una interfaz de mensajería, chat o asistente virtual
                2. Dashboard - Si es un panel de administración, dashboard o interfaz con gráficos y estadísticas
                3. General - Para cualquier otro tipo de interfaz

                Responde SOLO con una de estas palabras: "Chat", "Dashboard" o "General".

                Descripción de la interfaz: {refined_description}"""

                interface_type = send_message_to_model(interface_detection_prompt, temp_image_path).strip()

                # Normalizar la respuesta
                if "chat" in interface_type.lower():
                    interface_type = "Chat"
                    template_path = "template-chat.html"
                elif "dashboard" in interface_type.lower():
                    interface_type = "Dashboard"
                    template_path = "template-dashboard.html"
                else:
                    interface_type = "General"
                    template_path = "template-modern.html"

                st.write(f"🔍 Tipo de interfaz detectada: **{interface_type}**")

                # Leer la plantilla HTML adecuada
                template_html = ""
                try:
                    with open(template_path, "r", encoding="utf-8") as template_file:
                        template_html = template_file.read()
                    st.success(f"Usando plantilla para interfaz de tipo {interface_type}")
                except:
                    st.warning(f"No se encontró la plantilla {template_path}. Intentando con plantilla alternativa...")
                    try:
                        # Intentar con la plantilla moderna como respaldo
                        with open("template-modern.html", "r", encoding="utf-8") as template_file:
                            template_html = template_file.read()
                        st.success("Usando plantilla moderna como alternativa")
                    except:
                        st.warning("No se encontraron plantillas. Se generará el HTML desde cero.")

                # Crear prompt específico según el tipo de interfaz
                if interface_type == "Chat":
                    html_prompt = f"""Crea un archivo HTML para una interfaz de chat basado en la siguiente descripción, utilizando los elementos descritos en la respuesta anterior.

                    Presta especial atención a:
                    1. La estructura de los mensajes (usuario vs asistente)
                    2. El área de entrada de mensajes y botón de envío
                    3. Los iconos y avatares
                    4. Los colores exactos de la interfaz original
                    5. Efectos visuales como indicadores de escritura

                    La interfaz debe ser receptiva y estar diseñada para dispositivos móviles. No incluyas explicaciones ni comentarios. SOLO devuelve el código HTML con CSS en línea.

                    Aquí tienes una plantilla HTML para interfaces de chat que puedes usar como base:

                    {template_html}

                    Aquí tienes la descripción refinada de la interfaz: {refined_description}"""

                elif interface_type == "Dashboard":
                    html_prompt = f"""Crea un archivo HTML para un dashboard/panel administrativo basado en la siguiente descripción, utilizando los elementos descritos en la respuesta anterior.

                    Presta especial atención a:
                    1. La estructura del menú lateral y navegación
                    2. Las tarjetas de estadísticas y sus iconos
                    3. Los gráficos y visualizaciones de datos
                    4. Las tablas de datos y su formato
                    5. Los colores exactos de la interfaz original

                    La interfaz debe ser receptiva y estar diseñada para dispositivos móviles. No incluyas explicaciones ni comentarios. SOLO devuelve el código HTML con CSS en línea.

                    Aquí tienes una plantilla HTML para dashboards que puedes usar como base:

                    {template_html}

                    Aquí tienes la descripción refinada de la interfaz: {refined_description}"""

                else:  # General
                    html_prompt = f"""Crea un archivo HTML basado en la siguiente descripción de la interfaz de usuario, utilizando los elementos descritos en la respuesta anterior.

                    Presta especial atención a:
                    1. La estructura general de la página
                    2. Los componentes interactivos (botones, formularios, etc.)
                    3. Los iconos y elementos visuales
                    4. Los colores exactos de la interfaz original
                    5. El espaciado y alineación entre elementos

                    La interfaz debe ser receptiva y estar diseñada para dispositivos móviles. No incluyas explicaciones ni comentarios. SOLO devuelve el código HTML con CSS en línea.

                    Aquí tienes una plantilla HTML moderna que puedes usar como base:

                    {template_html}

                    Aquí tienes la descripción refinada de la interfaz: {refined_description}"""
                initial_html = send_message_to_model(html_prompt, temp_image_path)
                clean_initial_html = clean_html(initial_html)
                st.code(clean_initial_html, language='html')

                # Refinar HTML
                st.write("🔧 Refinando sitio web...")
                # Crear prompt de refinamiento específico según el tipo de interfaz
                if interface_type == "Chat":
                    refine_html_prompt = f"""Valida y mejora el siguiente código HTML para una interfaz de chat basado en la descripción y la imagen original.

                    Asegúrate de corregir los siguientes aspectos:
                    1. La estructura y estilo de los mensajes debe ser clara y distinguible entre usuario y asistente
                    2. El área de entrada de mensajes debe tener el estilo correcto (fondo, bordes, etc.)
                    3. Los iconos deben ser SVG personalizados, no uses Bootstrap Icons ni caracteres Unicode
                    4. Los colores deben coincidir exactamente con los de la imagen original
                    5. El espaciado y alineación entre elementos debe ser similar al de la imagen original

                    SOLO devuelve el código HTML refinado con CSS en línea. Aquí tienes el HTML inicial:

                    {initial_html}"""

                elif interface_type == "Dashboard":
                    refine_html_prompt = f"""Valida y mejora el siguiente código HTML para un dashboard/panel administrativo basado en la descripción y la imagen original.

                    Asegúrate de corregir los siguientes aspectos:
                    1. La estructura del menú lateral y navegación debe ser clara y funcional
                    2. Las tarjetas de estadísticas deben tener el estilo y colores correctos
                    3. Los gráficos y visualizaciones de datos deben ser precisos
                    4. Las tablas deben tener el formato adecuado
                    5. Los iconos deben ser SVG personalizados, no uses Bootstrap Icons ni caracteres Unicode
                    6. Los colores deben coincidir exactamente con los de la imagen original

                    SOLO devuelve el código HTML refinado con CSS en línea. Aquí tienes el HTML inicial:

                    {initial_html}"""

                else:  # General
                    refine_html_prompt = f"""Valida y mejora el siguiente código HTML basado en la descripción de la interfaz de usuario y la imagen original.

                    Asegúrate de corregir los siguientes aspectos:
                    1. La estructura general de la página debe ser fiel a la imagen original
                    2. Los componentes interactivos deben tener el estilo correcto (bordes, colores, etc.)
                    3. Los iconos deben ser SVG personalizados, no uses Bootstrap Icons ni caracteres Unicode
                    4. Los colores deben coincidir exactamente con los de la imagen original
                    5. El espaciado y alineación entre elementos debe ser similar al de la imagen original

                    SOLO devuelve el código HTML refinado con CSS en línea. Aquí tienes el HTML inicial:

                    {initial_html}"""
                refined_html = send_message_to_model(refine_html_prompt, temp_image_path)
                clean_refined_html = clean_html(refined_html)
                st.code(clean_refined_html, language='html')

                # Guardar el HTML refinado en un archivo
                with open("index.html", "w", encoding="utf-8") as file:
                    file.write(clean_refined_html)

                # Crear archivo de texto con todo el texto generado
                with open("proceso.txt", "w", encoding="utf-8") as file:
                    file.write(f"Descripción inicial:\n{description}\n\n")
                    file.write(f"Descripción refinada:\n{refined_description}\n\n")
                    file.write(f"HTML inicial:\n{clean_initial_html}\n\n")
                    file.write(f"HTML refinado:\n{clean_refined_html}\n")

                # Crear archivo zip
                with zipfile.ZipFile("ui_to_code_output.zip", "w") as zipf:
                    zipf.write("index.html")
                    zipf.write("temp_image.jpg")
                    zipf.write("proceso.txt")

                # Proporcionar enlace de descarga para el archivo ZIP
                with open("ui_to_code_output.zip", "rb") as f:
                    st.download_button(
                        label="Descargar ZIP con HTML, imagen y proceso",
                        data=f,
                        file_name="ui_to_code_output.zip",
                        mime="application/zip"
                    )

                # Eliminar archivos temporales
                os.remove("index.html")
                os.remove("temp_image.jpg")
                os.remove("proceso.txt")
                os.remove("ui_to_code_output.zip")

                st.success("Se ha creado y descargado el archivo ZIP con todos los elementos.")

        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()