import pandas as pd

# leer archivo generado
df = pd.read_csv("data_anime.csv")

# ============================
# LIMPIEZA
# ============================

# eliminar nulos
df = df.dropna()

# ============================
# TRANSFORMACIONES
# ============================

# redondear score
df["score"] = df["score"].round(1)

# asegurar tipo entero
df["episodios"] = df["episodios"].astype(int)
df["anio"] = df["anio"].astype(int)

# normalizar texto
df["titulo"] = df["titulo"].str.title()
df["estado"] = df["estado"].str.strip()

# ============================
# GUARDAR ARCHIVO LIMPIO
# ============================

df.to_csv("data_anime_limpio.csv", index=False)

print("✅ Datos de anime transformados correctamente en data_anime_limpio.csv")