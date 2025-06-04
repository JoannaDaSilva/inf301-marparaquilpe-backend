# Backend - INF301 Mar para Quilpué 🌊

Este es el backend del proyecto desarrollado para el curso INF301. Está construido con FastAPI y se conecta a una base de datos Supabase.

**Integrantes**:
- Raúl Cuello
- Joanna Da Silva
- Felipe San Martin

## Instrucciones de Ejecución

### 1. Clona el repositorio

```bash
git clone https://github.com/JoannaDaSilva/inf301-marparaquilpe-backend.git
cd inf301-marparaquilpe-backend
```

### 2. Crea y activa un entorno virtual (opcional pero recomendado)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Obtén el archivo .env

Solicita el archivo .env previamente, para la conexión a supabase.

### 5. Ejecuta el servidor

```bash
uvicorn app.main:app --reload
```

La API estará disponible en: http://127.0.0.1:8000/docs