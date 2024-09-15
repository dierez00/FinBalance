import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv('your_data.csv')

# Preparar datos
df['date'] = pd.to_datetime(df['date'])  # convertir a formato datetime si necesario

# Graficar
plt.plot(df['date'], df['value'])
plt.title('Evolución del valor sobre el tiempo')
plt.xlabel('Fecha')
plt.ylabel('Valor')
plt.show()