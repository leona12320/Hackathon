from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import init_db, get_db, close_db

app = Flask(__name__)
app.secret_key = 'zero-hunger-secret-key-2024'

# Initialize database on startup
init_db()

# ============ HOME PAGE ============
@app.route("/")
def home():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as count FROM pledges WHERE status='active'")
    pledge_count = c.fetchone()['count']
    close_db(conn)
    return render_template("home/home.html", pledge_count=pledge_count)

# ============ NGOs PAGE ============
@app.route("/ngos")
def ngos():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM ngos ORDER BY name")
    ngo_list = c.fetchall()
    close_db(conn)
    return render_template("home/ngos.html", ngos=ngo_list)

# ============ FOOD BANKS PAGE ============
@app.route("/foodbanks")
def foodbanks():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM food_banks ORDER BY name")
    bank_list = c.fetchall()
    close_db(conn)
    return render_template("home/foodbanks.html", foodbanks=bank_list)

# ============ COMMUNITY KITCHENS PAGE ============
@app.route("/community")
def community():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM community_kitchens ORDER BY name")
    kitchens = c.fetchall()
    close_db(conn)
    return render_template("home/community.html", kitchens=kitchens)

# ============ DONATE PAGE ============
@app.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        donor_name = request.form.get('donor_name', '').strip()
        donor_email = request.form.get('donor_email', '').strip()
        donation_type = request.form.get('donation_type', '').strip()
        amount = request.form.get('amount', '').strip()
        
        # Validation
        if not donor_name or not donor_email or not donation_type or not amount:
            flash('✗ Please fill in all fields.', 'error')
            return redirect(url_for('donate'))
        
        try:
            conn = get_db()
            c = conn.cursor()
            c.execute("INSERT INTO donations (donor_name, donor_email, donation_type, amount) VALUES (?, ?, ?, ?)",
                     (donor_name, donor_email, donation_type, amount))
            conn.commit()
            close_db(conn)
            flash('✓ Thank you for your donation! We truly appreciate your support.', 'success')
            return redirect(url_for('donate'))
        except Exception as e:
            flash('✗ Error saving donation. Please try again.', 'error')
    
    return render_template("home/donate.html")

# ============ PLEDGE PAGE ============
@app.route("/pledge", methods=["GET", "POST"])
def pledge():
    if request.method == "POST":
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        pledge_text = request.form.get('pledge', '').strip()
        
        if not name or not email or not pledge_text:
            flash('✗ Please fill in all fields.', 'error')
            return redirect(url_for('pledge'))
        
        if len(pledge_text) < 10:
            flash('✗ Pledge must be at least 10 characters.', 'error')
            return redirect(url_for('pledge'))
        
        try:
            conn = get_db()
            c = conn.cursor()
            c.execute("INSERT INTO pledges (name, email, pledge_text) VALUES (?, ?, ?)",
                     (name, email, pledge_text))
            conn.commit()
            close_db(conn)
            flash('✓ Pledge recorded successfully! Thank you for your commitment.', 'success')
            return redirect(url_for('pledge'))
        except Exception as e:
            flash('✗ This email already has an active pledge.', 'error')
    
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as count FROM pledges WHERE status='active'")
    total_pledges = c.fetchone()['count']
    close_db(conn)
    
    return render_template("home/pledge.html", total_pledges=total_pledges)

# ============ ADMIN: VIEW ALL PLEDGES ============
@app.route("/admin/pledges")
def admin_pledges():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM pledges WHERE status='active' ORDER BY created_at DESC")
    pledges = c.fetchall()
    close_db(conn)
    return render_template("admin/pledges.html", pledges=pledges)

# ============ ADMIN: VIEW STATISTICS ============
@app.route("/admin/stats")
def admin_stats():
    conn = get_db()
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) as count FROM pledges WHERE status='active'")
    total_pledges = c.fetchone()['count']
    
    c.execute("SELECT COUNT(*) as count FROM donations")
    total_donations = c.fetchone()['count']
    
    c.execute("SELECT SUM(CAST(amount AS FLOAT)) as total FROM donations")
    total_amount = c.fetchone()['total'] or 0
    
    c.execute("SELECT COUNT(*) as count FROM ngos")
    total_ngos = c.fetchone()['count']
    
    close_db(conn)
    
    return render_template("admin/stats.html", 
                         total_pledges=total_pledges,
                         total_donations=total_donations,
                         total_amount=total_amount,
                         total_ngos=total_ngos)

# ============ API: GET STATS ============
@app.route("/api/stats")
def api_stats():
    conn = get_db()
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) as count FROM pledges WHERE status='active'")
    pledge_count = c.fetchone()['count']
    
    c.execute("SELECT COUNT(*) as count FROM ngos")
    ngo_count = c.fetchone()['count']
    
    c.execute("SELECT COUNT(*) as count FROM food_banks")
    bank_count = c.fetchone()['count']
    
    close_db(conn)
    
    return jsonify({
        "total_pledges": pledge_count,
        "total_ngos": ngo_count,
        "total_food_banks": bank_count
    })

if __name__ == "__main__":
    app.run(debug=True)
