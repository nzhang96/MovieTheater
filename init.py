from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("main.html")


#main page for staff
@app.route('/staff')
def staff():
    return render_template("staff.html")


#=========== Movie Functions: =============#
#-------------------------------------------

@app.route('/movies')
def movies():
    return render_template("movies.html")


# Add a movie to the database
@app.route("/add_movie", methods=["POST"])
def add_movie():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query1 = ("ALTER TABLE Movie ADD COLUMN Poster VARCHAR(2083)")
    cursor.execute(query1)
    
    
    query = (
            "INSERT INTO Movie (MovieName, MovieYear, Poster)"
            "VALUES(%s, %s, %s)"
            )
    to_add =(
            request.form['movie_name'], 
            request.form['movie_year'],
            request.form['Poster']
            )

    
    cursor.execute(query, to_add)


    cnx.commit()
    cnx.close()
    return render_template (
                            'add_movie.html',  
                            MovieName=request.form['movie_name'], 
                            MovieYear=request.form['movie_year'],
                            Poster=request.form['Poster']
                            )
#-------------------------------------------

#-------------------------------------------
@app.route("/movie_to_add")
def movie_to_add():
    return render_template('add_movie_form.html')
#-------------------------------------------

#-------------------------------------------
# Delete a movie from the database
@app.route("/delete_movie", methods=["POST"])
def delete_movie():

    try:
        cnx = mysql.connector.connect(user='root', database='MovieTheatre')
        cursor = cnx.cursor()
        
        query = ("DELETE FROM Movie WHERE MovieName=%s")
        
        to_delete = (request.form['movie_name'],)

        cursor.execute(query, to_delete)
        cnx.commit()
        cnx.close()

        return render_template ('delete_movie.html', MovieName=request.form['movie_name'])

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html')


#-------------------------------------------

#-------------------------------------------                    
@app.route("/movie_to_delete")
def movie_to_delete():
    return render_template('delete_movie_form.html')
#-------------------------------------------

#-------------------------------------------    
# Modify a movie 
@app.route("/modify_movie", methods=["POST"])
def modify_movie():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query = ("UPDATE Movie SET MovieName=(%s), MovieYear=%s WHERE idMovie=%s")
    
    to_modify = (
                request.form['name_change'],
                request.form['year_change'],
                request.form['movie_id'],
                )
    
    cursor.execute(query, to_modify)
    cursor.close()
    cnx.commit()
    cnx.close()
    
    return render_template (
                            'modify_movie.html',  
                            MovieName=request.form['name_change'], 
                            MovieYear=request.form['year_change'],
                            idMovie=request.form['movie_id']
                            )
#-------------------------------------------

#-------------------------------------------
@app.route("/movie_to_modify")
def movie_to_modify():
    return render_template('modify_movie_form.html')
#-------------------------------------------

#-------------------------------------------
# List all movies and all attributes sorted alphabetically by the movie's name
@app.route("/list_of_movies")
def all_from_movie():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query = ("SELECT * FROM Movie ORDER BY MovieName")
    cursor.execute(query)

    data = cursor.fetchall()

    rows = []
    for row in cursor:
        print(row)
        rows.append(row)

    cursor.close()
    cnx.close()
    return render_template('list_of_movies.html', data=data)
#-------------------------------------------
#===================================================================================================================#
    
#============================================= Genre Functions: ====================================================#
#-------------------------------------------

@app.route('/genres')
def genres():
    return render_template("genres.html")

# Add a genre to a movie
@app.route("/add_genre", methods=["POST"])
def add_genre():
    try:
        cnx = mysql.connector.connect(user='root', database='MovieTheatre')
        cursor = cnx.cursor()
        
        query = (
                "INSERT INTO Genre (Genre, Movie_idMovie)"
                "VALUES(%s, %s)"
                )
        to_add =(
                request.form['genre'], 
                request.form['movieID']
                )
        
        cursor.execute(query, to_add)
        cnx.commit()
        cnx.close()
        return render_template (
                                'add_genre.html',  
                                MovieName=request.form['genre'], 
                                MovieYear=request.form['movieID']
                                )
    
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html')
#-------------------------------------------

#-------------------------------------------
@app.route("/genre_to_add")
def genre_to_add():
    return render_template('add_genre_form.html')
#-------------------------------------------

