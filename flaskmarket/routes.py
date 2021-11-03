from flask  import render_template,redirect,url_for, flash , request
from flaskmarket import app
from flaskmarket import db
from flaskmarket.models import Item, User
from flaskmarket.forms import  RegistrationForm, LoginForm, PurchaseForm, SellForm
from flask_login import login_user, logout_user,login_required, current_user


@app.route("/")
@app.route("/home")
def home():

    return render_template('home.html')

@app.route("/market", methods=['GET','POST'])
@login_required 
def market():
    purchase_form = PurchaseForm()
    sell_form = SellForm()
    #Purchase item logic
    if request.method == "POST":
        purchase_item = request.form.get('purchase_item')
        p_item_object = Item.query.filter_by(name=purchase_item).first()

        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations you buy {p_item_object.name} for {p_item_object.price}$" , category = 'info')
            
            else:
                flash( f"Sorry! you don't have enough budget for {p_item_object.name }", category = "danger")

            return redirect( url_for('market')) 
    #Sell item logic
    sold_item = request.form.get('sold_item')
    s_item_object = Item.query.filter_by(name=sold_item).first()
    if s_item_object:
        if current_user.can_sell(s_item_object):
            s_item_object.sell(current_user)
            flash(f"Congratulations you sell {s_item_object.name} for {s_item_object.price}$ back to the market" , category = 'info')

        else:
            flash(f"Something went wrong for selling { s_item_object.name}", categroy = 'danger')   

        return redirect(url_for('market'))      
    if request.method == "GET":   
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner = current_user.id)
        return render_template('market.html',items = items, purchase_form=purchase_form, owned_items = owned_items, sell_form = sell_form)


@app.route('/registration', methods=['GET','POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        creating_user = User(username=form.username.data,
        email_address = form.email_address.data,
        password = form.password1.data)
        db.session.add(creating_user)
        db.session.commit()
        login_user(creating_user)
        flash(f"Sucess! You are  logged in as: {creating_user.username}", category = 'info')
        return redirect(url_for('market'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There are was an error :{err_msg}', category="danger" )

    return render_template('registration.html', form = form)


@app.route('/login', methods = ['GET','POST'] )
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()
        if (attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data)):
            login_user(attempted_user)
            flash(f"Sucess! You are  logged in as: {attempted_user.username}", category = 'info')
            return redirect(url_for('market'))
        else:
            flash('Username and password are not match! Please try again', category = 'danger')

    return render_template('login.html', form = form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You are logged out", category = 'info')
    return redirect(url_for('home'))

