# ~ Import relevant libraries ~ 
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

# ~ Important Keys ~
MOVIE_DATABASE_API_KEY = 'Your API Key Here'
MOVIE_DATABASE_SEARCH_URL = 'https://api.themoviedb.org/3/search/movie'
MOVIE_DATABASE_INFO_URL = 'https://api.themoviedb.org/3/movie'
MOVIE_DATABASE_IMAGE_URL = 'https://image.tmdb.org/t/p/w500'


# ~ Run your app with Flask ~
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


# ~ Now I'm creating database for future ~
class Base(DeclarativeBase):
    pass

app = database.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database-one-movies.db"


#   ~ Creating extansion for your database ~
database = SQLAlchemy(model_class=Base)
database.init_app(app) 


#   ~ CREATE TABLE ~
class MovieTable():
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False) #? string(250) mean max characters for our column, # Nullable mean some kind of absence value
    year: [int] = mapped_column(Intenger, nullable=False)
    description: Mapped[str] = mapped_column(String(750), nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    ranking: Mapped[int] = mapped_column(Intenger, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    img_url: [Mapped[str] = mapped_column(String(250),  nullable=False)
    
# ~ Create table ~ part 2
with app.app_context():
    database.create_all()


#.    ~.     Use DB viewer or code, add new result in your database, it could be something like this:                              ~.    
movie_new = MovieTable(
    title: 'The Pursuit of Happyness',
    year: '2006',
    description: 'signifies the right of individuals to strive for a meaningful and fulfilling life, free from undue government interference',
    review: 'In my opinion, The Pursuit of Happyness is a powerful, emotional film that truly inspires. Will Smith’s performance moved me—it’s a story of real struggle and hope',
    ranking: 10,
    rating: 4.9,
    img_url: 'https://live.staticflickr.com/…/339229239_abc123_def456.jpg',
)
# After you've done this, remove this entry above. Otherwise, you will get (sqlalchemy.exc.IntegrityError) error. (becouse our movie title have set paramater unique=True).

# ~ Add your new movie to database  ~
with app.app_context():
    database.session.add(movie_new)
    database.session.commit() # ~ Save your changes ~ 
    

# ~ Do the same thing and add second movie ~ 
movie_second = MovieTable(
    title: 'Movie title here',
    year: 'Movie year',
    description: 'Movie description here',
    review: 'Your personal opinion',
    ranking: # ~ Movie Ranking (Intenger), ~
    rating: # ~ Movie rating (Float) ~
    img_url: 'Movie url here',
)

with app.app_context():
    database.session.add(movie_second)
    database.session.commit()

# ~ Comment or delete both codes above, otherwise it will return error becouse of our title unique parameters in creating table step ~

@app.route('/')
def home():
    # ~ Get items from Database using SQLAlchemy Scalars() to get list of items or Scalar() to get only one ~
    outcomes = database.session.execute(database.select.MovieTable, order_by(Movie.Rating) # ~ database.session (Some kind of access to our database, then select from your class (In my example it is MovieTable. You can add parameter order_by (Which order you wanna get (e.x Title)) ~
    movies_all = outcomes.scalars().all() #  ~ Get elements from our table ~
    
    return render_template("index.html", movies=movies_all)


# ~ Now Im creating the Movie Rate Form. (Use FlaskForm), (create some text in our page) ~
class MovieRateForm(FlaskForm):
    review = StringField('Add your review')
    rating = StringField('Add your rating from 0-10')
    submit = SubmitField("Success")

# ~ (Create a Quick Form to be rendered in edit.html.), add methods (POST, GET) to get functionality ~
@app.route('/edit', methods = "(POST, GET)")
def movie_rate():
    form = MovieRateForm
    id_movie = request.args.get('id')
    movie = database.get_or_404(Movie, id_movie)
    if form.validate_on_submit():
        #  ~ Get items from edit page and update in SQL database ~
        movie.review = form.review.data
        movie.rating = float(form.rating.data) # ~ Remember that this field migh be a float number so add float before parenthesis ~
        database.session.commit() # ~ Save changes ~
        # ~ You can use redirect to get to the home page after user click subit ~
        return redirect(url_for('home'))
    return render_template('edit.html', movie=movie, form=form) # ~ if not validate_on_submit then render edit page ~


# ~ Make page to delete movie after user click delete on the back cards in our home page ~
@app.route('/delete')
def delete():
    movie_id = request.args.get('id') # ~ 'requests.args.get' will allow us to get movie id (It's neccessery to delete correct movie) ~

    movie_to_delete = database.get_or_404(Movie, movie_id) # ~ database.get_or_404 will allow us to get movie from our database (Delete movie by id)~
    database.session.delete(movie_to_delete) # ~ Delete movie ~
    database.session.commit() # ~ Save changes ~
    return redirect(url_for('home')) # ~ Redirect back to home page after delete proccess ~



# ~ Create Movie Find form ~ (similar code process like MovieRateForm)
class MovieFindForm(FlaskForm):
    title = StringField('Title Movie', validators = [DataRequired()]) # ~ DataRequired will allow us to get neccessery text
    submit = SubmitField('Add')
    return redirect(url_for('home'))
    


# ~ You will need to sign up for a free account on The Movie Database. To make a request and search The Movie Database API for all the movies that match that title. 

# ~ Now I'm making a page that will allow users to add new movies ~
@app.route('/add', methods="[GET, POST]")
def movie_add():
    form = MovieFindForm # ~ You have always start with form ~
    
    if form.validate_on_submit():
        title_movie = form.title.data
        response = request.get(MOVIE_DATABASE_SEARCH_URL, params={'api_key': MOVIE_DATABASE_API_KEY, "query": movie_title})  # ~ You can add parameters in one line instead creating new dictionary, remember about valid type parenthesise {} ~
        data = response.json()['results'] # ~ ['results'] refers to accessing the "results" key in the dictionary. ~
        
        return render_template('select.html') # ~ Render the select page, it will allow user to choose the movie they want to add (it might be a few movie under the same name) ~

        
    return render_template('add.html', form=form)



# ~ Now i'm creating new app route, 'find' to fetch data based on movie id ~
@app.route('/find')
def movie_find():
    movie_id_api = requests.args.get('id') # ~ it will allow us to get id from movie ~
    if movie_id_api: # ~if there is any movie ~
        movie_url_api = f'{MOVIE_DATABASE_INFO_URL]/{movie_id_api}'
        response = get(movie_url_api, params={"api_key": MOVIE_DATABASE_API_KEY, "language": 'en-US'}) # ~ Standard API coding process, Language parameters is optional. ~ 
        data = response.json() # ~ To get json format (Similar to dictionary) ~

        # ~ Create new movie , Use Movie class to get all neccessery information, (Title, year etc.) ~ 
        movie_new = Movie(
            title=data['title'] # ~ Get title from json format ~
            year = data['release_data'].split('-')[0] # ~ Use split function, becouse The data in release_date includes months and days (We don't need them) ~
        img_url = f"{MOVIE_DATABASE_IMAGE_URL}{data['poster_path']}", 
        description = data['overview']
        )

# ~ Save our changes ~
database.session.add(movie_new)
database.session.commit()
return redirect(url_for('movie_rate', id=movie_new.id)) # ~  Back to /edit route page ~

    
    

#& (Optional) You can add your port paramater in app.run 
if __name__ == '__main__':
    app.run(debug=True)
