import json
import psycopg2

# Koneksi ke database
conn = psycopg2.connect(
    host="localhost",
    database="databasedesa",
    user="postgres",
    password="090503"
)

# Baca file GeoJSON
with open('file/Des_Kel_YD.geojson') as file:
    data = json.load(file)

# Iterasi melalui semua fitur
for feature in data['features']:
    # Ambil properti dan geometri
    properties = feature['properties']
    coordinates = feature['geometry']['coordinates']

    template = {
        'type' : 'Feature',
        'geometry' : {
            'type': 'MultiPolygon',
            'coordinates': coordinates
        }
    }

    # Simpan data ke tabel des_kel
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO desloc2 (OBJECTID, NAMOBJ, KDCPUM, WADMKC, WADMKD, WADMKK, WADMPR, luas, shape_length, shape_area, coordinates)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (properties['OBJECTID'], properties['NAMOBJ'], properties['KDCPUM'], properties['WADMKC'], properties['WADMKD'], properties['WADMKK'], properties['WADMPR'], properties['luas'],properties['SHAPE_Length'],properties['SHAPE_Area'], json.dumps(template)))
    conn.commit()

    cur.close()

# Tutup koneksi ke database
conn.close()