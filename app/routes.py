from app import app, db, Mail, Message
from flask import render_template, request, flash, redirect, url_for
from app.forms import UserInfoForm, LoginForm, CreateAPlan
from app.models import User, Plans, Cart
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash


ddb = """Dale's Dead Bugs | """


@app.route('/')
@app.route('/index')
# <<<<<<< master
# def ddb_Home():
#         title = "Dale's Dead Bug",
        
# =======
def index():
    title = ddb + """HOME"""
    return render_template('index.html', title=title)

# @app.route('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = ddb + "register"
    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        phone = form.phone.data
        address = form.address.data
        city = form.city.data
        zipcode = form.zipcode.data
        # admin = form.admin.data
        # print(username, email, password)

        # create new instance of User
        new_user = User(username, email, password,
                        phone, address, city, zipcode)
        # add new instance to our database
        db.session.add(new_user)
        # commit database
        db.session.commit()

        # send email to new user
        msg = Message(f"Welcome, {username}", [email])
        # msg.body = 'Thank you for signing up for the most glorious death of your bugs. I hope you enjoy your new carnage!'
        msg.html = "<p>Thanks you so much for signing up for the Dale's Dead Bugs service. Where we do buggin right! We may, or may not, be in Liberia!</p>"

        # Mail.send(msg)  error occurs saying that send needs a postional argument dont know why

        flash("It may be a crack in your internet, or the Chinese are making their move!", "success")
        return redirect(url_for('index'))
    return render_template('register.html', title=title, form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have succesfully logged out", 'primary')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = ddb + 'login'

    form = LoginForm()

    if request.method == 'POST' and form.validate():

        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            flash("Incorrect Username or Password. Please try again")
            return redirect(url_for('index'))

        login_user(user, remember=form.remember_me.data)
        flash(f"Welcome back {username}!")
        next_page = request.args.get('next')
        if next_page:
            return redirect(url_for(next_page.lstrip('/')))

        return redirect(url_for('index'))

    return render_template('login.html', title=title, form=form)


@app.route('/myinfo')
@login_required
def myinfo():
    title = ddb + 'My Info'
    return render_template('myinfo.html', title=title)


@app.route('/availableplans', methods=["GET", "POST"])
@login_required
def availableplans():
    
    title = ddb + 'Services'

    form = CreateAPlan()
    if request.method == 'POST' and form.validate():
    
        service_name = form.service_name.data
        service_date = form.service_date.data
        price = form.price.data
        description = form.description.data
        url = form.url.data
        sale = form.sale.data
        
        new_plan = Plans(service_name, service_date, price, description, url, sale=False)
        
        db.session.add(new_plan)
        db.session.commit()
        flash ("Great Job! You Added a NEW Service :)")
        return redirect(url_for('availableplans'))

    return render_template('available_plans.html', title=title)


@app.route('/mycart')
@login_required
def mycart():
    context = {
        'title': "DDB | My Cart",
        'total_price': 0,
        'cart': Cart.query.all()
    }

    print('BREAK!!!!')
    print(current_user.id)
    print('BREAK!!!!')
    # print(cart)
    print('break!!!!')
    for objects in context['cart']:

        print(objects.service_id)
        print(objects.user_id)

# =======
#     for objects in context['cart']:
# >>>>>>> master
        if current_user.id == objects.user_id:
            context['total_price'] += objects.plan.price
    return render_template('shoppingcart.html', **context)

@app.route('/removecartplan/delete/<int:cart_id>', methods=["POST"])
@login_required
def removecartplan(cart_id):
    cart = Cart.query.get_or_404(cart_id)
    db.session.delete(cart)
    db.session.commit()
    return redirect(url_for('mycart'))

@app.route('/addcartplan/add/<int:plan_id>', methods=["POST"])
@login_required
def addcartplan(plan_id):
    # plan = Plans.query.get_or_404(plan_id)
    item = Cart(plan_id, current_user.id)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('mycart'))


# @app.route('/addplan')
# def addplan():
#     if request.method = 'POST':
#         #add items to cart
#         return redirect(url_for('shoppingcart'))

@app.route('/myinfo/update/<int:user_id>', methods=['GET', 'POST'])


@login_required
def myInfoUpdate(user_id):
    title = ddb + "Update My Info"
    myinfo = User.query.get_or_404(user_id)
    update_info = UserInfoForm()

    if myinfo.id != current_user.id:
        flash("You cannot update another users info")
        return redirect(url_for('myinfo'))

    if request.method == 'POST' and update_form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        phone = form.phone.data
        address = form.address.data
        city = form.city.data
        zipcode = form.zipcode.data

        myinfo.username = username
        myinfo.email = email
        myinfo.password = password
        myinfo.phone = phone
        myinfo.address = address
        myinfo.city = city
        myinfo.zipcode = zipcode

        db.session.commit()

        flash("You have successfully updated your info")
        return redirect(url_for('myinfo', user_id=user.id))
    return render_template('myInfoUpdate.html', title=title, form=update_info)


# @app.route('/shoppingCart', methods=["GET", "POST"])
# @login_required
# def shoppingCart():
#     title = ddb + 'My Cart'
#     return render_template('shoppingCart.html',title=title)
