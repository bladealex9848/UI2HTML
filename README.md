![Logo de UI2HTML](https://github.com/bladealex9848/UI2HTM/blob/main/logo.jpg)

# UI2HTML: Convierte Interfaces en Código 🖼️➡️💻

[![Version](https://img.shields.io/badge/versión-1.0.0-darkgreen.svg)](https://github.com/bladealex9848/UI2HTML)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30.0-ff4b4b.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI_API-v2-00C244.svg)](https://platform.openai.com/)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-yellow.svg)](LICENSE)
[![Visitantes](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2Fbladealex9848%2FUI2HTML&label=Visitantes&labelColor=%235d5d5d&countColor=%231e7ebf&style=flat)](https://github.com/bladealex9848/UI2HTML)

## 📝 Descripción

UI2HTML es una herramienta innovadora que convierte imágenes de interfaces de usuario en código HTML. Utilizando la API de OpenAI, esta aplicación analiza y describe detalladamente la interfaz de usuario y genera el código HTML correspondiente, asegurando que el diseño sea receptivo y fiel al original.

## 🚀 Introducción

Con UI2HTML, puedes transformar imágenes de interfaces de usuario en código HTML de manera sencilla y eficiente. La aplicación utiliza la API de OpenAI para analizar y describir la interfaz de usuario, generando un código HTML preciso y estilizado con librerías modernas como Tailwind CSS, DaisyUI y otras. Para desarrollar esta aplicación necesitaremos:

- API de OpenAI
- Streamlit

## 🔍 ¿Cómo funciona?

1. **Carga una imagen** de la interfaz de usuario.
2. La imagen se **analiza y se describe detalladamente** utilizando modelos avanzados de visión.
3. Se genera un **código HTML** basado en la descripción de la interfaz de usuario.
4. El código HTML se **refina para mejorar la precisión** y la capacidad de respuesta.
5. Se utiliza una **plantilla base con librerías modernas** para garantizar un resultado visualmente atractivo.

## ✨ Funcionalidades

- **🖼️ Convertir imagen a HTML**: Transforma imágenes de interfaces de usuario en código HTML funcional.
- **🔄 Refinamiento de HTML**: Mejora la precisión y la capacidad de respuesta del código HTML generado.
- **💾 Descarga de HTML**: Permite descargar el código HTML generado para su uso inmediato.
- **🎨 Plantillas modernas**: Utiliza librerías como Tailwind CSS, DaisyUI y otras para resultados visualmente atractivos.
- **📱 Diseño responsive**: Genera código que se adapta a diferentes tamaños de pantalla.

## 🛠️ Instalación

1. Asegúrate de tener **Python 3.8 o superior** instalado en tu máquina.
2. Clona este repositorio usando:
   ```bash
   git clone https://github.com/bladealex9848/UI2HTML.git
   ```
3. Navega al directorio del proyecto:
   ```bash
   cd UI2HTML
   ```
4. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
5. Configura tu clave API de OpenAI en un archivo `.env` o como variable de entorno:
   ```
   OPENAI_API_KEY=tu_clave_api_aqui
   ```
6. Ejecuta la aplicación:
   ```bash
   streamlit run app.py
   ```

## 📋 Uso

### Convertir imagen a HTML

1. **Carga una imagen** de la interfaz de usuario que deseas convertir.
2. Selecciona el **framework CSS** que prefieras utilizar (Bootstrap, Tailwind, etc.).
3. Haz clic en **"Convertir en código HTML"**.
4. Espera a que se genere y refine el código HTML.
5. **Previsualiza** el resultado en tiempo real.
6. **Descarga** el archivo HTML generado para usarlo en tu proyecto.

### Personalización

- Puedes **ajustar los parámetros** de generación para obtener resultados más precisos.
- Selecciona entre diferentes **plantillas base** según el tipo de interfaz que estés convirtiendo.
- **Edita el código generado** directamente en la aplicación si necesitas hacer ajustes.

## 👥 Contribuciones

Si deseas contribuir a este proyecto, por favor:

1. Realiza un **fork** de este repositorio
2. Crea una **nueva rama** para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios y **commitea** (`git commit -am 'Añade nueva funcionalidad'`)
4. **Sube** los cambios a tu fork (`git push origin feature/nueva-funcionalidad`)
5. Crea un nuevo **Pull Request**

## 📂 Estructura del Proyecto

```
UI2HTML/
├── app.py                     # Archivo principal de la aplicación
├── requirements.txt           # Dependencias del proyecto
├── template-modern.html       # Plantilla base con Tailwind y DaisyUI
├── template-chat.html         # Plantilla para interfaces de chat
├── template-dashboard.html    # Plantilla para interfaces de dashboard
├── README.md                  # Documentación principal
├── LICENSE                    # Licencia del proyecto
├── CHANGELOG.md               # Registro de cambios
├── .gitignore                 # Archivos ignorados por git
└── Demos/                     # Ejemplos de interfaces convertidas
    ├── README.md              # Documentación de los ejemplos
    └── ChatGPT-Clone/         # Ejemplo de clon de ChatGPT
        ├── original.txt       # Descripción de la imagen original
        ├── generado.html      # Código HTML generado
        └── README.md          # Documentación del ejemplo
```

## 📚 Proyectos Relacionados

Si te gusta este proyecto, también puedes estar interesado en:

### Expert Nexus 🧠🔄

[Expert Nexus](https://github.com/bladealex9848/expert_nexus) es un sistema avanzado de asistentes virtuales especializados que permite cambiar entre diferentes expertos durante una misma conversación, manteniendo siempre el contexto completo.

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para obtener más detalles.

## 👤 Autor

Creado con ❤️ por [Alexander Oviedo Fadul](https://github.com/bladealex9848)

[GitHub](https://github.com/bladealex9848) | [Website](https://alexanderoviedofadul.dev) | [LinkedIn](https://www.linkedin.com/in/alexander-oviedo-fadul/) | [Instagram](https://www.instagram.com/alexander.oviedo.fadul) | [Twitter](https://twitter.com/alexanderofadul) | [Facebook](https://www.facebook.com/alexanderof/) | [WhatsApp](https://api.whatsapp.com/send?phone=573015930519&text=Hola%20!Quiero%20conversar%20contigo!%20)