#-------------------------------------------
# Delete a genre from a movie
@app.route("/delete_genre", methods=["POST"])
def delete_genre():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query = ("DELETE FROM Genre WHERE Genre=%s AND Movie_idMovie=(%s)")
    to_delete = (
                request.form['genre'],
                request.form['movieID'],
                )

    cursor.execute(query, to_delete)
    cnx.commit()
    cnx.close()
    return render_template (
                            'delete_genre.html',  
                            Genre=request.form['genre'],
                            Movie_idMovie=request.form['movieID']
                            )
#-------------------------------------------

#-------------------------------------------
@app.route("/genre_to_delete")
def genre_to_delete():
    return render_template('delete_genre_form.html')
#-------------------------------------------

#-------------------------------------------
# List all genres and the associated movie sorted alphabetically by genre
@app.route("/list_of_genres")
def all_from_genre():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query = ("SELECT Genre.Genre, Movie.MovieName from Genre INNER JOIN Movie ON Genre.Movie_idMovie=Movie.idMovie order by Genre.Genre")
    cursor.execute(query)
    data = cursor.fetchall()
    rows = []
    for row in cursor:
        print(row)
        rows.append(row)
        cursor.close()
        cnx.close()
    return render_template('list_of_genres.html', data=data)
#-------------------------------------------
#===================================================================================================================#

#=========================================== Theatre Room Functions: ===============================================#
#-------------------------------------------

@app.route('/rooms')
def rooms():
    return render_template("rooms.html")

# Add a room
@app.route("/add_theatreroom", methods=["POST"])
def add_theatreroom():

    try:
        cnx = mysql.connector.connect(user='root', database='MovieTheatre')
        cursor = cnx.cursor()
        
        query = (
                "INSERT INTO TheatreRoom (RoomNumber, Capacity)"
                "VALUES(%s, %s)"
                )
        to_add =(
                request.form['room_num'], 
                request.form['capacity']
                )
        
        cursor.execute(query, to_add)
        cnx.commit()
        cnx.close()
        return render_template (
                                'add_theatreroom.html',  
                                RoomNum=request.form['room_num'], 
                                Capacity=request.form['capacity']
                                )
    
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html')

#-------------------------------------------

#-------------------------------------------
@app.route("/theatreroom_to_add")
def theatreroom_to_add():
    return render_template('add_theatreroom_form.html')
#-------------------------------------------

#-------------------------------------------
# Delete a theatre room
@app.route("/delete_theatreroom", methods=["POST"])
def delete_theatreroom():
    
    try:
        cnx = mysql.connector.connect(user='root', database='MovieTheatre')
        cursor = cnx.cursor()
        
        query = ("DELETE FROM TheatreRoom WHERE RoomNumber=%s")
        
        to_delete = (request.form['room_number'],)

        cursor.execute(query, to_delete)
        cnx.commit()
        cnx.close()
        return render_template (
                                'delete_theatreroom.html',  
                                RoomNumber=request.form['room_number']
                                )

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html')
#-------------------------------------------

#-------------------------------------------
@app.route("/theatreroom_to_delete")
def theatreroom_to_delete():
    return render_template('delete_theatreroom_form.html')
#-------------------------------------------

#-------------------------------------------
# Modify a theatre room 
@app.route("/modify_theatreroom", methods=["POST"])
def modify_theatreroom():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query = (
            "UPDATE TheatreRoom SET Capacity=%s WHERE RoomNumber=%s"
            )
    to_add =(
            request.form['capacity'], 
            request.form['room_num']
            )
    
    cursor.execute(query, to_add)
    cnx.commit()
    cnx.close()
    return render_template (
                            'modify_theatreroom.html',  
                            Capacity=request.form['capacity'], 
                            RoomNumber=request.form['room_num']
                            )
#-------------------------------------------

#-------------------------------------------
@app.route("/theatreroom_to_modify")
def theatreroom_to_modify():
    return render_template('modify_theatreroom_form.html')
#-------------------------------------------

#-------------------------------------------
# List the rooms and all attributes
@app.route("/list_of_rooms")
def all_from_rooms():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query = ("select * from TheatreRoom")
    cursor.execute(query)
    data = cursor.fetchall()
    rows = []
    for row in cursor:
        print(row)
        rows.append(row)
        cursor.close()
        cnx.close()
    return render_template('list_of_rooms.html', data=data)
#-------------------------------------------
#===================================================================================================================#

