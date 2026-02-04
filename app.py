from flask import Flask, render_template, request, redirect, url_for, session, flash
import math

app = Flask(__name__)
app.secret_key = 'asta_pro_secret_2026'

# Complete City Database
CITY_INTEL = {
    "hyderabad": {
        "lat": 17.3850, "lon": 78.4867,
        "bg": "https://images.unsplash.com/photo-1590050752117-23a9d7fc2140?auto=format&fit=crop&w=1600&q=80",
        "spots": ["Charminar", "Golconda Fort", "Ramoji Film City", "Hussain Sagar", "Birla Mandir", "Salar Jung Museum"],
        "weather": "Sunny & Warm (25–35 °C)", "food": "Hyderabadi Biryani, Haleem, Irani Chai, Kebabs",
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3806.984!2d78.474!3d17.385!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bcb99c700000001%3A0x1b0a!2sHyderabad%2C%20Telangana!5e0!3m2!1sen!2sin!4v1730000000000!5m2!1sen!2sin"
    },
    "delhi": {
        "lat": 28.6139, "lon": 77.2090,
        "bg": "https://images.unsplash.com/photo-1587474260584-136574528ed5?auto=format&fit=crop&w=1600&q=80",
        "spots": ["India Gate", "Red Fort", "Lotus Temple", "Qutub Minar", "Humayun's Tomb", "Akshardham"],
        "weather": "Variable (5–45 °C)", "food": "Butter Chicken, Chole Bhature, Parathas, Chaat",
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3502.343!2d77.229509!3d28.613895!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x390ce2db00000001%3A0x!2sDelhi!5e0!3m2!1sen!2sin!4v1730000000000!5m2!1sen!2sin"
    },
    "goa": {
        "lat": 15.2993, "lon": 74.1240,
        "bg": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1600&q=80",
        "spots": ["Baga Beach", "Dudhsagar Falls", "Palolem Beach", "Fort Aguada", "Anjuna Flea Market", "Basilica of Bom Jesus"],
        "weather": "Tropical (25–32 °C)", "food": "Fish Curry Rice, Vindaloo, Bebinca, Prawn Balchão",
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d492485.451!2d73.702747!3d15.347898!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bbfba10633c4e41%3A0x1d5d28ca891038c8!2sGoa!5e0!3m2!1sen!2sin!4v1730000000000!5m2!1sen!2sin"
    },
    "kerala": {
        "lat": 9.9312, "lon": 76.2673,
        "bg": "https://images.unsplash.com/photo-1564507592333-c3f5b6f2b2b0?auto=format&fit=crop&w=1600&q=80",
        "spots": ["Alleppey Backwaters", "Munnar Tea Gardens", "Periyar Sanctuary", "Kovalam Beach", "Thekkady"],
        "weather": "Tropical Monsoon (24–32 °C)", "food": "Appam with Stew, Sadhya, Karimeen Pollichathu",
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3929.984!2d76.2673!3d9.9312!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3b080d!2sKerala!5e0!3m2!1sen!2sin!4v1730000000000!5m2!1sen!2sin"
    },
    "bangalore": {
        "lat": 12.9716, "lon": 77.5946,
        "bg": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=1600&q=80",
        "spots": ["Lalbagh", "Bangalore Palace", "Cubbon Park", "ISKCON Temple", "Wonderla", "Bannerghatta Park"],
        "weather": "Pleasant (20–30 °C)", "food": "Benne Dosa, Filter Coffee, Masala Dosa, Bisi Bele Bath",
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3886.984!2d77.5946!3d12.9716!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae1670c9b44e51%3A0x63802444d7155d43!2sBengaluru%2C%20Karnataka!5e0!3m2!1sen!2sin!4v1730000000000!5m2!1sen!2sin"
    },
    "mumbai": {
        "lat": 19.0760, "lon": 72.8777,
        "bg": "https://images.unsplash.com/photo-1567157577867-05ccb1388e66?auto=format&fit=crop&w=1600&q=80",
        "spots": ["Gateway of India", "Marine Drive", "Elephanta Caves", "Juhu Beach", "Siddhivinayak Temple"],
        "weather": "Humid Coastal (25–35 °C)", "food": "Vada Pav, Pav Bhaji, Misal Pav, Seafood",
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3770.843!2d72.877655!3d19.0760!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7c6306644edc1%3A0x5da4ed8f8d648c69!2sMumbai%2C%20Maharashtra!5e0!3m2!1sen!2sin!4v1730000000000!5m2!1sen!2sin"
    },
    "chennai": {
        "lat": 13.0827, "lon": 80.2707,
        "bg": "https://images.unsplash.com/photo-1582514904323-3e0a6e5e4b0e?auto=format&fit=crop&w=1600&q=80",
        "spots": ["Marina Beach", "Kapaleeshwarar Temple", "Fort St. George", "Santhome Basilica", "Government Museum"],
        "weather": "Hot & Humid (28–38 °C)", "food": "Idli Sambar, Chettinad Chicken, Pongal, Filter Coffee",
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3886.984!2d80.2707!3d13.0827!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a52663500000001%3A0x!2sChennai!5e0!3m2!1sen!2sin!4v1730000000000!5m2!1sen!2sin"
    },
    "ooty": {
        "lat": 11.4102, "lon": 76.6950,
        "bg": "https://images.unsplash.com/photo-1580130718646-9f694209b207?auto=format&fit=crop&w=1600&q=80",
        "spots": ["Ooty Lake", "Botanical Gardens", "Tea Plantations", "Doddabetta Peak", "Pykara Falls"],
        "weather": "Cool & Misty (10–25 °C)", "food": "Varkey, Homemade Chocolates, Masala Chai",
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3919.000!2d76.6950!3d11.4102!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3ba8590000000001%3A0x!2sOoty!5e0!3m2!1sen!2sin!4v1730000000000!5m2!1sen!2sin"
    },
    "manali": {
        "lat": 32.2396, "lon": 77.1887,
        "bg": "https://images.unsplash.com/photo-1712388430474-ace0c16051e2?auto=format&fit=crop&w=1600&q=80",
        "spots": ["Rohtang Pass", "Solang Valley", "Hadimba Temple", "Old Manali", "Manu Temple"],
        "weather": "Cold & Snowy (0–20 °C)", "food": "Siddu, Trout Fish, Momos, Thukpa",
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3430.000!2d77.1887!3d32.2396!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x390!2sManali!5e0!3m2!1sen!2sin!4v1730000000000!5m2!1sen!2sin"
    },
    "kolkata": {
        "lat": 22.5726, "lon": 88.3639,
        "bg": "https://images.unsplash.com/photo-1564507592333-c3f5b6f2b2b0?auto=format&fit=crop&w=1600&q=80",
        "spots": ["Victoria Memorial", "Howrah Bridge", "Dakshineswar Temple", "Science City", "Indian Museum"],
        "weather": "Humid (22–35 °C)", "food": "Kathi Roll, Rasgulla, Phuchka, Mishti Doi",
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3685.000!2d88.3639!3d22.5726!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a027!2sKolkata!5e0!3m2!1sen!2sin!4v1730000000000!5m2!1sen!2sin"
    },
    "kochi": {
        "lat": 9.9312, "lon": 76.2673,
        "bg": "https://images.unsplash.com/photo-1564507592333-c3f5b6f2b2b0?auto=format&fit=crop&w=1600&q=80",
        "spots": ["Chinese Fishing Nets", "Fort Kochi", "Mattancherry Palace", "Marine Drive", "Jewish Synagogue"],
        "weather": "Tropical (25–33 °C)", "food": "Appam, Fish Moilee, Kerala Sadya, Seafood",
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3929.984!2d76.2673!3d9.9312!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3b080d!2sKochi!5e0!3m2!1sen!2sin!4v1730000000000!5m2!1sen!2sin"
    },
    "kashmir": {
        "lat": 34.0837, "lon": 74.7974,
        "bg": "https://images.unsplash.com/photo-1715457573748-8e8a70b2c1be?auto=format&fit=crop&w=1600&q=80",
        "spots": ["Dal Lake", "Shalimar Bagh", "Gulmarg", "Pahalgam", "Sonamarg", "Betaab Valley"],
        "weather": "Cool to Cold (0–25 °C)", "food": "Rogan Josh, Gushtaba, Kahwa, Dum Aloo",
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3300.000!2d74.7974!3d34.0837!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x38e18f0000000001%3A0x!2sSrinagar!5e0!3m2!1sen!2sin!4v1730000000000!5m2!1sen!2sin"
    },
    "yelagiri": {
        "lat": 12.5930, "lon": 78.6294,
        "bg": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1600&q=80",
        "spots": ["Swamimalai Hill", "Punganoor Lake", "Nature Park", "Yelagiri Dam", "Jalagamparai Falls"],
        "weather": "Cool Hill Station (15–28 °C)", "food": "Local Tamil Snacks, Fresh Fruits, Hill Coffee",
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3886.984!2d78.6294!3d12.5930!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bad!2sYelagiri!5e0!3m2!1sen!2sin!4v1730000000000!5m2!1sen!2sin"
    },
    "kodaikanal": {
        "lat": 10.2396, "lon": 77.4893,
        "bg": "https://images.unsplash.com/photo-1580130718646-9f694209b207?auto=format&fit=crop&w=1600&q=80",
        "spots": ["Kodaikanal Lake", "Coaker's Walk", "Bryant Park", "Pillar Rocks", "Silver Cascade"],
        "weather": "Cool & Misty (10–25 °C)", "food": "Plum Cake, Homemade Chocolates, Masala Chai",
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3886.984!2d77.4893!3d10.2396!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3b078!2sKodaikanal!5e0!3m2!1sen!2sin!4v1730000000000!5m2!1sen!2sin"
    },
    "vellore": {
        "lat": 12.9165, "lon": 79.1325,
        "bg": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1600&q=80",
        "spots": ["Vellore Fort", "Golden Temple Sripuram", "Government Museum", "Archaeological Survey of India Museum"],
        "weather": "Hot (25–38 °C)", "food": "Idli, Dosa, Local Chettinad, Biryani",
        "map": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3886.984!2d79.1325!3d12.9165!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3a528!2sVellore!5e0!3m2!1sen!2sin!4v1730000000000!5m2!1sen!2sin"
    }
}


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "asta123"

