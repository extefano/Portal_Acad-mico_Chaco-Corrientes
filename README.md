# 🎓 Portal Académico Chaco-Corrientes

Sitio web estático del **Portal Académico Chaco-Corrientes**, que reúne la oferta académica universitaria pública y gratuita de la región (UNNE, UTN FRRe y UNCAUS).

El proyecto replica con fidelidad el diseño, estructura de bloques Gutenberg, interactividad y estilos del tema oficial **WordPress Assembler**.

---

## 🚀 Estructura del Proyecto

```text
├── dist/                          # 🌐 SITIO WEB EN PRODUCCIÓN (Publicable)
│   ├── index.html                 # Página principal / Portada
│   ├── *.html                     # Páginas de facultades y carreras (15 páginas)
│   └── assets/
│       ├── css/
│       │   └── wordpress-assembler.css # CSS Maestro responsivo
│       ├── js/
│       │   └── site.js            # Lógica interactiva (menú, pestañas, mapas, carrusel)
│       ├── images/                # 37 imágenes locales (logos, portadas, sedes)
│       └── vendor/leaflet/        # Librería Leaflet local (mapas interactivos)
│
├── build_site.py                  # Script constructor desde el XML de WordPress
├── wp_extracted_styles.json       # Tokens de diseño y estilos base extraídos
├── vercel.json                    # Configuración para despliegue en Vercel
├── render.yaml                    # Configuración para despliegue en Render
└── README.md
```

---

## 💻 Vista previa local

Para previsualizar el sitio en tu computadora:

1. Abrir directamente `dist/index.html` en cualquier navegador web.
2. O iniciar un servidor local con Python:
   ```bash
   python -m http.server 8080 --directory dist
   ```
   Luego ingresar en [http://localhost:8080](http://localhost:8080).

---

## ☁️ Despliegue en la Nube

### Vercel
El repositorio incluye `vercel.json` configurado para publicar la carpeta `dist/`. Solo debes conectar tu repositorio en [vercel.com](https://vercel.com).

### Render
El repositorio incluye `render.yaml`. En [render.com](https://render.com), crea un **Static Site** con directorio de publicación: `dist`.
