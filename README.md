Final Project - Poetry
Web Programming with Python and JavaScript

This is my implementation of CS50W's Final Project.

Short Description of the project:
    This is an online platform for poets to share their poems and show off their poetry skills to the whole wide world!
    Poets (Users) are able to browse through all of the poems posted on Poetry.
    They're also able to read a poem completely and they can rate and review it if they want.
    Once a rating/review has been made on a poem, the poet (user) who posted that poem will get a notification about it.
    Poets are also able to browse through the explore section of the Poetry which arranges the poems according to some categories like most popular poems, top rated poems, short poems, etc.
    The poets are also able to see the average rating and total number of ratings made on a poem.
    In case if a poet forgets his/her password, he/she is able to reset it with the help of his/her e-mail!
    This web application is fully mobile responsive and it has some nice and sleek animations!

Description of some files:
    views.py: Holds all the Django views. It is responsible for much of the server's functionality.
    admin.py: Connects database models to Django Admin (for site administrator).
    models.py: Contains all the Django database models.
    urls.py (in the poems directory): Connects views and urls.
    bg.png: Background png image.
    icon.ico: Icon for the website.
    jumbo-bg.jpeg: Background image for the registration and login jumbotrons.
    logo.png and logo1.png: Brand logo for Poetry.
    script.js: JavaScript file containing functions like show/hide password, functions for star rating, etc.
    styles.css: Contains the custom CSS used in this web app.
    db.sqlite3: Database file containing all of the tables.
    base.html: Base HTML template to be used in every other templates.
    edit_profile.html: Contains edit profile section (Change Password, Delete Account).
    explore.html: Contains explore sections having categories such as top rated poems, recent poems, short poems, etc.
    index.html: Contains poems section (that shows recent poems) with a search bar to search the poems.
    login.html: Contains the login form.
    notifications.html: Contains notifications section to display all the notifications (with pagination for old notifications).
    profile.html: Contains profile information of the poet with the poems of the poet.
    read.html: Contains the complete poem, displays rating, avergae rting, and reviews, and contains a rating and review form.
    register.html: Contains the register form.
    reset_confirm.html: Contains a form to the change the password without entering the current password.
    reset.html: Contains a form to send a reset password link to a poet's e-mail address.
    write.html: Contains a form for writing the poem.