def get_dist(l1, ln1, l2, ln2):
    R = 6371
    dlat, dlon = math.radians(l2-l1), math.radians(ln2-ln1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(l1)) * math.cos(math.radians(l2)) * math.sin(dlon/2)**2
    return round(2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a)))

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    saved = {"source": "", "dest": "", "budget": "", "days": "", "people": ""}
    if request.method == "POST":
        src_name = request.form.get("source", "").lower().strip()
        dst_name = request.form.get("destination", "").lower().strip()
        saved = {"source": src_name, "dest": dst_name, "budget": request.form.get("budget"), 
                 "days": request.form.get("days"), "people": request.form.get("people")}
        try:
            budget = float(request.form.get("budget") or 0)
            days = int(request.form.get("days") or 1)
            people = int(request.form.get("people") or 1)
            if dst_name in CITY_INTEL:
                dst = CITY_INTEL[dst_name]
                src = CITY_INTEL.get(src_name, CITY_INTEL["hyderabad"])
                distance = get_dist(src["lat"], src["lon"], dst["lat"], dst["lon"])
                t_cost, s_cost = budget * 0.25, budget * 0.35
                rem_total = budget - (t_cost + s_cost)
                result = {"to": dst_name.capitalize(), "from": src_name.capitalize(), "dist": distance, 
                          "days": days, "people": people, "daily": round(max(0, (rem_total/days)/people), 2), 
                          "transport": round(t_cost, 2), "stay": round(s_cost, 2), 
                          "remaining_total": round(max(0, rem_total), 2), **dst}
            else:
                flash(f"City '{dst_name}' not found!")
        except: flash("Check your inputs!")
    return render_template("index.html", result=result, saved=saved)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USERNAME and request.form.get("password") == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("admin"))
        flash("Invalid Credentials")
    return render_template("login.html")

@app.route("/admin")
def admin():
    if not session.get("logged_in"): return redirect(url_for("login"))
    return render_template("admin.html",cities=CITY_INTEL)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)