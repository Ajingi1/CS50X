import os

import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd, get_time

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get user id
    user_id = session["user_id"]

    try:
        # Get  portfolios data and balance left from database
        portfolios = db.execute(
            "SELECT symbol, no_of_shares AS total_shares FROM portfolio WHERE user_id = ?",
            user_id,
        )
        balance_left = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

        # Convert balance_left to float if it exists
        balance_left = (
            float(balance_left[0]["cash"])
            if balance_left and "cash" in balance_left[0]
            else 0.0
        )

        # variables for total amount and template rendering
        total_amount = balance_left
        portfolio_data = []

        # format balance
        balance_left = f"{balance_left: .2f}"

        # Loop through portfolios to calculate total value
        for portfolio in portfolios:
            symbol = portfolio["symbol"]
            total_shares = portfolio["total_shares"]

            # Get current price from lookup function
            lookup_data = lookup(symbol)
            current_price = float(lookup_data["price"])
            # print(f"Symbol: {symbol}, Current Price: {current_price}")

            # Calculate total value for this symbol
            total_value = total_shares * current_price

            # Add total value to total amount
            total_amount += total_value
            portfolio_data.append(
                {
                    "symbol": symbol,
                    "total_shares": total_shares,
                    "current_price": f"{current_price: .2f}",
                    "total_value": f"{total_value: .2f}",
                }
            )

    except ValueError:
        return apology("Failed to show portfolio")

    # Render template with data
    return render_template(
        "index.html",
        portfolios=portfolio_data,
        total_amount=total_amount,
        balance=balance_left,
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Get the values from user
        share_symbol = request.form.get("symbol")
        share_number = request.form.get("shares")

        # look up symbol from API
        stock = lookup(share_symbol)

        share_symbol = share_symbol.upper()

        # check field empty or invalid symbol
        if not share_symbol or not stock:
            return apology("Invalid share symbol")
        # check if user enter anything otherthan positive interger
        elif not share_number.isdigit():
            return apology("invalid share number")

        # Get user id
        user_id = session["user_id"]
        # Get users current Balance
        user_current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_current_cash = user_current_cash[0]["cash"]
        # calculate how many share we want buy
        transaction_value = int(share_number) * stock["price"]

        if user_current_cash < transaction_value:
            return apology("Insufficient Balance")

        # Purchase the stock share
        update_user_cash = user_current_cash - transaction_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_user_cash, user_id)

        update_user_cash = f"{update_user_cash:,.2f}"

        #  add data to portfolio
        # Check if the user already holds the stock
        existing_stock = db.execute(
            "SELECT * FROM portfolio WHERE user_id = ? AND symbol = ?",
            user_id,
            share_symbol,
        )

        if existing_stock:
            # Update the existing stock
            current_shares = existing_stock[0]["no_of_shares"]

            share_number = int(share_number)
            new_shares = current_shares + share_number

            db.execute(
                "UPDATE portfolio SET no_of_shares = ? WHERE user_id = ? AND symbol = ?",
                new_shares,
                user_id,
                share_symbol,
            )
        else:
            db.execute(
                "INSERT INTO portfolio(user_id, symbol, no_of_shares) VALUES (?, ?, ?)",
                user_id,
                share_symbol,
                share_number,
            )
        # Add history to database
        db.execute(
            "INSERT INTO history (user_id, item_symbol, price, share_number, action,  balance, purchase_date) VALUES(?, ?, ?, ?, ?, ?, ?)",
            user_id,
            share_symbol,
            transaction_value,
            share_number,
            "BOUGHT",
            update_user_cash,
            get_time(),
        )
        flash(f"Successfully bought {share_number} shares of {share_symbol}!")
        return redirect("/")
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Get user id
    user_id = session["user_id"]
    # Get user data from database
    rows = db.execute("SELECT * FROM history WHERE user_id = ?", user_id)
    # render the page
    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbols = request.form.get("symbol")

        # if field is empty
        if not symbols:
            return apology("Invalid Symbol")

        # check if morethan one symbol split it then request from API
        symbols = [
            symbol.strip() for symbol in re.split(r"[,\s]+", symbols) if symbol.strip()
        ]

        # empty stocks list
        stocks = []

        # loop in to my list of symbols
        for symbol in symbols:
            # make sure the value is string
            symbol = str(symbol)
            stock = lookup(symbol)

            # check if sctock is none
            if stock is None:
                return apology("Invalid Symbol")

            # add usd symbol
            stock["price"] = usd(stock["price"])

            # append stock in to stocks list
            stocks.append(stock)

        return render_template("quoted.html", stocks=stocks)

    return render_template("quote.html")
    # return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        """Register user"""
        # Get data from form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Get exiting usernames from database
        usersname = db.execute("SELECT username FROM users")

        # check if the data from form is blank
        if not username or not password or not confirmation:
            return apology("must provide username, password and confirmation ")

        for item in usersname:
            if item["username"] == username:
                return apology("This username already exit")

        # UserName length must be morethan 4 characters
        if len(username) < 5:
            return apology("Your Username must not be lesthan 5 characters")

        # # checking username if is alpa numeric
        # if not username.isalnum():
        #     return apology("You username can only contain aplabet and numbers", 403)

        # checking password length
        if len(password) < 8:
            return apology("Your password length must be morethan 7")

        # Check password similarity
        if password != confirmation:
            return apology("password and confirmation doen't match")

        # hash the password
        hash_password = generate_password_hash(password)
        # insert the username and hashed password in to the database
        db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)", username, hash_password
        )

        # return log in page
        flash(f"Successfully registered!")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Get user id
        user_id = session["user_id"]

        # Get the values from user
        share_symbol = request.form.get("symbol")
        share_number = int(request.form.get("shares"))

        # Lookup symbol from API
        stock = lookup(share_symbol)

        # Check if fields are empty or symbol is invalid
        if not share_symbol or not stock:
            return apology("Invalid share symbol")

        # Check if share_number is a positive integer
        if share_number <= 0:
            return apology("Invalid share number")

        # Get user's current cash balance
        user_current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        if not user_current_cash:
            return apology("User not found")

        user_current_cash = user_current_cash[0]["cash"]

        # Calculate transaction value
        transaction_value = share_number * stock["price"]

        # Get user's portfolio for the specific symbol
        portfolio = db.execute(
            "SELECT no_of_shares FROM portfolio WHERE user_id = ? AND symbol = ?",
            user_id,
            share_symbol,
        )
        if not portfolio or portfolio[0]["no_of_shares"] < share_number:
            return apology("You don't own this amount of shares")

        # Update user's cash balance and portfolio
        new_cash_balance = int(user_current_cash) + transaction_value
        new_shares = portfolio[0]["no_of_shares"] - share_number

        # Update users table and portfolio table without explicit transaction
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash_balance, user_id)
        db.execute(
            "UPDATE portfolio SET no_of_shares = ? WHERE user_id = ? AND symbol = ?",
            new_shares,
            user_id,
            share_symbol,
        )

        # Add sale history to database
        db.execute(
            "INSERT INTO history (user_id, item_symbol, price, share_number, action, balance, purchase_date) VALUES(?, ?, ?, ?, ?, ?, ?)",
            user_id,
            share_symbol,
            transaction_value,
            share_number,
            "SOLD",
            new_cash_balance,
            get_time(),
        )

        flash(f"Successfully SOLD {share_number} shares of {share_symbol}!")
        return redirect("/")

    else:
        user_id = session["user_id"]
        stocks = db.execute("SELECT symbol FROM portfolio WHERE user_id = ?", user_id)
        return render_template("sell.html", stocks=stocks)
