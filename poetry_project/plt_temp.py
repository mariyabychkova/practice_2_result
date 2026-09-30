import requests
import matplotlib.pyplot as plt
import pandas as pd


URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=55.75&longitude=37.62"
    "&hourly=temperature_2m"
    "&forecast_days=1"
)


def make_dataframe(data):
    """Преобразует ответ API в DataFrame."""
    return pd.DataFrame({
        "time": pd.to_datetime(data["hourly"]["time"]),
        "temperature_c": data["hourly"]["temperature_2m"],
    })


def main():
    response = requests.get(URL, timeout=10)

    # Проверяем успешность HTTP-запроса
    response.raise_for_status()

    # JSON разбираем только после проверки ответа
    data = response.json()

    df = make_dataframe(data).head(24)

    # Сохраняем CSV
    df.to_csv("temperature_24h.csv", index=False)

    # Строим график
    plt.figure(figsize=(10, 5))
    plt.plot(df["time"], df["temperature_c"])
    plt.xlabel("Время")
    plt.ylabel("Температура, °C")
    plt.title("Температура за ближайшие 24 часа")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Сохраняем PNG
    plt.savefig("temperature_24h.png", dpi=150)
    plt.show()

    print("Сохранено:")
    print("- temperature_24h.csv")
    print("- temperature_24h.png")


if __name__ == "__main__":
    main()