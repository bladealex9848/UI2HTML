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
    return response.choices[0].message.content

# Framework selection
framework = "Bootstrap"  # Cambia esto a "Bootstrap" u otro framework según sea necesario

# Streamlit app
def main():
    st.title("GPT-4.1 Nano Vision, UI a Código 👨‍💻")
    st.subheader('Hecho con ❤️ by [Alexander](https://twitter.com/alexanderofadul)')

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
                prompt = "Describe esta interfaz de usuario en detalle. Cuando hagas referencia a un elemento de la interfaz de usuario, pon su nombre y su cuadro delimitador en el formato: [nombre del objeto (y_min, x_min, y_max, x_max)]. También describe el color de los elementos. Usa el idioma español para describir los elementos de la interfaz de usuario."
                description = send_message_to_model(prompt, temp_image_path)
                st.write(description)

                # Refinar la descripción
                st.write("🔍 Refinando descripción con comparación visual...")
                refine_prompt = f"Compara los elementos de la interfaz de usuario descritos con la imagen proporcionada e identifica cualquier elemento faltante o inexactitud. También describe el color de los elementos. Proporciona una descripción refinada y precisa de los elementos de la interfaz de usuario basada en esta comparación. Aquí tienes la descripción inicial: {description}"
                refined_description = send_message_to_model(refine_prompt, temp_image_path)
                st.write(refined_description)

                # Generar HTML
                st.write("🛠️ Generando sitio web...")
                html_prompt = f"Crea un archivo HTML basado en la siguiente descripción de la interfaz de usuario, utilizando los elementos de la interfaz de usuario descritos en la respuesta anterior. Incluye CSS de {framework} dentro del archivo HTML para dar estilo a los elementos. Asegúrate de que los colores utilizados sean los mismos que los de la interfaz de usuario original. La interfaz de usuario debe ser receptiva y estar diseñada para dispositivos móviles, coincidiendo lo más posible con la interfaz de usuario original. No incluyas explicaciones ni comentarios. SOLO devuelve el código HTML con CSS en línea. Aquí tienes la descripción refinada: {refined_description}"
                initial_html = send_message_to_model(html_prompt, temp_image_path)
                st.code(initial_html, language='html')

                # Refinar HTML
                st.write("🔧 Refinando sitio web...")
                refine_html_prompt = f"Valida el siguiente código HTML basado en la descripción de la interfaz de usuario y la imagen y proporciona una versión refinada del código HTML con CSS de {framework} que mejore la precisión, la capacidad de respuesta y la fidelidad al diseño original. SOLO devuelve el código HTML refinado con CSS en línea. Aquí tienes el HTML inicial: {initial_html}"
                refined_html = send_message_to_model(refine_html_prompt, temp_image_path)
                st.code(refined_html, language='html')

                # Guardar el HTML refinado en un archivo
                with open("index.html", "w", encoding="utf-8") as file:
                    file.write(refined_html)

                # Crear archivo de texto con todo el texto generado
                with open("proceso.txt", "w", encoding="utf-8") as file:
                    file.write(f"Descripción inicial:\n{description}\n\n")
                    file.write(f"Descripción refinada:\n{refined_description}\n\n")
                    file.write(f"HTML inicial:\n{initial_html}\n\n")
                    file.write(f"HTML refinado:\n{refined_html}\n")

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