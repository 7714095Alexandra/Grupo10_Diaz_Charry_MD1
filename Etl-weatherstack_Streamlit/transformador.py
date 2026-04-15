import pandas as pd

# leer archivo generado
df = pd.read_csv("data_clima.csv")

# limpieza básica
df = df.dropna()

# ejemplo de transformación
df["temperatura"] = df["temperatura"].round(1)

# guardar nuevo archivo
df.to_csv("data_clima_limpio.csv", index=False)

print("✅ Datos transformados correctamente en data_clima_limpio.csv")