#============================================== Showing Functions: =================================================#
#-------------------------------------------

@app.route('/staff_showings')
def staff_showings():
    return render_template("staff_showings.html")

# Add a showing 
@app.route("/add_showing", methods=["POST"])
def add_showing():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query = (
            "INSERT INTO Showing (ShowingDateTime, Movie_idMovie, TheatreRoom_RoomNumber, TicketPrice)"
            "VALUES(%s, %s, %s, %s)"
            )
    to_add =( 
            request.form['showing_date_time'], 
            request.form['movie_id'],
            request.form['theatre_room_num'],
            request.form['ticket_price']
            )
    
    cursor.execute(query, to_add)
    cnx.commit()
    cnx.close()
    return render_template (
                            'add_showing.html',
                            ShowingDateTime=request.form['showing_date_time'],
                            Movie_idMovie=request.form['movie_id'],
                            TheatreRoom_RoomNumber=request.form['theatre_room_num'],
                            TicketPrice=request.form['ticket_price']
                            )
#-------------------------------------------

#-------------------------------------------
@app.route("/showing_to_add")
def showing_to_add():
    return render_template('add_showing_form.html')
#-------------------------------------------

#-------------------------------------------
# Delete a showing
@app.route("/delete_showing")
def delete_showing():
        
    try:
        cnx = mysql.connector.connect(user='root', database='MovieTheatre')
        cursor = cnx.cursor()
        
        query = ("DELETE FROM Showing WHERE idShowing=%s")
        
        to_delete = (request.form['showing_id'],)

        cursor.execute(query, to_delete)
        cnx.commit()
        cnx.close()
        return render_template (
                                'delete_showing.html',  
                                idShowing=request.form['showing_id']
                                )

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html')
#-------------------------------------------

#-------------------------------------------
@app.route("/showing_to_delete")
def showing_to_delete():
    return render_template('delete_showing_form.html')
#-------------------------------------------
    
#-------------------------------------------
# Modify a theatre room 
@app.route("/modify_showing", methods=["POST"])
def modify_showing():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query = (
            "UPDATE Showing SET ShowingDateTime=(%s), Movie_idMovie=%s, TheatreRoom_RoomNumber=%s, TicketPrice=%s WHERE idShowing=%s"
            )
    to_add =( 
            request.form['date_change'],
            request.form['movie_id_change'],
            request.form['room_num_change'],
            request.form['price_change'],
            request.form['id_change']
            )
    
    cursor.execute(query, to_add)
    cnx.commit()
    cnx.close()
    return render_template (
                            'modify_showing.html',  
                            ShowingDateTime=request.form['date_change'],
                            Movie_idMovie=request.form['movie_id_change'],
                            TheatreRoom_RoomNumber=request.form['room_num_change'],
                            TiketPrice=request.form['price_change'],
                            idShowing=request.form['id_change']
                            )
#-------------------------------------------

#-------------------------------------------
@app.route("/showing_to_modify")
def showing_to_modify():
    return render_template('modify_showing_form.html')
#-------------------------------------------

#-------------------------------------------
# List all the showing and all attributes sorted by date
@app.route("/list_of_showings")
def list_of_showings():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    query = ("select * from Showing ORDER BY ShowingDateTime")
    cursor.execute(query)
    data = cursor.fetchall()
    rows = []
    for row in cursor:
        print(row)
        rows.append(row)
        cursor.close()
        cnx.close()
    return render_template('list_of_showings.html', data=data)



#-------------------------------------------
#===================================================================================================================#

#============================================ Customer Functions: ==================================================#
#-------------------------------------------

@app.route('/staff_customers')
def staff_customers():
    return render_template("staff_customers.html")

# Add a customer
@app.route("/add_customer", methods=["POST"])
def add_customer():
    
    try:
        cnx = mysql.connector.connect(user='root', database='MovieTheatre')
        cursor = cnx.cursor()
        
        query = (
                "INSERT INTO Customer (FirstName, LastName, EmailAddress, Sex) VALUES(%s, %s, %s, %s)"
                )
        
        to_add =( 
                request.form['fname'], 
                request.form['lname'],
                request.form['email'],
                request.form['sex']
                )
        
        cursor.execute(query, to_add)
        cnx.commit()
        cnx.close()
        return render_template (
                                'add_customer.html',
                                FirstName=request.form['fname'],
                                LastName=request.form['lname'],
                                EmailAddress=request.form['email'],
                                Sex=request.form['sex'],
                                )

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html')
#-------------------------------------------

