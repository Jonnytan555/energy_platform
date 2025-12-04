import pandas as pd

async def get_shipping_status():

    ships = pd.DataFrame([
        {"name": "LNG Sakura", "speed": 0.5, "cargo": 170_000},
        {"name": "LNG River", "speed": 14.3, "cargo": 160_000},
        {"name": "LNG Poseidon", "speed": 0.8, "cargo": 155_000}
    ])

    floating = ships[ships["speed"] < 1]

    return {
        "ships": ships.to_dict(orient="records"),
        "floating_storage": floating.to_dict(orient="records")
    }
