import streamlit as st
import pathlib
from PIL import Image
import google.generativeai as genai

# Configure the API key directly in the script
# Configura la clave de la API directamente en el script
# API_KEY = 'YOUR KEY'
# genai.configure(api_key=API_KEY)

# Cargar API Key / Load API Key
# Intenta cargar la API Key desde st.secrets / Try to load API Key from st.secrets
API_KEY = st.secrets.get('API_KEY')

# Si la API Key no está en st.secrets, pídela al usuario / If API Key is not in st.secrets, ask the user
if not API_KEY:
    API_KEY = st.text_input('Gemini API Key', type='password')

# Si no se ha proporcionado la API Key, no permitas que el usuario haga nada más / If API Key is not provided, do not allow the user to do anything else
if not API_KEY:
    st.stop()

# Configurar la clave de la API / Configure the API Key
genai.configure(api_key=API_KEY)

# Generation configuration
# Configuración de generación
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Safety settings
# Configuración de seguridad
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Model name
# Nombre del modelo
MODEL_NAME = "gemini-1.5-pro-latest"

# Framework selection (e.g., Tailwind, Bootstrap, etc.)
# Selección del framework (por ejemplo, Tailwind, Bootstrap, etc.)
# framework = "Regular CSS use flex grid etc"  # Change this to "Bootstrap" or any other framework as needed
framework = "Bootstrap" # Cambia esto a "Bootstrap" u otro framework según sea necesario

# Create the model
# Crear el modelo
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    safety_settings=safety_settings,
    generation_config=generation_config,
)

# Start a chat session
# Iniciar una sesión de chat
chat_session = model.start_chat(history=[])

# Function to send a message to the model
# Función para enviar un mensaje al modelo

def send_message_to_model(message, image_path):
    image_input = {
        'mime_type': 'image/jpeg',
        'data': pathlib.Path(image_path).read_bytes()
    }
    response = chat_session.send_message([message, image_input])
    return response.text

# Streamlit app
def main():
    st.title("Gemini 1.5 Pro, UI a Codigo 👨‍💻 ")
    st.subheader('Hecho con ❤️ by [Alexander](https://twitter.com/alexanderofadul)')

    uploaded_file = st.file_uploader("Selecciona una imagen de la interfaz de usuario para convertir en código HTML.", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            # Load and display the image
            # Cargar y mostrar la imagen
            image = Image.open(uploaded_file)
            # st.image(image, caption='Uploaded Image.', use_column_width=True)
            st.image(image, caption='Imagen subida.', use_column_width=True)

            # Convert image to RGB mode if it has an alpha channel
            # Convertir la imagen al modo RGB si tiene un canal alfa
            if image.mode == 'RGBA':
                image = image.convert('RGB')

            # Save the uploaded image temporarily
            # Guardar la imagen subida temporalmente
            temp_image_path = pathlib.Path("temp_image.jpg")
            image.save(temp_image_path, format="JPEG")

            # Generate UI description
            # Generar descripción de la interfaz de usuario
            if st.button("Convertir en código HTML"):
                # st.write("🧑‍💻 Looking at your UI...")
                st.write("🧑‍💻 Analizando tu interfaz de usuario...")
                # prompt = "Describe this UI in accurate details. When you reference a UI element put its name and bounding box in the format: [object name (y_min, x_min, y_max, x_max)]. Also Describe the color of the elements."
                prompt = "Describe esta interfaz de usuario en detalle. Cuando hagas referencia a un elemento de la interfaz de usuario, pon su nombre y su cuadro delimitador en el formato: [nombre del objeto (y_min, x_min, y_max, x_max)]. También describe el color de los elementos. Usa el idioma español para describir los elementos de la interfaz de usuario."
                description = send_message_to_model(prompt, temp_image_path)
                st.write(description)

                # Refine the description
                # Refinar la descripción
                # st.write("🔍 Refining description with visual comparison...")
                st.write("🔍 Refinando descripción con comparación visual...")
                # refine_prompt = f"Compare the described UI elements with the provided image and identify any missing elements or inaccuracies. Also Describe the color of the elements. Provide a refined and accurate description of the UI elements based on this comparison. Here is the initial description: {description}"
                refine_prompt = f"Compara los elementos de la interfaz de usuario descritos con la imagen proporcionada e identifica cualquier elemento faltante o inexactitud. También describe el color de los elementos. Proporciona una descripción refinada y precisa de los elementos de la interfaz de usuario basada en esta comparación. Aquí tienes la descripción inicial: {description}"
                refined_description = send_message_to_model(refine_prompt, temp_image_path)
                st.write(refined_description)

                # Generate HTML
                # Generar HTML
                # st.write("🛠️ Generating website...")
                st.write("🛠️ Generando sitio web...")
                # html_prompt = f"Create an HTML file based on the following UI description, using the UI elements described in the previous response. Include {framework} CSS within the HTML file to style the elements. Make sure the colors used are the same as the original UI. The UI needs to be responsive and mobile-first, matching the original UI as closely as possible. Do not include any explanations or comments. Avoid using ```html. and ``` at the end. ONLY return the HTML code with inline CSS. Here is the refined description: {refined_description}"
                html_prompt = f"Crea un archivo HTML basado en la siguiente descripción de la interfaz de usuario, utilizando los elementos de la interfaz de usuario descritos en la respuesta anterior. Incluye CSS de {framework} dentro del archivo HTML para dar estilo a los elementos. Asegúrate de que los colores utilizados sean los mismos que los de la interfaz de usuario original. La interfaz de usuario debe ser receptiva y estar diseñada para dispositivos móviles, coincidiendo lo más posible con la interfaz de usuario original. No incluyas explicaciones ni comentarios. Evita usar ```html. y ``` al final. SOLO devuelve el código HTML con CSS en línea. Aquí tienes la descripción refinada: {refined_description}"
                initial_html = send_message_to_model(html_prompt, temp_image_path)
                st.code(initial_html, language='html')

                # Refine HTML
                # Refinar HTML
                # st.write("🔧 Refining website...")
                st.write("🔧 Refinando sitio web...")
                # refine_html_prompt = f"Validate the following HTML code based on the UI description and image and provide a refined version of the HTML code with {framework} CSS that improves accuracy, responsiveness, and adherence to the original design. ONLY return the refined HTML code with inline CSS. Avoid using ```html. and ``` at the end. Here is the initial HTML: {initial_html}"
                refine_html_prompt = f"Valida el siguiente código HTML basado en la descripción de la interfaz de usuario y la imagen y proporciona una versión refinada del código HTML con CSS de {framework} que mejore la precisión, la capacidad de respuesta y la fidelidad al diseño original. SOLO devuelve el código HTML refinado con CSS en línea. Evita usar ```html. y ``` al final. Aquí tienes el HTML inicial: {initial_html}"
                refined_html = send_message_to_model(refine_html_prompt, temp_image_path)
                st.code(refined_html, language='html')

                # Save the refined HTML to a file
                # Guardar el HTML refinado en un archivo
                with open("index.html", "w") as file:
                    file.write(refined_html)
                # st.success("HTML file 'index.html' has been created.")
                st.success("Se ha creado el archivo HTML 'index.html'.")

                # Provide download link for HTML
                # Proporcionar enlace de descarga para HTML
                st.download_button(label="Descargar HTML", data=refined_html, file_name="index.html", mime="text/html")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
