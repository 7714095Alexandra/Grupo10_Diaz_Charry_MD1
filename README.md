[README_Proyecto.md](https://github.com/user-attachments/files/26125438/README_Proyecto.md)
# 🚀 Grupo 10_Diaz_Charry_MD1  

---

## 📌 Descripción del Proyecto  
Este proyecto consiste en el desarrollo de un sistema de análisis de datos basado en un **catálogo de anime y manga**, utilizando la API de Jikan para acceder a una de las bases de datos más grandes de este contenido.  

Se implementa un flujo completo de **ETL (Extract, Transform, Load)**, almacenamiento en base de datos, visualización interactiva y modelos de machine learning para generar valor a partir de los datos.

---

## 🎯 Objetivo del Proyecto  
Desarrollar una solución integral que permita:  
- Extraer datos de anime y manga desde una API externa.  
- Almacenar y estructurar la información en una base de datos.  
- Analizar y visualizar tendencias del contenido.  
- Aplicar modelos de machine learning para predicción y recomendación.  

---

## 📂 Descripción de los Datos  
Los datos son obtenidos desde la API de Jikan e incluyen información como:  
- Título del anime/manga  
- Géneros  
- Puntuación (score)  
- Popularidad  
- Número de episodios  
- Temporadas de emisión  
- Sinopsis  

Estos datos son procesados y transformados antes de almacenarse en PostgreSQL.

---

## 🌎 Alcance  
El proyecto cubre:  
- Extracción automatizada de datos desde la API  
- Procesamiento y limpieza de datos  
- Almacenamiento estructurado en base de datos  
- Visualización interactiva mediante dashboard  
- Implementación de modelos predictivos  
- Despliegue mediante contenedores Docker  

---

## 🛠️ Herramientas  
- 💻 VS Code  
- 🐍 Python  
- 🐧 WSL  
- 🐳 Docker  
- 🌐 Streamlit   
- 🗄️ PostgreSQL  

---

## 💡 Solución  
Se implementa una arquitectura de datos basada en:  

1. **Extractor ETL**  
   - Script en Python que consume la API Jikan  
   - Manejo de errores y validación de datos  

2. **Base de Datos PostgreSQL**  
   - Diseño optimizado de tablas  
   - Almacenamiento estructurado  

3. **Dashboard en Streamlit**  
   - Visualización interactiva  
   - Análisis exploratorio de datos  

4. **Machine Learning (Jupyter)**  
   - Predicción de puntuaciones  
   - Sistema de recomendación  

5. **Docker Compose**  
   - Orquestación de servicios  
   - Entorno reproducible  

---

## 🏗️ Estructura  
El proyecto se organiza de la siguiente manera:

```
Etl-jikan/
├── alembic/                 
│   ├── versions/
│   │   └── xxx_initial_migration.py
│   ├── env.py
│   ├── script.py.mako
│   └── alembic.ini
├── .streamlit/
│   ├── secrets.toml               
│   └── config.toml   
├── scripts/
│   ├── database.py
│   ├── models.py
│   ├── extractor.py
│   ├── extractor_db.py
│   ├── consultas.py
│   ├── test_db.py
│   └── visualizador.py
├── data/
│   ├── clima.csv
│   └── clima_raw.json
├── logs/
│   └── etl.log
├── .env                    
├── dashboard_app.py                
├── dashboard_advanced.py           
├── dashboard_interactive.py               
├── requirements.txt               
├── .gitignore                     
└── README.md
```

---

## 📥 Clonar  

git clone https://github.com/7714095Alexandra/Grupo10_Diaz_Charry_MD1.git

---

## 👩‍💻👩‍💻 Autores - 📧 Email 

---amcharry-2023a@corhuila.edu.co ---madiaz-2023a@corhuila.edu.co