#-------------------------------------------
@app.route("/customer_to_add")
def customer_to_add():
    return render_template('add_customer_form.html')
#-------------------------------------------

#-------------------------------------------
# Delete a customer
@app.route("/delete_customer", methods=['POST'])
def delete_customer():
    
    try:
        cnx = mysql.connector.connect(user='root', database='MovieTheatre')
        cursor = cnx.cursor()
        
        query = ("DELETE FROM Customer WHERE idCustomer=%s")
        
        to_delete = (request.form['customer_id'],)

        cursor.execute(query, to_delete)
        cnx.commit()
        cnx.close()
        return render_template (
                                'delete_customer.html',  
                                idCustomer=request.form['customer_id']
                                )
    
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return render_template('error.html')



#-------------------------------------------

#-------------------------------------------
@app.route("/customer_to_delete")
def customer_to_delete():
    return render_template('delete_customer_form.html')
#-------------------------------------------

#-------------------------------------------
# Modify a customer
@app.route("/modify_customer", methods=["POST"])
def modify_customer():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query = (
            "UPDATE Customer SET FirstName=%s, LastName=%s, EmailAddress=%s, Sex=%s WHERE idCustomer=%s"
            )
    to_add =(
            request.form['fname'], 
            request.form['lname'],
            request.form['email'], 
            request.form['sex'], 
            request.form['id_cus']
            )
    
    cursor.execute(query, to_add)
    cnx.commit()
    cnx.close()
    return render_template (
                            'modify_customer.html',  
                            FirstName=request.form['fname'], 
                            LastName=request.form['lname'],
                            EmailAddress=request.form['email'],
                            Sex=request.form['sex'],
                            idCustomer=request.form['id_cus']
                            )
#-------------------------------------------

#-------------------------------------------
@app.route("/customer_to_modify")
def customer_to_modify():
    return render_template('modify_customer_form.html')
#-------------------------------------------

#-------------------------------------------
# list all the customers and all attributes sorted by last name
@app.route("/customer_attributes")
def all_from_customers():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query = ("select LastName,FirstName,idCustomer, EmailAddress,cast(Sex as char(1)) from Customer ORDER BY LastName")
    cursor.execute(query)

    data = cursor.fetchall()

    rows = []
    for row in cursor:
        print(row)
        rows.append(row)

    cursor.close()
    cnx.close()

    #return str(users)
    return render_template('customer_attributes.html', data=data)

#-------------------------------------------
#===================================================================================================================#

#============================================= Attend Functions: ===================================================#
#-------------------------------------------
# List all the paid for attendances and all attributes, along with, customer full names, thw showing and date, the movie and its title.  All sorted by the rating


@app.route("/list_of_attends")

def list_of_attends():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query = ("SELECT LastName, FirstName, idShowing, ShowingDateTime, Movie_idMovie, MovieName, Rating from Attend, Customer, Movie, Showing WHERE Showing.Movie_idMovie=Movie.idMovie AND Showing.idShowing=Attend.Showing_idShowing AND Attend.Customer_idCustomer=Customer.idCustomer ORDER BY Rating")
    cursor.execute(query)

    data = cursor.fetchall()

    rows = []
    for row in cursor:
        print(row)
        rows.append(row)

    cursor.close()
    cnx.close()
    return render_template('list_of_attends.html', data=data)
    
    #query = ("SELECT Customer.FirstName, Customer.LastName, Showing.idShowing, Showing.ShowingDateTime, Movie.MovieName, Movie.idMovie, Attend.* FROM Attend INNER JOIN Customer ON Attend.Customer_idCustomer=Customer.idCustomer INNER JOIN Showing ON Attend.Showing_idShowing=Showing.idShowing INNER JOIN Movie ON Showing.Movie_idMovie=Movie.idMovie ORDER BY Attend.Rating")




#########FRONT END STUFF########



#main page for customer
@app.route('/customer')
def customer():
    return render_template("customer.html")





#prompt user for name
@app.route('/profile')
def profile():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query2 = ("SELECT DISTINCT LastName from Customer ORDER BY LastName")
    cursor.execute(query2)
    LastName = cursor.fetchall()

    query3 = ("SELECT DISTINCT FirstName from Customer ORDER BY FirstName")
    cursor.execute(query3)
    FirstName = cursor.fetchall()


    return render_template('profile_form.html', LastName=LastName, FirstName=FirstName) 
    #return render_template('profile_form.html', Name=Name)


