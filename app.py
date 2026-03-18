#!/usr/bin/python3

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
#import mysql.connector
import bcrypt
import requests
import os
import pymysql

application = Flask(__name__)

app = application

app.secret_key = '12345'

db_config = {
    'host': 'rds-x23289678.c2qx8l1p5uig.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'rds-x23289678',
    'database': 'rds-x23289678'
}

# Route for landing page
@app.route('/')
def landing():
    return  render_template('signin.html')


# Route for home page
@app.route('/home')
def home():
    # Check if the user is authenticated
    if 'email' in session:
        if session['email'] == 'admin@frb.com':
            return redirect(url_for('admin_panel'))
        else:
            # For regular users, continue with the existing functionality
            cart_count = get_cart_count()
            return render_template('index.html', cart_count=cart_count)
    else:
        return redirect(url_for('signin'))

# Route for recipe
@app.route('/recipe')
def recipe():
    # checks items on the cart
    cart_count = get_cart_count()
    return render_template('recipe.html', cart_count=cart_count)


# Route for the product page
@app.route('/products')
def products():
    # Connect to the MySQL database
    cnx = pymysql.connect(**db_config)
    cursor = cnx.cursor()

    # Retrieve product data from the database
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # Render the template and pass the product data to it
    cart_count = get_cart_count()
    return render_template('shop.html', products=products, cart_count=cart_count)


def get_cart_count():
    # Check if the user is authenticated
    if 'email' in session:
        # Connect to the MySQL database
        cnx = pymysql.connect(**db_config)
        cursor = cnx.cursor()

        # Retrieve the cart count for the user
        select_query = """
        SELECT COUNT(CP.ProductId)
        FROM cartproduct CP
        JOIN cart C ON CP.CartId = C.Id
        JOIN user U ON C.UserId = U.Id
        WHERE U.Email = %s
        """
        cursor.execute(select_query, (session['email'],))
        cart_count = cursor.fetchone()[0]

        # Close the cursor and connection
        cursor.close()
        cnx.close()

        return cart_count

    pass


