import pandas as pd
import random

ciudades = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena"]

data = []

for ciudad in ciudades:
    for _ in range(200):  # 200 por ciudad = 1000 total
        data.append({
            "ciudad": ciudad,
            "temperatura": round(random.uniform(15, 35), 2),
            "humedad": random.randint(50, 100),
            "velocidad_viento": round(random.uniform(1, 10), 2),
            "descripcion": random.choice(["Soleado", "Nublado", "Lluvioso"])
        })

df = pd.DataFrame(data)

# guardar archivo
df.to_csv("data_clima.csv", index=False)

print("✅ 1000 registros generados correctamente en data_clima.csv")