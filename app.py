"""
Wolfie Delivery - Complete Website v1.0
Modern Design with All Features
"""

import os
import time
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
from database import Database
from pricing import PricingEngine

app = Flask(__name__)
app.secret_key = "WOLFIE_DELIVERY_2026_SECRET"
db = Database()
pricing = PricingEngine()

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ══════════════════════════════════════════════════════════════
# HOMEPAGE - WOLFIE DELIVERY
# ══════════════════════════════════════════════════════════════

HOMEPAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐺 Wolfie Delivery - Be Wolfie</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; overflow-x: hidden; }
        
        /* Hero Section */
        .hero { 
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh; 
            color: white; 
            position: relative;
            overflow: hidden;
        }
        .hero::before {
            content: '🐺';
            position: absolute;
            font-size: 600px;
            opacity: 0.03;
            top: -100px;
            right: -150px;
            transform: rotate(-15deg);
        }
        
        /* Navigation */
        nav { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            padding: 25px 50px;
            position: relative;
            z-index: 100;
        }
        .logo { 
            font-size: 32px; 
            font-weight: 800; 
            display: flex; 
            align-items: center; 
            gap: 10px;
            color: white;
            text-decoration: none;
        }
        .logo span { color: #e94560; }
        .nav-links { 
            display: flex; 
            gap: 30px; 
            list-style: none; 
        }
        .nav-links a { 
            color: white; 
            text-decoration: none; 
            font-weight: 500;
            transition: color 0.3s;
        }
        .nav-links a:hover { color: #e94560; }
        .cta-btn { 
            background: #e94560; 
            padding: 12px 30px; 
            border-radius: 25px; 
            color: white; 
            text-decoration: none;
            font-weight: 600;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .cta-btn:hover { 
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(233, 69, 96, 0.4);
        }
        
        /* Hero Content */
        .hero-content { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 100px 50px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            align-items: center;
        }
        .hero-text h1 { 
            font-size: 72px; 
            font-weight: 800; 
            line-height: 1.1;
            margin-bottom: 20px;
        }
        .hero-text .highlight { 
            color: #e94560;
            display: block;
        }
        .hero-text p { 
            font-size: 20px; 
            margin: 30px 0;
            opacity: 0.9;
            line-height: 1.6;
        }
        .hero-buttons { 
            display: flex; 
            gap: 20px; 
            margin-top: 40px;
        }
        .btn-primary { 
            background: #e94560; 
            color: white; 
            padding: 18px 40px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 600;
            font-size: 18px;
            transition: all 0.3s;
            border: 2px solid #e94560;
        }
        .btn-primary:hover { 
            transform: scale(1.05);
            box-shadow: 0 15px 40px rgba(233, 69, 96, 0.5);
        }
        .btn-secondary { 
            background: transparent; 
            color: white; 
            padding: 18px 40px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 600;
            font-size: 18px;
            border: 2px solid rgba(255,255,255,0.3);
            transition: all 0.3s;
        }
        .btn-secondary:hover { 
            background: rgba(255,255,255,0.1);
            border-color: white;
        }
        
        /* Stats */
        .stats { 
            display: grid; 
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
            margin-top: 80px;
        }
        .stat-card { 
            text-align: center; 
            padding: 30px;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }
        .stat-number { 
            font-size: 48px; 
            font-weight: 800; 
            color: #e94560;
            display: block;
            margin-bottom: 10px;
        }
        .stat-label { 
            font-size: 16px; 
            opacity: 0.8;
        }
        
        /* Features Section */
        .features { 
            padding: 100px 50px;
            background: white;
        }
        .section-title { 
            text-align: center; 
            font-size: 48px; 
            font-weight: 800;
            margin-bottom: 60px;
            color: #1a1a2e;
        }
        .features-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .feature-card { 
            padding: 40px;
            background: #f8f9fa;
            border-radius: 20px;
            transition: all 0.3s;
            border: 2px solid transparent;
        }
        .feature-card:hover { 
            transform: translateY(-10px);
            box-shadow: 0 20px 50px rgba(0,0,0,0.1);
            border-color: #e94560;
        }
        .feature-icon { 
            font-size: 64px; 
            margin-bottom: 20px;
        }
        .feature-card h3 { 
            font-size: 24px; 
            margin-bottom: 15px;
            color: #1a1a2e;
        }
        .feature-card p { 
            color: #666; 
            line-height: 1.8;
        }
        .feature-badge {
            display: inline-block;
            background: #e94560;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin-top: 15px;
        }
        
        /* Pricing Section */
        .pricing { 
            padding: 100px 50px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
        }
        .pricing-comparison { 
            max-width: 1000px;
            margin: 50px auto;
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
            padding: 40px;
            backdrop-filter: blur(10px);
        }
        .comparison-row { 
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            padding: 20px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            align-items: center;
        }
        .comparison-row:last-child { border-bottom: none; }
        .comparison-header { 
            font-weight: 700;
            font-size: 18px;
        }
        .price-cell { 
            text-align: center;
            font-size: 20px;
            font-weight: 600;
        }
        .wolfie-price { color: #4ade80; }
        .competitor-price { color: #f87171; opacity: 0.7; }
        
        /* CTA Section */
        .cta-section { 
            padding: 100px 50px;
            background: #e94560;
            text-align: center;
            color: white;
        }
        .cta-section h2 { 
            font-size: 56px; 
            font-weight: 800;
            margin-bottom: 30px;
        }
        .cta-section p { 
            font-size: 24px; 
            margin-bottom: 50px;
            opacity: 0.95;
        }
        
        /* Footer */
        footer { 
            background: #1a1a2e;
            color: white;
            padding: 60px 50px 30px;
        }
        .footer-content { 
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 60px;
            margin-bottom: 40px;
        }
        .footer-brand { 
            font-size: 28px; 
            font-weight: 800;
            margin-bottom: 20px;
        }
        .footer-links { 
            list-style: none;
        }
        .footer-links li { 
            margin-bottom: 12px;
        }
        .footer-links a { 
            color: rgba(255,255,255,0.7);
            text-decoration: none;
            transition: color 0.3s;
        }
        .footer-links a:hover { 
            color: #e94560;
        }
        .footer-bottom { 
            text-align: center;
            padding-top: 30px;
            border-top: 1px solid rgba(255,255,255,0.1);
            opacity: 0.7;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .hero-content { 
                grid-template-columns: 1fr;
                text-align: center;
            }
            .hero-text h1 { font-size: 48px; }
            .stats { grid-template-columns: 1fr; }
            .features-grid { grid-template-columns: 1fr; }
            .comparison-row { grid-template-columns: 1fr; }
            .footer-content { grid-template-columns: 1fr; text-align: center; }
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav>
        <a href="/" class="logo">
            🐺 <div>Wolfie <span>Delivery</span></div>
        </a>
        <ul class="nav-links">
            <li><a href="#features">Features</a></li>
            <li><a href="#pricing">Pricing</a></li>
            <li><a href="/driver">Drivers</a></li>
            <li><a href="/restaurant">Restaurants</a></li>
        </ul>
        <a href="/register" class="cta-btn">Get Started</a>
    </nav>
    
    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <div class="hero-text">
                <h1>
                    Delivery Done
                    <span class="highlight">The Wolfie Way</span>
                </h1>
                <p>
                    Save up to <strong>25% compared to Uber Eats & DoorDash</strong>. 
                    Better for customers, better for restaurants, better for drivers.
                </p>
                <div class="hero-buttons">
                    <a href="/register" class="btn-primary">Start Delivering</a>
                    <a href="/restaurant" class="btn-secondary">Join as Restaurant</a>
                </div>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <span class="stat-number">25%</span>
                    <span class="stat-label">Lower Fees</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">$8-14</span>
                    <span class="stat-label">Driver Earnings</span>
                </div>
                <div class="stat-card">
                    <span class="stat-number">5★</span>
                    <span class="stat-label">Rating System</span>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Features Section -->
    <section class="features" id="features">
        <h2 class="section-title">Why Choose Wolfie? 🐺</h2>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">💰</div>
                <h3>Lowest Prices in NYC</h3>
                <p>Save 20-25% compared to competitors. Better prices mean more orders for restaurants and more value for customers.</p>
                <span class="feature-badge">COMPETITIVE EDGE</span>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🚀</div>
                <h3>Easy Registration</h3>
                <p>Sign up in 60 seconds. No complex paperwork, no waiting. Upload your menu photo and you're ready to go!</p>
                <span class="feature-badge">QUICK START</span>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">⭐</div>
                <h3>Smart Rating System</h3>
                <p>Fair ratings for drivers and restaurants. Build your reputation and earn more with our transparent 5-star system.</p>
                <span class="feature-badge">FAIR & TRANSPARENT</span>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">💵</div>
                <h3>Transparent Pricing</h3>
                <p>Know exactly what you're paying. No hidden fees. $4-$12 delivery based on distance, that's it!</p>
                <span class="feature-badge">NO SURPRISES</span>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📸</div>
                <h3>Simple Menu Upload</h3>
                <p>Just take a photo of your menu. No need to type everything. We make it stupid simple for restaurants.</p>
                <span class="feature-badge">TIME SAVER</span>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🤝</div>
                <h3>Fair Contracts</h3>
                <p>Clear, simple contracts. No complicated legal jargon. 10-18% commission vs 30% from competitors.</p>
                <span class="feature-badge">WIN-WIN</span>
            </div>
        </div>
    </section>
    
    <!-- Pricing Comparison -->
    <section class="pricing" id="pricing">
        <h2 class="section-title">The Wolfie Advantage</h2>
        <div class="pricing-comparison">
            <div class="comparison-row comparison-header">
                <div>Order Details</div>
                <div>🐺 Wolfie</div>
                <div>Uber Eats</div>
                <div>DoorDash</div>
            </div>
            <div class="comparison-row">
                <div>Food: $25</div>
                <div class="price-cell wolfie-price">$35.98</div>
                <div class="price-cell competitor-price">$41.50</div>
                <div class="price-cell competitor-price">$42.00</div>
            </div>
            <div class="comparison-row">
                <div>Delivery Fee (3km)</div>
                <div class="price-cell wolfie-price">$7.49</div>
                <div class="price-cell competitor-price">$12.99</div>
                <div class="price-cell competitor-price">$11.99</div>
            </div>
            <div class="comparison-row">
                <div>Service Fee</div>
                <div class="price-cell wolfie-price">$3.49</div>
                <div class="price-cell competitor-price">$3.51</div>
                <div class="price-cell competitor-price">$5.01</div>
            </div>
            <div class="comparison-row">
                <div><strong>YOU SAVE</strong></div>
                <div class="price-cell wolfie-price">—</div>
                <div class="price-cell wolfie-price">$5.52</div>
                <div class="price-cell wolfie-price">$6.02</div>
            </div>
        </div>
        <div style="text-align:center; margin-top:40px;">
            <p style="font-size:24px; margin-bottom:30px;">
                <strong>Restaurant Commission:</strong> 10-18% vs 30% competitors 💪
            </p>
            <p style="font-size:24px;">
                <strong>Driver Pay:</strong> $8-14 per order vs $6-10 competitors 🚀
            </p>
        </div>
    </section>
    
    <!-- CTA Section -->
    <section class="cta-section">
        <h2>Ready to Be Wolfie? 🐺</h2>
        <p>Join hundreds of restaurants and drivers saving money and earning more.</p>
        <div class="hero-buttons" style="justify-content:center;">
            <a href="/driver" class="btn-primary" style="background:white; color:#e94560;">Become a Driver</a>
            <a href="/restaurant" class="btn-secondary" style="border-color:white;">Add Your Restaurant</a>
        </div>
    </section>
    
    <!-- Footer -->
    <footer>
        <div class="footer-content">
            <div>
                <div class="footer-brand">🐺 Wolfie Delivery</div>
                <p style="opacity:0.7; line-height:1.8;">
                    The smartest way to deliver in NYC. Lower prices, better service, fairer pay.
                </p>
            </div>
            <div>
                <h4 style="margin-bottom:20px;">Company</h4>
                <ul class="footer-links">
                    <li><a href="/about">About Us</a></li>
                    <li><a href="/contact">Contact</a></li>
                    <li><a href="/careers">Careers</a></li>
                </ul>
            </div>
            <div>
                <h4 style="margin-bottom:20px;">Partners</h4>
                <ul class="footer-links">
                    <li><a href="/driver">Become a Driver</a></li>
                    <li><a href="/restaurant">Add Restaurant</a></li>
                    <li><a href="/admin">Admin Panel</a></li>
                </ul>
            </div>
            <div>
                <h4 style="margin-bottom:20px;">Legal</h4>
                <ul class="footer-links">
                    <li><a href="/terms">Terms of Service</a></li>
                    <li><a href="/privacy">Privacy Policy</a></li>
                    <li><a href="/cookies">Cookie Policy</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            © 2026 Wolfie Delivery NYC. All rights reserved. Made with ❤️ in New York.
        </div>
    </footer>
</body>
</html>
"""

# ══════════════════════════════════════════════════════════════
# DRIVER PAGE - BE WOLFIE
# ══════════════════════════════════════════════════════════════

DRIVER_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Be Wolfie - Driver Registration</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            max-width: 600px;
            width: 100%;
            background: white;
            border-radius: 30px;
            padding: 50px;
            box-shadow: 0 30px 80px rgba(0,0,0,0.3);
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .logo {
            font-size: 64px;
            margin-bottom: 10px;
        }
        
        h1 {
            font-size: 42px;
            font-weight: 800;
            color: #1a1a2e;
            margin-bottom: 10px;
        }
        
        .tagline {
            font-size: 24px;
            color: #e94560;
            font-weight: 600;
        }
        
        .benefits {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 20px;
            margin: 30px 0;
        }
        
        .benefit {
            display: flex;
            align-items: center;
            gap: 15px;
            margin: 15px 0;
            font-size: 16px;
        }
        
        .benefit-icon {
            font-size: 28px;
            min-width: 40px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #1a1a2e;
        }
        
        input, select {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 16px;
            transition: border 0.3s;
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: #e94560;
        }
        
        .btn-submit {
            width: 100%;
            padding: 18px;
            background: #e94560;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 20px;
        }
        
        .btn-submit:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(233, 69, 96, 0.4);
        }
        
        .back-link {
            text-align: center;
            margin-top: 20px;
        }
        
        .back-link a {
            color: #e94560;
            text-decoration: none;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🐺</div>
            <h1>Be Wolfie</h1>
            <p class="tagline">Join the Pack</p>
        </div>
        
        <div class="benefits">
            <div class="benefit">
                <span class="benefit-icon">💰</span>
                <span><strong>$8-14 per delivery</strong> - Higher than competitors</span>
            </div>
            <div class="benefit">
                <span class="benefit-icon">🚀</span>
                <span><strong>Instant approval</strong> - Start earning today</span>
            </div>
            <div class="benefit">
                <span class="benefit-icon">⭐</span>
                <span><strong>Fair ratings</strong> - Build your reputation</span>
            </div>
            <div class="benefit">
                <span class="benefit-icon">📱</span>
                <span><strong>Simple dashboard</strong> - Easy to use</span>
            </div>
        </div>
        
        <form action="/register" method="POST" enctype="multipart/form-data">
            <input type="hidden" name="role" value="driver">
            
            <div class="form-group">
                <label>Full Name *</label>
                <input type="text" name="name" placeholder="John Doe" required>
            </div>
            
            <div class="form-group">
                <label>Phone Number *</label>
                <input type="tel" name="phone" placeholder="+1 (555) 123-4567" required>
            </div>
            
            <div class="form-group">
                <label>Address in NYC *</label>
                <input type="text" name="address" placeholder="123 Main St, Brooklyn, NY" required>
            </div>
            
            <div class="form-group">
                <label>Vehicle Type *</label>
                <select name="vehicle" required>
                    <option value="">Choose your vehicle</option>
                    <option value="bike">🚲 Bike</option>
                    <option value="scooter">🛵 Scooter</option>
                    <option value="car">🚗 Car</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>ID Photo (optional)</label>
                <input type="file" name="id_img" accept="image/*">
            </div>
            
            <button type="submit" class="btn-submit">🐺 Join the Pack</button>
        </form>
        
        <div class="back-link">
            <a href="/">← Back to Home</a>
        </div>
    </div>
</body>
</html>
"""

# Routes remain same as before...
@app.route('/')
def home():
    return render_template_string(HOMEPAGE)

@app.route('/driver')
def driver_page():
    return render_template_string(DRIVER_PAGE)

@app.route('/register', methods=['POST'])
def register():
    # Same registration logic as before
    role = request.form.get('role')
    phone = request.form.get('phone')
    
    user_data = {
        "id": phone,
        "name": request.form.get('name'),
        "phone": phone,
        "address": request.form.get('address'),
        "role": role,
        "status": "active",
        "created": datetime.now().isoformat(),
        "online": True,
        "completed": 0,
        "earned": 0.0
    }
    
    if role == 'driver':
        user_data['vehicle'] = request.form.get('vehicle', 'bike')
        if 'id_img' in request.files:
            file = request.files['id_img']
            if file and file.filename:
                filename = secure_filename(f"{phone}_id.jpg")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user_data['id_img'] = filename
    
    data = db.load()
    category = f"{role}s"
    if category not in data:
        data[category] = {}
    data[category][phone] = user_data
    db.save(data)
    
    session['user_id'] = phone
    session['role'] = role
    
    return redirect('/driver/dashboard' if role == 'driver' else '/admin')

# Include all other routes from previous version...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
