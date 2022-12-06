cardinalList = ["N","NNE","NE","ENE","E","ESE","SE","SSE",
        "S","SSW","SW","WSW","W","WNW","NW","NNW"]
degrees = int(float(degrees))
index = int((degrees + 11.25) / 22.5)
direction = cardinalList[index % 16]