#allow a customer to select their name and see his/her profile (all the info about the customer)###

@app.route('/customer_info', methods=["POST"])
def customer_info():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()


    #query = ("select idCustomer,LastName,FirstName,EmailAddress,cast(Sex as char(1)) from Customer WHERE idCustomer=%s")
    query = ("select idCustomer,LastName,FirstName,EmailAddress,cast(Sex as char(1)) from Customer WHERE FirstName=(%s) AND LastName=(%s)")

    #query = ("SELECT * FROM Customer WHERE FirstName=(%s) AND LastName=(%s)")
    stuff = (request.form["FirstName"],request.form["LastName"])
    cursor.execute(query, stuff)


    data = cursor.fetchall()

    rows = []
    for row in cursor:
        print(row)
        rows.append(row)

    cursor.close()
    cnx.close()

    return render_template('profile.html', data=data)





###allow customer to select name adn see all movie titles and ratings 
@app.route('/history')
def history():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query2 = ("SELECT DISTINCT LastName from Customer ORDER BY LastName")
    cursor.execute(query2)
    LastName = cursor.fetchall()

    query3 = ("SELECT DISTINCT FirstName from Customer ORDER BY FirstName")
    cursor.execute(query3)
    FirstName = cursor.fetchall()





    return render_template('history_form.html', LastName=LastName, FirstName=FirstName) 


@app.route('/history_info', methods=["POST"])
def history_info():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    #query = "SELECT MovieName, Rating FROM Movie, Attend, Showing, Customer WHERE Attend.Showing_idShowing=Showing.idShowing AND Showing.Movie_idMovie=Movie.idMovie AND Customer.idCustomer=Attend.Customer_idCustomer AND idCustomer=%s"
    query = ("SELECT MovieName, Rating FROM Movie, Attend, Showing, Customer WHERE Attend.Showing_idShowing=Showing.idShowing AND Showing.Movie_idMovie=Movie.idMovie AND Customer.idCustomer=Attend.Customer_idCustomer AND Customer.FirstName=(%s) AND Customer.LastName=(%s)")

    stuff = (request.form["FirstName"],request.form["LastName"])
    cursor.execute(query, stuff)


    data = cursor.fetchall()

    rows = []
    for row in cursor:
        print(row)
        rows.append(row)

    cursor.close()
    cnx.close()

    return render_template('history.html', data=data)



@app.route("/rate")
def rate(): 
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    
    query2 = ("SELECT DISTINCT LastName from Customer, Attend WHERE Customer.idCustomer = Attend.Customer_idCustomer ORDER BY LastName")
    cursor.execute(query2)
    LastName = cursor.fetchall()

    query3 = ("SELECT DISTINCT FirstName from Customer, Attend WHERE Customer.idCustomer = Attend.Customer_idCustomer ORDER BY FirstName")
    cursor.execute(query3)
    FirstName = cursor.fetchall()

    query4 = ("SELECT DISTINCT Showing_idShowing from Attend ORDER BY Showing_idShowing")
    cursor.execute(query4)
    ShowingID = cursor.fetchall()

    Rating = ('1','2','3','4','5')

    #return render_template('rate_form.html', LastName=LastName, FirstName=FirstName, ShowingID=ShowingID, Rating=Rating) 
    return render_template('rate_form.html', LastName=LastName, FirstName=FirstName, ShowingID=ShowingID, Rating = Rating) 


@app.route('/rate_info', methods=["POST"])
def rate_info():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    #query = ("UPDATE Attend SET Rating=(%s) WHERE Showing_idShowing=(%s) AND Customer_idCustomer=(SELECT idCustomer from Customer WHERE FirstName='%s' AND LastName='%s')")
    query = ("UPDATE Attend Set Rating = %s WHERE Showing_idShowing = %s AND Customer_idCustomer = (SELECT idCustomer FROM Customer WHERE FirstName =%s AND LastName =%s")

    stuff = (request.form["Rating"],request.form["ShowingID"],request.form["FirstName"],request.form["LastName"] )
    cursor.execute(query, stuff)


    rows = []
    for row in cursor:
        print(row)
        rows.append(row)

    cursor.close()
    cnx.close()

    return render_template('rate.html')



