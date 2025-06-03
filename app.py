from flask import Flask, request, render_template_string
import json

app = Flask(__name__)

with open("oglasi.json", "r", encoding="utf-8") as f:
    svi_oglasi = json.load(f)

zupanije = sorted(set(o["zupanija"] for o in svi_oglasi if o.get("zupanija")))

@app.route("/", methods=["GET"])
def home():
    z = request.args.get("zupanija", "")
    filtrirano = [o for o in svi_oglasi if z in ("", o.get("zupanija", ""))]
    return render_template_string(open("index.html", encoding="utf-8").read(), oglasi=filtrirano, zupanije=zupanije, odabrana=z)

if __name__ == "__main__":
    app.run()
