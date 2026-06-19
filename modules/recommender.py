import pandas as pd

df = pd.read_csv("data/styles.csv")

COLOR_MAP = {

    "Fair": [
        "Black",
        "Navy Blue",
        "Maroon",
        "Burgundy",
        "Teal",
        "Purple",
        "Emerald",
        "Olive"
    ],

    "Medium": [
        "Brown",
        "Coffee Brown",
        "Olive",
        "Mustard",
        "Teal",
        "Sea Green",
        "Blue",
        "Maroon"
    ],

    "Dark": [
        "White",
        "Yellow",
        "Mustard",
        "Red",
        "Turquoise Blue",
        "Royal Blue",
        "Teal",
        "Orange"
    ]
}

def recommend_products(
        skin_tone,
        gender,
        occasion):

    colors = COLOR_MAP.get(
        skin_tone,
        ["Black"]
    )

    recommendations = df[
        (df["gender"] == gender)
        &
        (df["baseColour"].isin(colors))
        &
        (df["usage"] == occasion)
    ]

    return recommendations[
        [
            "productDisplayName",
            "baseColour",
            "articleType",
            "usage"
        ]
    ].head(20)