#Attend --> select name and any showing & buy ticket for it 

@app.route("/attend")
def attend():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query2 = ("SELECT DISTINCT LastName from Customer ORDER BY LastName")
    cursor.execute(query2)
    LastName = cursor.fetchall()

    query3 = ("SELECT DISTINCT FirstName from Customer ORDER BY FirstName")
    cursor.execute(query3)
    FirstName = cursor.fetchall()

    query4 = ("SELECT DISTINCT idShowing from Showing ORDER BY idShowing")
    cursor.execute(query4)
    ShowingID = cursor.fetchall()

    return render_template('attend_form.html', LastName=LastName, FirstName=FirstName, ShowingID=ShowingID) 
    


@app.route("/attend_info", methods=["POST"])
def attend_info():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    #query = ("INSERT INTO Attend(Customer_idCustomer=(SELECT idCustomer FROM Customer WHERE Customer.FirstName=%s AND Customer.LastName=%s), Showing_idShowing=%s, Rating=0)")
    query = ("INSERT INTO Attend(Customer_idCustomer, Showing_idShowing, Rating) VALUES((select idCustomer FROM Customer WHERE Customer.FirstName=%s AND Customer.LastName=%s),%s,%s) ") 


    stuff = (request.form["FirstName"],request.form["LastName"],request.form["ShowingID"],request.form["Rating"] )
    cursor.execute(query, stuff)

    rows = []
    for row in cursor:
        print(row)
        rows.append(row)
    
    cnx.commit()
    cursor.close()
    cnx.close()

    return render_template('attend.html')





@app.route('/search')
def search():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query1 = ("SELECT DISTINCT Genre from Genre ORDER BY Genre")
    cursor.execute(query1)
    genre = cursor.fetchall()
    
    query2 = ("SELECT DISTINCT ShowingDateTime from Showing ORDER BY ShowingDateTime")
    cursor.execute(query2)
    datetime = cursor.fetchall()

    #cursor.close()
    #cnx.close()

    return render_template('search_form.html', genre=genre, datetime=datetime)
    #return render_template('search_form.html', genre=genre)



@app.route("/search_info", methods=["GET","POST"])
def search_info():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    query = ("select idShowing,ShowingDateTime,Showing.Movie_idMovie,MovieName, "
             "TheatreRoom_RoomNumber,TicketPrice,Capacity, Poster from Showing join Genre on "
             "Genre.Movie_idMovie=Showing.Movie_idMovie join TheatreRoom on TheatreRoom_RoomNumber=RoomNumber "
             "left join Attend on Showing_idShowing=idShowing join Movie on Showing.Movie_idMovie=idMovie where "
             "Genre=%s and ShowingDateTime >= %s and ShowingDateTime <= %s and MovieName= %s ")

    stuff = (request.form['Genre'], request.form['startdate'], request.form['enddate'], request.form['moviename'],)

    if request.form.get("seatsAvailable") == "1":
        query = query + "group by idShowing having count(*) < TheatreRoom.Capacity"
        cursor.execute(query, stuff)
        data = cursor.fetchall()

        rows = []
        for row in cursor:
            print(row)
            rows.append(row)

        cnx.commit()
        cursor.close()
        cnx.close()
        return render_template('search.html', data=data)

    cursor.execute(query, stuff)
    data = cursor.fetchall()

    rows = []
    for row in cursor:
        print(row)
        rows.append(row)

    cnx.commit()
    cursor.close()
    cnx.close()

    return render_template('search.html', data=data)






#@app.route("/poster")
#def poster()


#@app_route("/poster_info", methods=["POST"])  








#-------------------------------------------

@app.route('/sqlInjection')
def sqlInjection(name=None):
    return render_template('sqlInjection_form.html')

@app.route('/injection', methods=["POST"])
def sqlInjectionResult():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    id = request.form['id']
    #query = ("SELECT * FROM Customer WHERE idCustomer='"+ id + "'")
    query = ("SELECT idCustomer, LastName, FirstName, EmailAddress, cast(Sex as char(1)) FROM Customer WHERE idCustomer='"+ id + "'")


    cursor.execute(query)
    print("Attempting: " + query)
    users=cursor.fetchall()
    print(users)
    
    rows = []
    for row in cursor:
        rows.append(row)
    
    cnx.commit()
    cnx.close()
    return render_template('sqlinjection.html', users=users)
    














if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
