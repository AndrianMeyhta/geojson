import json
import psycopg2

# Koneksi ke database
conn = psycopg2.connect(
    host="localhost",
    database="databasedesa",
    user="postgres",
    password="090503"
)

# Membaca data dari tabel desloc2
cur = conn.cursor()
cur.execute("SELECT * FROM desloc2")
rows = cur.fetchall()

# Membuat struktur data GeoJSON
geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Iterasi melalui setiap baris data
for row in rows:
    # Mengambil kolom yang sesuai
    object_id = row[0]
    namobj = row[1]
    kdcpum = row[2]
    wadmkc = row[3]
    wadmkd = row[4]
    wadmkk = row[5]
    wadmpr = row[6]
    luas = row[7]
    shape_length = row[8]
    shape_area = row[9]
    json_data = row[10]
    value = json.loads(json_data)

    # Membuat fitur GeoJSON
    feature = {
        "type": "Feature",
        "properties": {
            "OBJECTID": object_id,
            "NAMOBJ": namobj,
            "KDCPUM": kdcpum,
            "WADMKC": wadmkc,
            "WADMKD": wadmkd,
            "WADMKK": wadmkk,
            "WADMPR": wadmpr,
            "luas": luas,
            "SHAPE_Length": shape_length,
            "SHAPE_Area": shape_area
        },
        "geometry": value['geometry']
    }

    # Menambahkan fitur ke koleksi GeoJSON
    geojson["features"].append(feature)

# Menutup koneksi ke database
conn.close()

# Menyimpan struktur data GeoJSON ke file
with open('output.geojson', 'w') as file:
    json.dump(geojson, file, indent= 2)