# Route for sign up
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Connect to the MySQL database
        cnx = pymysql.connect(**db_config)
        cursor = cnx.cursor()

        # Check if the email already exists in the database
        select_query = "SELECT * FROM user WHERE Email = %s"
        cursor.execute(select_query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            # If the email already exists, display an error message
            error_message = 'Email already exists. Please choose a different email.'
            return render_template('signup.html', error_message=error_message)
        else:
            # Insert the user data into the database
            insert_query = "INSERT INTO user (Name, Email, Password, Phone) VALUES (%s, %s, %s, %s)"
            user_data = (name, email, hashed_password.decode('utf-8'), phone)  # Store the hashed password
            cursor.execute(insert_query, user_data)

            # Commit the changes
            cnx.commit()

        # Close the cursor and connection
        cursor.close()
        cnx.close()

        # Create a session for the user
        session['email'] = email

        # Redirect to the profile page
        return redirect(url_for('profile'))
    else:
        return render_template('signup.html')


# Route for sign in
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Retrieve form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Connect to the MySQL database
        cnx = pymysql.connect(**db_config)
        cursor = cnx.cursor()

        # Retrieve the hashed password from the database
        query = "SELECT Password FROM user WHERE Email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result:
            hashed_password = result[0]
            # Verify the password
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                # If credentials are valid, create a session for the user
                session['email'] = email

                # Redirect to the home page
                return redirect(url_for('home'))

        # User not found or invalid credentials
        cursor.close()
        cnx.close()
        return render_template('signup.html')

        # Close the cursor and connection
        

    # If it's a GET request and the user is already signed in, redirect to the home page
    if 'email' in session:
        return redirect(url_for('home'))

    # If it's a GET request and the user is not signed in, render the sign-in page
    return render_template('signin.html')


@app.route('/profile')
def profile():
    # Check if the user is authenticated (session exists)
    if 'email' in session:
        # Connect to the MySQL database
        cnx = pymysql.connect(**db_config)
        cursor = cnx.cursor()

        # Retrieve user data from the database
        cursor.execute("SELECT * FROM user WHERE Email = %s", (session['email'],))
        user = cursor.fetchone()

         # Retrieve shipping info from database
        select_shipping_query = """
        SELECT * FROM shipping
        INNER JOIN user ON shipping.UserId = user.Id
        WHERE user.Email = %s
        """
        cursor.execute(select_shipping_query, (session['email'],))
        shipping_info = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        cnx.close()

        # checks items on the cart
        cart_count = get_cart_count()

        # Render the template and pass the user data to it
        return render_template('profile.html', user=user, shipping_info=shipping_info, cart_count=cart_count)
    else:
        return redirect(url_for('signin'))


# Route for signing out
@app.route('/signout')
def signout():
    # Clear the session
    session.clear()

    # Redirect to the sign-in page
    return redirect(url_for('signin'))


@app.route('/search')
def search():
    # Get the search query from the request's query parameters
    query = request.args.get('query')

    # Check if the query is None or empty
    if not query or query.strip() == '':
        # Handle the case when no query is provided
        return redirect(url_for('products'))

    # Connect to the MySQL database
    cnx = pymysql.connect(**db_config)
    cursor = cnx.cursor()

    # Search for products matching the query
    search_query = "SELECT * FROM product WHERE Name LIKE %s OR Description LIKE %s"
    pattern = f'%{query}%'
    cursor.execute(search_query, (pattern, pattern))
    products = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # checks items on the cart
    cart_count = get_cart_count()

    # Render the template and pass the product data to it
    return render_template('search_results.html', products=products, query=query, cart_count=cart_count)

@app.route('/cart')
def cart():
    if 'email' not in session:
        return redirect(url_for('signin'))

    cnx = pymysql.connect(**db_config)
    cursor = cnx.cursor()

    select_query = """
    SELECT P.Id, P.Name, P.Description, P.Price, P.Image, P.Category
    FROM cartproduct CP
    JOIN product P ON CP.ProductId = P.Id
    JOIN cart C ON CP.CartId = C.Id
    JOIN user U ON C.UserId = U.Id
    WHERE U.Email = %s
    """
    cursor.execute(select_query, (session['email'],))
    cart_products = cursor.fetchall()

    total_query = """
    SELECT SUM(P.Price)
    FROM cartproduct CP
    JOIN product P ON CP.ProductId = P.Id
    JOIN cart C ON CP.CartId = C.Id
    JOIN user U ON C.UserId = U.Id
    WHERE U.Email = %s
    """
    cursor.execute(total_query, (session['email'],))
    total_price = cursor.fetchone()[0]

    if total_price is None:
        total_price = 0

    count_query = """
    SELECT COUNT(*)
    FROM cartproduct CP
    JOIN cart C ON CP.CartId = C.Id
    JOIN user U ON C.UserId = U.Id
    WHERE U.Email = %s
    """
    cursor.execute(count_query, (session['email'],))
    cart_count = cursor.fetchone()[0]

    cursor.close()
    cnx.close()

    return render_template(
        'cart.html',
        cart_products=cart_products,
        total_price=total_price,
        cart_count=cart_count
    )

import requests


@app.route('/apply_coupon_cart', methods=['POST'])
def apply_coupon_cart():

    data = request.get_json()

    total_price = float(data.get("total_amount", 0))
    coupon = data.get("coupon_code")

    final_price = apply_coupon(total_price, coupon)

    discount = total_price - final_price

    session["discount"] = discount
    session["discounted_total"] = final_price

    return jsonify({
        "status": "success",
        "final_price": final_price,
        "discount_amount": round(discount, 2)
    })

def apply_coupon(total_price, coupon):

    # url = "http://localhost:5001/apply_coupon"
    url = "https://v2hjgc2fa3.execute-api.us-east-1.amazonaws.com/default/discount-api-x23289678"

    payload = {
        "total_amount": total_price,
        "coupon_code": coupon
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data["final_price"]

    return total_price


# Route for adding a product to the cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'email' not in session:
        return redirect(url_for('signin'))

    # Retrieve the product ID from the request form
    product_id = request.form.get('product_id')

    # Connect to the MySQL database
    cnx = pymysql.connect(**db_config)
    cursor = cnx.cursor()

    # Retrieve the user's cart ID
    select_cart_query = "SELECT Id FROM cart WHERE UserId = (SELECT Id FROM user WHERE Email = %s)"
    cursor.execute(select_cart_query, (session['email'],))
    cart_row = cursor.fetchone()

    # Check if the user has an active cart
    if cart_row:
        cart_id = cart_row[0]
    else:
        # If the user does not have a cart, create a new cart
        insert_cart_query = "INSERT INTO cart (UserId) SELECT Id FROM user WHERE Email = %s"
        cursor.execute(insert_cart_query, (session['email'],))
        cnx.commit()

        # Retrieve the new cart ID
        cart_id = cursor.lastrowid

    # Insert the product into the user's cart
    insert_cart_product_query = "INSERT INTO cartproduct (CartId, ProductId) VALUES (%s, %s)"
    cart_product_data = (cart_id, product_id)
    cursor.execute(insert_cart_product_query, cart_product_data)
    cnx.commit()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # Redirect back to the products page
    return jsonify({'status': 'success'})


# Route for removing a product from the cart
@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    # Check if the user is authenticated
    if 'email' not in session:
        return redirect(url_for('signin'))

    # Get the product ID from the request form
    product_id = request.form.get('product_id')

    # Connect to the MySQL database
    cnx = pymysql.connect(**db_config)
    cursor = cnx.cursor()

    # Retrieve the user's cart ID
    select_cart_query = "SELECT Id FROM cart WHERE UserId = (SELECT Id FROM User WHERE Email = %s)"
    cursor.execute(select_cart_query, (session['email'],))
    cart_id = cursor.fetchone()[0]

    # Delete the product from the user's cart
    delete_query = "DELETE FROM cartproduct WHERE CartId = %s AND ProductId = %s"
    cursor.execute(delete_query, (cart_id, product_id))

    # Commit the changes
    cnx.commit()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # Redirect back to the cart page
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Check if the user is authenticated
    if 'email' not in session:
        return redirect(url_for('signin'))

    # Connect to the MySQL database
    # total_final_price = session["discounted_total"]
    total_final_price = session.get("discounted_total")
    discount_amount = session.get("discount", 0)
    


    cnx = pymysql.connect(**db_config)
    cursor = cnx.cursor()

    # Retrieve cart data for the user from the database
    select_query = """
    SELECT P.Id, P.Name, P.Description, P.Price, P.Image, P.Category
    FROM cartproduct CP
    JOIN product P ON CP.ProductId = P.Id
    JOIN cart C ON CP.CartId = C.Id
    JOIN user U ON C.UserId = U.Id
    WHERE U.Email = %s
    """
    cursor.execute(select_query, (session['email'],))
    cart_products = cursor.fetchall()

    # Calculate the total price of the cart
    total_query = """
    SELECT SUM(P.Price)
    FROM cartproduct CP
    JOIN product P ON CP.ProductId = P.Id
    JOIN cart C ON CP.CartId = C.Id
    JOIN user U ON C.UserId = U.Id
    WHERE U.Email = %s
    """
    cursor.execute(total_query, (session['email'],))
    total_price = cursor.fetchone()[0]
    
    if total_final_price is None:
        total_final_price = total_price
    
    print("------------------> TOTAL FINAL PRICE CHECKOUT: ",total_final_price)

    # Retrieve shipping info from database
    select_shipping_query = """
    SELECT * FROM shipping
    INNER JOIN user ON shipping.UserId = user.Id
    WHERE user.Email = %s
    """
    cursor.execute(select_shipping_query, (session['email'],))
    shipping_info = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # Render the template and pass the cart data to it
    return render_template('checkout.html',
                           cart_products=cart_products,
                            total_price=total_price,
                           total_final_price=total_final_price,
                           discount_amount=discount_amount,
                           shipping_info=shipping_info)


@app.route('/place_order', methods=['POST'])
def place_order():
    # Check if the user is authenticated
    if 'email' not in session:
        return redirect(url_for('signin'))
    
    total_final_price = session.get("discounted_total")

    # Retrieve the user's ID
    cnx = pymysql.connect(**db_config)
    cursor = cnx.cursor()

    # Retrieve the UserId based on the user's email in the session
    select_user_id_query = "SELECT Id FROM user WHERE Email = %s"
    cursor.execute(select_user_id_query, (session['email'],))
    user_id = cursor.fetchone()[0]

    # Retrieve the user's cart ID
    select_cart_query = "SELECT Id FROM cart WHERE UserId = %s"
    cursor.execute(select_cart_query, (user_id,))
    cart_id = cursor.fetchone()[0]

    # Calculate the total price of the order
    total_query = """
    SELECT SUM(P.Price)
    FROM cartproduct CP
    JOIN product P ON CP.ProductId = P.Id
    JOIN cart C ON CP.CartId = C.Id
    JOIN user U ON C.UserId = U.Id
    WHERE U.Id = %s
    """
    cursor.execute(total_query, (user_id,))
    total_price = cursor.fetchone()[0]
    
    if total_final_price is None:
        total_final_price = total_price

    # Insert the order into the database
    insert_order_query = "INSERT INTO `order` (UserId, Status, Total) VALUES (%s, %s, %s)"
    cursor.execute(insert_order_query, (user_id, 'processing', total_final_price))
    cnx.commit()
    order_id = cursor.lastrowid

    # Retrieve the products from the user's cart
    select_cart_products_query = "SELECT ProductId FROM cartproduct WHERE CartId = %s"
    cursor.execute(select_cart_products_query, (cart_id,))
    cart_products = cursor.fetchall()

    insert_order_product_query = "INSERT INTO orderproduct (OrderId, ProductId) VALUES (%s, %s)"
    order_product_data = [(order_id, product_id) for product_id, in cart_products]
    cursor.executemany(insert_order_product_query, order_product_data)
    cnx.commit()

    delete_cart_products_query = "DELETE FROM cartproduct WHERE CartId = %s"
    cursor.execute(delete_cart_products_query, (cart_id,))

    cnx.commit()

    cursor.close()
    cnx.close()

    return redirect(url_for('order_confirmation', order_id=order_id))


@app.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):

    total_final_price = session.get("discounted_total")
    
    if 'email' not in session:
        return redirect(url_for('signin'))

    cnx = pymysql.connect(**db_config)
    cursor = cnx.cursor()


    select_order_query = """
    SELECT O.Id, P.Name, P.Description, P.Price, P.Image, P.Category
    FROM `order` O
    JOIN orderproduct OP ON O.Id = OP.OrderId
    JOIN product P ON OP.ProductId = P.Id
    JOIN user U ON O.UserId = U.Id
    WHERE U.Email = %s AND O.Id = %s
    """
    cursor.execute(select_order_query, (session['email'], order_id))
    order_products = cursor.fetchall()

    total_query = """
    SELECT SUM(P.Price)
    FROM `order` O
    JOIN orderproduct OP ON O.Id = OP.OrderId
    JOIN product P ON OP.ProductId = P.Id
    JOIN user U ON O.UserId = U.Id
    WHERE U.Email = %s AND O.Id = %s
    """
    cursor.execute(total_query, (session['email'], order_id))
    total_price = cursor.fetchone()[0]
    
    if total_final_price is None:
        total_final_price = total_price
    
    print("------------------> TOTAL PRICE : ",total_price)
    print("------------------> TOTAL FINAL PRICE : ",total_final_price)


    select_shipping_query = """
    SELECT * FROM shipping
    INNER JOIN user ON shipping.UserId = user.Id
    WHERE user.Email = %s
    """
    cursor.execute(select_shipping_query, (session['email'],))
    shipping_info = cursor.fetchall()
    cursor.close()
    cnx.close()
    cart_count = get_cart_count()
    email_id=session['email']

    #API_URL = "http://127.0.0.1:5052/email"
    API_URL = "https://6k14b06og7.execute-api.us-east-1.amazonaws.com/default/email-api-x23289678"
    try:
        subject='Order place for GreenKart '
        message=f"Your Order has been sucessfully placed for Rs {total_price}. Your order id is {order_id}. Thankyou for shopping!"
        data=f'{subject} : {message} : {email_id}'
        
        json_data = {"text": data }
        response = requests.get(API_URL, json=json_data, stream=True)
        if response.status_code == 200:
            
            print("Mail delivered Successfully ")
        else:
            print(response)
            print("Failed to email")
    except Exception as e:
        converted_amt = f"An error occurred: {str(e)}"

    return render_template('order_confirmation.html',
                           order_id=order_id,
                           order_products=order_products,
                           total_price=total_price,
                           total_final_price=total_final_price,
                           shipping_info=shipping_info,
                           cart_count=cart_count)


@app.route('/shipping', methods=['GET', 'POST'])
def shipping():
    if 'email' not in session:
        return redirect(url_for('signin'))

    if request.method == 'POST':
        if 'delete_shipping' in request.form:
            shipping_id = request.form.get('delete_shipping')
            cnx = pymysql.connect(**db_config)
            cursor = cnx.cursor()
            delete_shipping_query = "DELETE FROM shipping WHERE Id = %s"
            cursor.execute(delete_shipping_query, (shipping_id,))
            cnx.commit()
            cursor.close()
            cnx.close()
            return redirect(url_for('shipping'))

        else:
            full_name = request.form.get('full_name')
            street_address = request.form.get('street_address')
            city = request.form.get('city')
            state_province = request.form.get('state_province')
            postal_code = request.form.get('postal_code')
            country = request.form.get('country')
            cnx = pymysql.connect(**db_config)
            cursor = cnx.cursor()
            select_user_query = "SELECT Id FROM user WHERE Email = %s"
            cursor.execute(select_user_query, (session['email'],))
            user_id = cursor.fetchone()[0]
            insert_shipping_query = """
            INSERT INTO shipping (UserId, Full_Name, Street_Address, City, State_Province, Postal_Code, Country)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            shipping_data = (user_id, full_name, street_address, city, state_province, postal_code, country)
            cursor.execute(insert_shipping_query, shipping_data)
            cnx.commit()

            select_shipping_query = """
            SELECT * FROM shipping
            INNER JOIN user ON shipping.UserId = user.Id
            WHERE user.Email = %s
            """
            cursor.execute(select_shipping_query, (session['email'],))
            shipping_info = cursor.fetchall()
            cursor.close()
            cnx.close()
            
            return render_template('shipping.html', shipping_info=shipping_info)

    
    cnx = pymysql.connect(**db_config)
    cursor = cnx.cursor()
    
    select_shipping_query = """
    SELECT * FROM shipping
    INNER JOIN user ON shipping.UserId = user.Id
    WHERE user.Email = %s
    """
    cursor.execute(select_shipping_query, (session['email'],))
    shipping_info = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    return render_template('shipping.html', shipping_info=shipping_info)

@app.context_processor
def inject_cart_count():

    if 'email' not in session:
        return dict(cart_count=0)

    cnx = pymysql.connect(**db_config)
    cursor = cnx.cursor()

    query = """
    SELECT COUNT(*)
    FROM cartproduct CP
    JOIN cart C ON CP.CartId = C.Id
    JOIN user U ON C.UserId = U.Id
    WHERE U.Email = %s
    """

    cursor.execute(query, (session['email'],))
    result = cursor.fetchone()
    cart_count = result[0] if result else 0

    cursor.close()
    cnx.close()

    return dict(cart_count=cart_count)

@app.route('/videos')
def videos():
    # Configure your YouTube API key and channel ID
    api_key = os.environ.get('YT_API_KEY')

    # Define the search query for cooking videos
    search_query = 'African meals'

    # Make a request to the YouTube API
    url = f'https://www.googleapis.com/youtube/v3/search?key={api_key}&part=snippet&type=video&q={search_query}'
    response = requests.get(url)
    data = response.json()

    # Extract the video information from the API response
    videos = []
    for item in data['items']:
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        video_thumbnail = item['snippet']['thumbnails']['medium']['url']
        videos.append({'id': video_id, 'title': video_title, 'thumbnail': video_thumbnail})

    # Limit the number of videos to a maximum of 10
    videos = videos[:10]

    cart_count = get_cart_count()
    
    # Render the template and pass the videos to it
    return render_template('videos.html', videos=videos, cart_count=cart_count)


# Route for the admin panel
@app.route('/admin', methods=['GET'])
def admin_panel():
    if 'email' in session and session['email'] == 'admin@frb.com':
        return render_template('admin_panel.html')
    else:
        return redirect(url_for('signin'))

import io
import base64
import requests
from flask import send_file, jsonify, request

@app.route('/convert', methods=['POST'])
def convert_to_json():
    try:
        print("---- /convert endpoint called ----")

        data = request.json
        invoice_data = data.get("invoice") if data else None

        if not invoice_data:
            return jsonify({"error": "No invoice data provided"}), 400

        json_data = {"table": invoice_data}

        pdf_response = requests.post(
            "https://nda1hat3je.execute-api.us-east-1.amazonaws.com/default/lambda-export-pdf",
            json=json_data
        )

        print("Lambda status:", pdf_response.status_code)
        print("Lambda first bytes:", pdf_response.content[:50])

        if pdf_response.status_code != 200:
            return jsonify({
                "error": "Export API failed",
                "details": pdf_response.text
            }), 500

        # Decode base64 PDF
        decoded_pdf = base64.b64decode(pdf_response.content)

        print("Decoded PDF first bytes:", decoded_pdf[:10])

        pdf_bytes = io.BytesIO(decoded_pdf)

        return send_file(
            pdf_bytes,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="invoice.pdf"
        )

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
