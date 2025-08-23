from flask import Flask, render_template, request, redirect, url_for, session
from math import radians, sin, cos, sqrt, atan2
import os
import dotenv
import pymysql
from flask import jsonify

# Load environment variables
dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "sfansofdbalsnkglasdg")

# Home location coordinates
HOME_LAT = 30.3529
HOME_LNG = 76.3637

# Access token for registration
ACCESS_TOKEN = "token123"

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "drone-dispatch-system-thapar-a4f3.c.aivencloud.com"),
    "port": int(os.getenv("DB_PORT", 23916)),
    "user": os.getenv("DB_USER", "avnadmin"),
    "password": os.getenv("DB_PASSWORD", "AVNS_jjQPJ7jxq9aVaNDMFBE"),
    "db": os.getenv("DB_NAME", "defaultdb"),
    "charset": os.getenv("DB_CHARSET", "utf8mb4"),
    "connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", 10)),
    "read_timeout": int(os.getenv("DB_READ_TIMEOUT", 10)),
    "write_timeout": int(os.getenv("DB_WRITE_TIMEOUT", 10)),
    "cursorclass": getattr(pymysql.cursors, os.getenv("DB_CURSORCLASS", "DictCursor")),
}

def get_db_connection():
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    memberType=request.form.get('memberType', 'user')
    email_error = password_error = error = None

    if not email:
        email_error = "Email is required."
    elif "@" not in email or "." not in email:
        email_error = "Invalid email address."
    if not password:
        password_error = "Password is required."

    if email_error or password_error:
        return render_template('index.html', email_error=email_error, password_error=password_error, email=email, signup_error=False)

    conn = get_db_connection()
    if not conn:
        error = "Database connection error."
        return render_template('index.html', error=error, email=email, signup_error=False)

    try:
        if memberType=='user':
            with conn.cursor() as cursor:

                cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
                user = cursor.fetchone()
            if not user:
                error = "Invalid credentials"
                return render_template('index.html', error=error, email=email, signup_error=False)
            session['user_email'] = email
            session['logged_in'] = True
            return redirect(url_for('user_dashboard'))
        elif memberType=='admin':
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM admin WHERE email = %s AND password = %s", (email, password))
                admin = cursor.fetchone()
            if not admin:
                error = "Invalid credentials"
                return render_template('index.html', error=error, email=email, signup_error=False)
            session['admin_email'] = email
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
    finally:
        conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        conn.close()

def add_user(email, password):
    conn = get_db_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding user: {e}")
        return False
    finally:
        conn.close()

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email_', '').strip()
    password = request.form.get('password_', '')
    access_token = request.form.get('access_token', '')
    email_error = password_error = access_token_error = error = None

    if not email:
        email_error = "Email is required."
    elif "@" not in email or "." not in email:
        email_error = "Invalid email address."
    elif get_user_by_email(email):
        email_error = "Email already exists."
    if not password:
        password_error = "Password is required."
    elif len(password) < 8:
        password_error = "Password must be at least 8 characters long."
    if not access_token:
        access_token_error = "Access token is required."
    elif access_token != ACCESS_TOKEN:
        access_token_error = "Invalid access token."

    if email_error or password_error or access_token_error:
        return render_template('index.html', email_error=email_error, password_error=password_error, access_token_error=access_token_error, signup_error=True, email=email, access_token=access_token, password=password)

    if not add_user(email, password):
        error = "Failed to register user."
        return render_template('index.html', error=error, signup_error=True)

    session['user_email'] = email
    session['logged_in'] = True
    return redirect(url_for('user_dashboard'))

@app.route('/user_dashboard')
def user_dashboard():
    connection= get_db_connection()
    if not connection:
        return render_template('user_dashboard.html', error="Database connection error.")
    cursor= connection.cursor()
    cursor.execute("SELECT * FROM vaccines")
    vaccines = cursor.fetchall()
    cursor.execute("SELECT * FROM deliveries WHERE user_mail = %s", (session.get('user_email'),))
    deliveries = cursor.fetchall()
    cursor.close()
    session['vaccines'] = vaccines
    session['deliveries'] = deliveries
    return render_template('user_dashboard.html')

