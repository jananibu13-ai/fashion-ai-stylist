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

BODY_SHAPE_MAP = {

    "Hourglass": [
        "Dresses",
        "Tops",
        "Tunics",
        "Jeans",
        "Jackets",
        "Kurtis"
    ],

    "Pear": [
        "Tops",
        "Tunics",
        "Jackets",
        "Sweatshirts",
        "Kurtis",
        "Kurtas"
    ],

    "Apple": [
        "Kurtas",
        "Tunics",
        "Tshirts",
        "Shirts",
        "Dresses"
    ],

    "Rectangle": [
        "Dresses",
        "Tops",
        "Tunics",
        "Jackets",
        "Kurtis"
    ],

    "Inverted Triangle": [
        "Skirts",
        "Jeans",
        "Trousers",
        "Leggings",
        "Jeggings"
    ]
}


def recommend_products(
        skin_tone,
        gender,
        occasion,
        body_shape):

    colors = COLOR_MAP.get(
        skin_tone,
        ["Black"]
    )

    preferred_articles = BODY_SHAPE_MAP.get(
        body_shape,
        []
    )

    recommendations = df[
        (df["gender"] == gender)
        &
        (df["baseColour"].isin(colors))
        &
        (df["usage"] == occasion)
    ]

    if preferred_articles:

        body_filtered = recommendations[
            recommendations["articleType"].isin(
                preferred_articles
            )
        ]

        if len(body_filtered) > 0:
            recommendations = body_filtered

    return recommendations[
        [
            "productDisplayName",
            "baseColour",
            "articleType",
            "usage"
        ]
    ].head(20)