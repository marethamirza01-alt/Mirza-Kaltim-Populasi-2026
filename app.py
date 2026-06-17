from flask import Flask, render_template
import folium
import pandas as pd

app = Flask(__name__)

# =====================
# HOME
# =====================
@app.route("/")
def home():
    return render_template("home.html")

# =====================
# CONTACT
# =====================
@app.route("/contact")
def contact():
    return render_template("contact.html")

# =====================
# MAP
# =====================
@app.route("/map")
def map_view():

    # load data
    df = pd.read_csv("C:\\Users\\ASUS\\Downloads\\PAK BAYU KALTIM\\static\\kaltim_dengan_koordinat.csv")
    df["populasi"] = pd.to_numeric(df["populasi"], errors="coerce")

    # pusat Kalimantan Timur
    map_kaltim = folium.Map(
        location=[-0.5, 116.9],
        zoom_start=7,
        tiles="OpenStreetMap"
    )

    max_pop = df["populasi"].max()

    # =====================
    # COLOR FUNCTION
    # =====================
    def get_color(pop):
        if pop >= max_pop * 0.75:
            return "red"       # sangat padat
        elif pop >= max_pop * 0.5:
            return "orange"    # padat
        elif pop >= max_pop * 0.25:
            return "blue"      # sedang
        else:
            return "green"     # rendah

    # =====================
    # MARKER POPULASI
    # =====================
    for _, row in df.iterrows():

        if pd.isna(row["latitude"]) or pd.isna(row["longitude"]):
            continue

        pop = row["populasi"]

        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=max(pop / 300000, 5),  # biar tidak terlalu kecil
            color=get_color(pop),
            fill=True,
            fill_color=get_color(pop),
            fill_opacity=0.75,
            popup=folium.Popup(
                f"""
                <b>{row['kabupaten']}</b><br>
                Populasi: {pop:,.0f}
                """,
                max_width=250
            )
        ).add_to(map_kaltim)

    # =====================
    # LEGEND (KIRI BAWAH)
    # =====================
    legend_html = """
    <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        z-index:9999;
        background-color:white;
        padding:12px;
        border-radius:10px;
        border:2px solid grey;
        font-size:14px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    ">
    <b>Legenda Kepadatan Penduduk</b><br><br>

    <span style="color:red;">●</span> Sangat Tinggi<br>
    <span style="color:orange;">●</span> Tinggi<br>
    <span style="color:blue;">●</span> Sedang<br>
    <span style="color:green;">●</span> Rendah<br>

    </div>
    """

    map_kaltim.get_root().html.add_child(folium.Element(legend_html))

    # =====================
    # SAVE MAP (WAJIB UNTUK VERCEL)
    # =====================
    map_kaltim.save("templates/map.html")

    return render_template("map.html")


if __name__ == "__main__":
    app.run(debug=True)