@app.route('/tracking', methods=['GET', 'POST'])
def tracking():
    if request.method == 'POST':
        vaccine_types = request.form.getlist('vaccines')
        print(vaccine_types)
        latitude = request.form.get('lat')
        longitude = request.form.get('lng')
        vaccine_error=None
        location_error=None
        if not vaccine_types:
            vaccine_error = "Please select a vaccine type."
        if not latitude or not longitude:
            location_error = "Please provide valid latitude and longitude."
        if vaccine_error or location_error:
            return render_template("user_dashboard.html", vaccine_error=vaccine_error, location_error=location_error)
        try:
            lat2 = float(latitude)
            lon2 = float(longitude)
        except (TypeError, ValueError):
            return render_template("user_dashboard.html", error="Invalid coordinates.")

        # Haversine formula
        R = 6371  # Earth radius in kilometers
        dlat = radians(lat2 - HOME_LAT)
        dlon = radians(lon2 - HOME_LNG)
        a = sin(dlat / 2)**2 + cos(radians(HOME_LAT)) * cos(radians(lat2)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        data = {
            "vaccine_types": vaccine_types,
            "latitude": latitude,
            "longitude": longitude,
            "distance": f"{distance:.2f}"
        }

        if distance > 15:
            return render_template("user_dashboard.html", error="Drone is too far from the home location.")
        else:
            # Find vaccine_id from session vaccines
            vaccine_id = None
            for vaccine in session.get('vaccines', []):
                if vaccine['name'] == vaccine_types:
                    vaccine_id = vaccine['id']
                    break
            # Save tracking info to database
            conn = get_db_connection()
            token= ''.join(__import__('random').choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
            if conn:
                try:
                    print(f"Saving tracking info: {data}")
                    with conn.cursor() as cursor:
                        cursor.execute(
                            """
                            INSERT INTO deliveries (
                                user_mail, vaccine_id, latitude, longitude, distance_km, status, delivery_token
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """,
                            (
                                session.get('user_email'),
                                vaccine_id,
                                lat2,
                                lon2,
                                distance,
                                "Created",
                                token
                            )
                        )
                        delivery_id = cursor.lastrowid
                    conn.commit()

                    data["delivery_id"] = delivery_id

                except Exception as e:
                    print(f"Error saving tracking info: {e}")
                finally:
                    conn.close()
            return render_template("tracking.html", data=data,token=token)
    return render_template('tracking.html')



@app.route('/delivery/<int:delivery_id>/verify_token', methods=['POST'])
def verify_token(delivery_id):
    data = request.get_json()
    token = data.get('token')
    print(f"Received token verification request: delivery_id={delivery_id}, token={token}")
    import time
    # Replace with your actual token validation logic
    # For example, compare with a stored token for this delivery
    conn= get_db_connection()
    if not conn:
        print("DB connection failed")
        return jsonify({"error": "DB connection failed"}), 500
    cursor= conn.cursor()
    cursor.execute("SELECT delivery_token FROM deliveries WHERE id = %s", (delivery_id,))
    result = cursor.fetchone()
    expected_token = result['delivery_token'] if result else None
    if token == expected_token:
        return jsonify({'valid': True})
    else:
        return jsonify({'valid': False})
    
    
    
@app.route('/delivery/<int:delivery_id>/update_status', methods=['POST'])
def update_delivery_status(delivery_id):
    status = request.json.get('status')
    print(f"Received status update request: delivery_id={delivery_id}, status={status}")

    # Accept and log all status values
    allowed_statuses = [
        'created', 'drone arrived', 'dispatched', 'drone assigned',
        'attended max height', 'heading to target', 'landing',
        'returning to home station', 'dispatching vaccine', 'Drone Landing',
        'Drone Returned Home!'
    ]
    if status not in allowed_statuses:
        print(f"Warning: Received unrecognized status '{status}' for delivery_id={delivery_id}")

    conn = get_db_connection()
    if not conn:
        print("DB connection failed")
        return jsonify({"error": "DB connection failed"}), 500
    try:
        with conn.cursor() as cursor:
            print(f"Attempting to update delivery {delivery_id} status to '{status}'")
            cursor.execute("UPDATE deliveries SET status=%s WHERE id=%s", (status, delivery_id))
            print(f"Database update executed for delivery_id={delivery_id}")
        conn.commit()
        print(f"Database commit successful for delivery_id={delivery_id}")
        return jsonify({"success": True, "delivery_id": delivery_id, "status": status})
    except Exception as e:
        print(f"Error updating delivery: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
        print(f"Database connection closed for delivery_id={delivery_id}")
        
@app.route('/add_vaccine', methods=['POST'])
def add_vaccine():
    vaccine_name = request.form.get('vaccine_name', '').strip()
    image_url = request.form.get('image_url', '').strip()
    description = request.form.get('description', '').strip()
    vaccine_name_error = image_url_error = description_error =None
    if not vaccine_name:
        vaccine_name_error = "Vaccine name is required."
    if not image_url:
        image_url_error = "Image URL is required."
    if not description:
        description_error = "Description is required."
    errors={
        "vaccine_name_error": vaccine_name_error,
        "image_url_error": image_url_error,
        "description_error": description_error
    }
    if not vaccine_name:
        error = "Vaccine name is required."
        return render_template('dashboard.html', **error)
    conn = get_db_connection()
    if not conn:
        error = "Database connection error."
        return render_template('dashboard.html', error=error)
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO vaccines (name, image_url, description) VALUES (%s, %s, %s)",
                (vaccine_name, image_url, description)
            )
        conn.commit()
    except Exception as e:
        print(f"Error adding vaccine: {e}")
        error = "Failed to add vaccine."
        return render_template('dashboard.html', error=error)
    finally:
        conn.close()
    return redirect(url_for('admin_dashboard'))
@app.route('/delete_vaccine/<int:vaccine_id>', methods=['POST'])
def delete_vaccine(vaccine_id):
    print("here")
    conn = get_db_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM vaccines WHERE id = %s", (vaccine_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting vaccine: {e}")
        return False
    finally:
        conn.close()
        return redirect(url_for('admin_dashboard'))
@app.route('/delete_user/<string:user_mail>', methods=['POST'])
def delete_user(user_mail):
    conn = get_db_connection()
    if not conn:
        return render_template('dashboard.html', error="Database connection error.")
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE email = %s", (user_mail,))
        conn.commit()
    except Exception as e:
        print(f"Error deleting user: {e}")
        return render_template('dashboard.html', error="Failed to delete user.")
    finally:
        conn.close()
    print("User deleted successfully.")
    return redirect(url_for('admin_dashboard'))
@app.route('/delete_admin/<string:user_mail>', methods=['POST'])
def delete_admin(user_mail):
    conn = get_db_connection()
    if not conn:
        return render_template('dashboard.html', error="Database connection error.")
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM admin WHERE email = %s", (user_mail,))
        conn.commit()
    except Exception as e:
        print(f"Error deleting user: {e}")
        return render_template('dashboard.html', error="Failed to delete user.")
    finally:
        conn.close()
    print("User deleted successfully.")
    return redirect(url_for('admin_dashboard'))

@app.route('/add_admin', methods=['POST'])
def add_admin():
    email = request.form.get('admin_email', '').strip()
    password = request.form.get('admin_password', '')
    email_error = password_error = error = None

    if not email:
        email_error = "Email is required."
    elif ("@" not in email or "." not in email):
        email_error = "Invalid email address."
    
    if not password:
        password_error = "Password is required."
    elif len(password) < 8:
        password_error = "Password must be at least 8 characters long."
    conn = get_db_connection()
    if not conn:
        error = "Database connection error."
        return render_template('dashboard.html', error=error,email=email, email_error=email_error, password_error=password_error)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM admin WHERE email = %s", (email,))
            existing_admin = cursor.fetchone()
            if existing_admin:
                email_error = "Admin email already exists."
        if not password:
            password_error = "Password is required."
        elif len(password) < 8:
            password_error = "Password must be at least 8 characters long."
        if email_error or password_error:
            return render_template('dashboard.html', email_error=email_error, password_error=password_error)
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO admin (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
    except Exception as e:
        print(f"Error adding admin: {e}")
        error = "Failed to add admin."
        return render_template('dashboard.html', error=error)
    finally:
        conn.close()
    return redirect(url_for('admin_dashboard'))
    
        
@app.route('/delete_delivery/<int:delivery_id>', methods=['POST'])
def delete_delivery(delivery_id):
    conn = get_db_connection()
    if not conn:
        return render_template('dashboard.html', error="Database connection error.")
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM deliveries WHERE id = %s", (delivery_id,))
        conn.commit()
    except Exception as e:
        print(f"Error deleting delivery: {e}")
        return render_template('dashboard.html', error="Failed to delete delivery.")
    finally:
        conn.close()
    print("Delivery deleted successfully.")
    return redirect(url_for('admin_dashboard'))
        

@app.route('/admin_dashboard')
def admin_dashboard():
    connection= get_db_connection()
    if not connection:
        return render_template('dashboard.html', error="Database connection error.")
    cursor= connection.cursor()
    cursor.execute("SELECT * FROM vaccines")
    vaccines = cursor.fetchall()
    cursor.execute("SELECT d.*,v.name,v.image_url FROM deliveries d JOIN vaccines v ON d.vaccine_id = v.id")
    deliveries = cursor.fetchall()
    cursor.execute("SELECT `email`,`created_at` FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT * FROM admin")
    admins = cursor.fetchall()
    cursor.execute("select count(*) from deliveries")
    total_requests= cursor.fetchone()['count(*)']
    cursor.execute("select count(*) from deliveries where status in ('dispatching vaccine', 'delivered', 'returning to home station')")
    total_deliveries = cursor.fetchone()['count(*)']
    cursor.execute("select count(*) from deliveries where status in ('token failed', 'delivery failed')")
    failed_deliveries = cursor.fetchone()['count(*)']
    x=total_requests - total_deliveries-failed_deliveries
    cursor.close()
    messages = {
        "vaccines": vaccines,
        "deliveries": deliveries,
        "users": users,
        "admins": admins,
        "total_users": len(users),
        "total_drones": 1,
        "total_deliveries": total_deliveries,
        "pending_deliveries": max(x, 0),
        "total_requests": total_requests,
        "failed_deliveries": failed_deliveries
    }
    return render_template('dashboard.html',**messages )


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
