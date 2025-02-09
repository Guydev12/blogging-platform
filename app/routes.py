from flask import Blueprint, request, render_template, flash, redirect, url_for
from app.models import User, Article, Profile,Tag
from app import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, logout_user, login_user

# Create a group of routes
main_routes = Blueprint('main', __name__)
# Load the user 
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))
# Define the main route (index)
@main_routes.route('/')
def index():
    data = Article.query.order_by(Article.created_at.desc()).all()
    print("Current User",current_user)
    return render_template("index.html", data = data)
    
# Create the user handpoints
@main_routes.route('/login',methods=["GET","POST"])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  # If the user is not authenticated let log the user in
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    if not username:
      flash("Username is required", "danger")
      return redirect(url_for('main.login'))
    if  len(password) < 8:
      flash("password is required")
      return redirect(url_for('main.login'))
    # Check if the user exist
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.hash, password):
      flash("Invalid credential", "danger")
      return redirect(url_for('main.login'))
      # Register the user in the session
    login_user(user)
    return redirect(url_for('main.index'))
  return render_template('auth.html')
  
  
@main_routes.route("/register", methods=["GET", "POST"])
def create_user():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  if request.method == "POST": 
    # Get the username and their email
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    # check if there is a username and email
    if not username:
      flash("The username field is empty ,Please provide an username!","danger")
      return redirect(url_for("main.create_user"))
      
    elif not email:
       flash("The email field is empty","danger")
       return redirect(url_for("main.create_user"))
       
    elif len(password) < 8:
      flash('Password is too short','danger')
    # Check if the user exist 
    user_exist = User.query.filter_by(username = username).first()
    if user_exist:
      flash("User Already exist","danger")
      return redirect(url_for('main.create_user'))
    # Hash the password
    hash = generate_password_hash(password)
    # Create the user
    try:
      new_user = User(username=username,email=email, hash = hash)
      db.session.add(new_user)
      db.session.commit()
      flash("User created successfully!","success")
      return redirect(url_for('main.login'))
    except error:
      print("create user 500", error)
      return render_template("500.html")
  return render_template("user.html")
    
        
# Create Article
@main_routes.route('/article', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        username = request.form.get('username')

        if not title:
            flash('Title is required', 'danger')
            # Log the error
            print("no Title")
            return redirect(url_for("main.create_article"))

        if not content:
            flash('Content is required', 'danger')
            print('no Content')
            return redirect(url_for("main.create_article"))
        # Get the tags
        tags = request.form.get("tags").strip()
        if not tags:
          flash("Please enter a tag","danger")
          return redirect(url_for('main.create_article'))
        
        list_of_tags = tags.split(' ')

        # Create the article
        article = Article(title=title, content=content, author_id=current_user.id)
        # Add the tag in article
        for tag_name in list_of_tags:
          tag_name = tag_name.strip()
          tag = Tag.query.filter_by(name=tag_name).first()

          if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
          article.tags.append(tag)

        # Add the created article to the database
        db.session.add(article)
        # Save it 
        db.session.commit()
        flash('New article created!', 'success')
        return redirect(url_for("main.index"))
        
    return render_template('create-article.html')
    
# View article details

@main_routes.route('/article/<article_id>', methods= ["GET","POST"])
def article_details(article_id):
  if not article_id:
    flash("No Id found", "danger")
    return redirect(url_for('main.article_details'))
  # Get this particular Article by its Id
  article = Article.query.filter_by(id= int(article_id)).first()
  if not article:
    flash('No article found','dangee')
    return redirect(url_for('main.article-details'))
  if request.method == "POST":
    db.session.delete(article)
    db.session.commit()
    flash('Article with id {} was removed'.format(article.id),'success')
    return redirect('/')
  return render_template('article-details.html', article=article)
# Edit article 
@main_routes.route('/article/<article_id>/edit',methods=["GET","POST"])
def edit_article(article_id):
  article = Article.query.get(int(article_id))
  if not article:
    flash('no article found','danger')
    return redirect(url_for('main.edit_article'))

  if request.method == "POST":
    title = request.form.get("title")
    if not title:
      flash("title is required",'danger')
      return redirect(url_for('main.edit_article'))

    content = request.form.get('content')
    if not content:
      flash("content is required",'danger')
      return redirect(url_for('main.edit_article'))

    # Get the tags
    tags = request.form.get("tags").strip()
    if not tags:
      flash("Please enter at least one tag","danger")
      return redirect(url_for('main.edit_article',article_id=article_id))
    
    list_of_tags = [tag.strip() for tag in tags.split() if tag.strip()]  # Clean and remove empty tags
    current_tags = set([tag.name for tag in article.tags])  # Get existing tags of the article

    # Remove tags that were removed in the form
    for tag in article.tags[:]:
      if tag.name not in list_of_tags:
        article.tags.remove(tag)
        db.session.delete(tag)  # Delete the tag from the database if it's no longer associated with the article

   
    # Add or update tags
    for tag_name in list_of_tags:
      if tag_name not in current_tags:
        # Check if the tag exists in the database, if not, create a new one
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:  # If no existing tag is found
          tag = Tag(name=tag_name)  # Create new tag
          db.session.add(tag)  # Add new tag to the session
        article.tags.append(tag)  # Append the tag to the article
        current_tags.add(tag_name)

    # Update the article details
    article.title = title
    article.content = content
    db.session.add(article)
    db.session.commit()

    flash('Changes have been saved','success')
    return redirect(f'/article/{article_id}')

  return render_template('article-form-update.html', article= article)
# route to clear the session
@main_routes.route('/logout')
@login_required
def logout():
  # Log the user out
  logout_user()
  return redirect(url_for('main.login'))