import smtplib
import datetime
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Poem, ChangePassword, Rating, Review, Notification
from django.db.models import Q
from django.db.models.functions import Length


def get_notif_count(request):
    # Get notifications count
    notif_count = 0
    try:
        notifications = Notification.objects.all().filter(
            receiver=request.user, read=False
        )
        for notification in notifications:
            notif_count += 1
    except:
        print("No notifications!")
    return notif_count


# Create your views here.


@require_http_methods(["GET", "POST"])
@login_required(login_url="login")
def index(request):
    """ Redirect to home page if user is logged in """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get search query
        q = request.POST["q"]
        # Return to index page if no q
        if not q:
            return HttpResponseRedirect(reverse("index"))
        # Go to search route with q
        return HttpResponseRedirect(reverse("search", args=(q,)))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Get poems from db (recents first)
        poems = Poem.objects.all().order_by("-id")

        # Show 12 poems per page
        paginator = Paginator(poems, 12)
        page = request.GET.get("page")
        poems_per_page = paginator.get_page(page)
        # Get required data from db
        context = {
            "user": request.user,
            "poets": Poem.objects.all().distinct('user'),
            "poems": poems_per_page,
            "poems1": Poem.objects.all(),
        }

        # Get notifications count
        context["notif_count"] = get_notif_count(request)

        # Render index.html page
        return render(request, "poems/index.html", context=context)


@require_http_methods(["GET"])
def search_view(request, q):
    """ Search poem/poet """
    # Return to index page if no q
    if not q:
        return HttpResponseRedirect(reverse("index"))
    # Filter for q in poems or poets
    poems = Poem.objects.all().filter(
        Q(title__icontains=q) | Q(user__username__icontains=q)
    )

    # Show 12 poems per page
    paginator = Paginator(poems, 12)
    page = request.GET.get("page")
    poems_per_page = paginator.get_page(page)

    # Get required data from db
    context = {
        "user": request.user,
        "poets": User.objects.all(),
        "poems": poems_per_page,
        "poems1": Poem.objects.all(),
    }

    # Get notifications count
    context["notif_count"] = get_notif_count(request)

    # Render index.html page
    return render(request, "poems/index.html", context=context)


@require_http_methods(["GET", "POST"])
def register_view(request):
    """ Register user/displays register form """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get form fields
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        # Ensure form fields are not empty
        if not first_name:
            messages.success(request, "Must provide first name!")
            return HttpResponseRedirect(reverse("register"))
        if not last_name:
            messages.success(request, "Must provide last name!")
            return HttpResponseRedirect(reverse("register"))
        if not email:
            messages.success(request, "Must provide e-mail address!")
            return HttpResponseRedirect(reverse("register"))
        if not username:
            messages.success(request, "Must provide username!")
            return HttpResponseRedirect(reverse("register"))
        if not password1:
            messages.success(request, "Must provide password!")
            return HttpResponseRedirect(reverse("register"))
        if not password2:
            messages.success(request, "Must confirm password!")
            return HttpResponseRedirect(reverse("register"))

        # Ensure first name and last name are valid
        if not first_name.isalpha():
            messages.success(request, "Must provide a proper first name!")
            return HttpResponseRedirect(reverse("register"))
        if not last_name.isalpha():
            messages.success(request, "Must provide a proper last name!")
            return HttpResponseRedirect(reverse("register"))

        # Ensure username > 3 characters
        if len(username) < 4:
            messages.success(request, "Username must contain at least 4 characters!")
            return HttpResponseRedirect(reverse("register"))

        # Ensure password1 > 5 characters
        if len(password1) < 6:
            messages.success(request, "Password must contain at least 6 characters!")
            return HttpResponseRedirect(reverse("register"))

        # Ensure password1 and password2 matches
        if password1 != password2:
            messages.success(request, "Password mismatched!")
            return HttpResponseRedirect(reverse("register"))

        # Ensure email and username is unique
        user = User.objects.filter(email=email)
        if len(user) != 0:
            messages.success(request, "E-mail address already exists!")
            return HttpResponseRedirect(reverse("register"))
        user = User.objects.filter(username=username)
        if len(user) != 0:
            messages.success(request, "Username already exists!")
            return HttpResponseRedirect(reverse("register"))

        # If everything is fine, register & log in user
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password1,
        )
        user.save()

        # Authenticate
        user = authenticate(request, username=username, password=password1)
        login(request, user)
        messages.success(request, "Account created!")
        return HttpResponseRedirect(reverse("index"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render(request, "poems/register.html")


@require_http_methods(["GET", "POST"])
def login_view(request):
    """ Logs in user/displays log in form """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get form fields
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate
        user = authenticate(request, username=username, password=password)

        # Ensure if authentication is successful
        if user is None:
            messages.success(request, "Invalid username/password!")
            return HttpResponseRedirect(reverse("login"))

        # If authentication is successful, log in user
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render(request, "poems/login.html")


@require_http_methods(["GET"])
@login_required(login_url="login")
def logout_view(request):
    """ Logs in user/displays log in form """

    # Log out user
    logout(request)
    messages.success(request, "Logged out!")
    return HttpResponseRedirect(reverse("login"))


@require_http_methods(["GET", "POST"])
@login_required(login_url="login")
def write_view(request):
    """ Write a poem/display write poem page """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get form fields
        title = request.POST["title"]
        poem = request.POST["poem"]

        # Ensure form fields are not empty
        if not title:
            messages.success(request, "Must provide title!")
            return HttpResponseRedirect(reverse("write"))
        if not poem:
            messages.success(request, "Must write a poem!")
            return HttpResponseRedirect(reverse("write"))

        # If everything is fine, save poem to database & return user to index page
        poem = Poem(user=request.user, title=title, poem=poem)
        poem.save()
        messages.success(request, "Poem written!")
        return HttpResponseRedirect(reverse("index"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        context = {}
        # Get notifications count
        context["notif_count"] = get_notif_count(request)
        return render(request, "poems/write.html", context)


@require_http_methods(["GET"])
@login_required(login_url="login")
def profile_view(request, user):
    """ Displays profile of users """

    # Ensure user exists
    try:
        user = User.objects.get(username=user)
    except User.DoesNotExist:
        raise Http404("User does not exist!")

    # Get user's poems from db (recents first)
    poems = Poem.objects.all().filter(user=user).order_by("-id")

    # Show 12 poems per page
    paginator = Paginator(poems, 12)
    page = request.GET.get("page")
    poems_per_page = paginator.get_page(page)
    # Get required data from db
    context = {"user": user, "poems": poems_per_page}

    # Get notifications count
    context["notif_count"] = get_notif_count(request)

    # Render profile.html page
    return render(request, "poems/profile.html", context)


@require_http_methods(["GET", "POST"])
@login_required(login_url="login")
def read_view(request, poem_id):
    """ Reads poem """

    # Ensure poem exists
    try:
        poem = Poem.objects.get(id=poem_id)
    except Poem.DoesNotExist:
        raise Http404("Poem does not exist!")

    # Get data from db to be displayed
    context = {"poem": poem}
    try:
        context["rating"] = Rating.objects.get(poem=poem, user=request.user)
    except:
        print("No Ratings by User!")

    try:
        context["review"] = Review.objects.get(poem=poem, user=request.user)
    except:
        print("No Review by User!")

    try:
        reviews = (
            Review.objects.filter(poem=poem).exclude(user=request.user).order_by("-id")
        )
        # Show 10 reviews per page
        paginator = Paginator(reviews, 10)
        page = request.GET.get("page")
        reviews_per_page = paginator.get_page(page)
        context["reviews"] = reviews_per_page
        ratings = []
        for review in reviews:
            try:
                rating = Rating.objects.get(poem=poem, user=review.user)
                ratings.append(rating)
            except:
                ratings.append({"user": review.user, "rating": "0.0"})
                print("No Ratings!")
        context["ratings"] = ratings
    except:
        print("No Reviews!")

    # Get notifications count
    context["notif_count"] = get_notif_count(request)

    return render(request, "poems/read.html", context)


@require_http_methods(["GET", "POST"])
def reset_view(request):
    """ Reset password phase 1 """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get e-mail from form field
        email = request.POST["email"]

        # Ensure email is not empty
        if not email:
            messages.success(request, "Must provide E-mail address!")
            return HttpResponseRedirect(reverse("reset"))

        # Ensure email is present in database
        present = User.objects.filter(email=email)
        if not present:
            messages.success(request, "E-mail address does not exists!")
            return HttpResponseRedirect(reverse("reset"))

        # If everything is fine, send mail to user with a reset password link
        sender = "pinocchiopizza987654321@gmail.com"
        receiver = email
        user = User.objects.get(email=email)
        username = user.username
        position = email.find("@")
        email1 = email[0:position]
        email2 = email[position + 1 :]
        # Message to be sent
        # Create the base text message.
        message = EmailMessage()
        message["Subject"] = "Reset password"
        message["From"] = Address("Poetry", "pinocchiopizza987654321", "gmail.com")
        message["To"] = Address(username, email1, email2)
        asparagus_cid = make_msgid()
        message.add_alternative(
            f"""\
        <html>
        <head></head>
        <body>
            <p>Hello {username}</p>
            <p>We got a request to reset your Poetry password.</p>
            <p>You can use the link below only once!</p>
            <a href="http://127.0.0.1:8000/reset/{username}">Reset</a>
            <p>If you ignore this message, your password will not be changed.</p>
        </body>
        </html>
        """.format(
                asparagus_cid=asparagus_cid[1:-1]
            ),
            subtype="html",
        )
        # Creates SMTP session
        s = smtplib.SMTP("smtp.gmail.com", 587)
        # Start TLS for security
        s.starttls()
        # Authentication
        s.login(sender, "sultan@123")
        # Send mail
        s.send_message(message)
        # Terminate session
        s.quit()

        # Initiate password change
        change_password = ChangePassword(user=user)
        change_password.save()

        # Redirect user to reset
        messages.success(request, "Link sent!")
        return HttpResponseRedirect(reverse("reset"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Get data from db to be displayed
        return render(request, "poems/reset.html")


@require_http_methods(["GET", "POST"])
def reset_confirm_view(request, username):
    """ Reset password phase 2 """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get form fields
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        # Ensure form fields are not empty
        if not password1:
            messages.success(request, "Must provide password!")
            return HttpResponseRedirect(reverse("reset_confirm", args=(username,)))
        if not password2:
            messages.success(request, "Must confirm password!")
            return HttpResponseRedirect(reverse("reset_confirm", args=(username,)))

        # Ensure password1 > 5 characters
        if len(password1) < 6:
            messages.success(request, "Password must contain at least 6 characters!")
            return HttpResponseRedirect(reverse("reset_confirm", args=(username,)))

        # Ensure password1 and password2 matches
        if password1 != password2:
            messages.success(request, "Password mismatched!")
            return HttpResponseRedirect(reverse("reset_confirm", args=(username,)))

        # Change password
        user = User.objects.get(username=username)
        user.set_password(password1)
        user.save()

        messages.success(request, "Password changed!")
        return HttpResponseRedirect(reverse("login"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Ensure user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404("User does not exist!")

        # Ensure user's instance is made in change password
        present = ChangePassword.objects.filter(user=user)
        if not present:
            messages.success(request, "Trying to hack?")
            return HttpResponseRedirect(reverse("login"))

        # Delete user's instance from change password model
        if present:
            present.delete()

        # Render reset confirm html page
        context = {"username": username}
        return render(request, "poems/reset_confirm.html", context)


@require_http_methods(["GET"])
@login_required(login_url="login")
def edit_profile_view(request):
    """ Edit profile """

    context = {}
    # Get notifications count
    context["notif_count"] = get_notif_count(request)

    return render(request, "poems/edit_profile.html", context)


@require_http_methods(["POST"])
@login_required(login_url="login")
def change_password_view(request):
    # Get form fields
    current_password = request.POST["current_password"]
    new_password = request.POST["new_password"]
    confirm_password = request.POST["confirm_password"]

    # Ensure fields are not empty
    if not current_password:
        messages.success(request, "Must provide current password!")
        return HttpResponseRedirect(reverse("edit_profile"))
    if not new_password:
        messages.success(request, "Must provide new password!")
        return HttpResponseRedirect(reverse("edit_profile"))
    if not confirm_password:
        messages.success(request, "Must confirm new password!")
        return HttpResponseRedirect(reverse("edit_profile"))

    # Ensure current password is correct
    user = request.user
    if not user.check_password(current_password):
        messages.success(request, "Invalid current password!")
        return HttpResponseRedirect(reverse("edit_profile"))

    # Ensure new password > 5 characters
    if len(new_password) < 6:
        messages.success(request, "New password must contain at least 6 characters!")
        return HttpResponseRedirect(reverse("edit_profile"))

    # Ensure new password and current password does not match
    if new_password == current_password:
        messages.success(request, "New password must be different!")
        return HttpResponseRedirect(reverse("edit_profile"))

    # Ensure new password and confirm password matches
    if new_password != confirm_password:
        messages.success(request, "Password mismatched!")
        return HttpResponseRedirect(reverse("edit_profile"))

    # Change password and redirect to edit profile
    user.set_password(new_password)
    user.save()
    update_session_auth_hash(request, request.user)
    logout(request)
    messages.success(request, "Password changed! Log in again!")
    return HttpResponseRedirect(reverse("login"))


@require_http_methods(["POST"])
@login_required(login_url="login")
def delete_account_view(request):
    # Get form fields
    password = request.POST["password"]

    # Ensure fields are not empty
    if not password:
        messages.success(request, "Must provide password!")
        return HttpResponseRedirect(reverse("edit_profile"))

    # Ensure current password is correct
    user = request.user
    if not user.check_password(password):
        messages.success(request, "Invalid current password!")
        return HttpResponseRedirect(reverse("edit_profile"))

    # Calculate current average rating of the poems without the current user's ratings
    poems = Poem.objects.all()
    for poem in poems:
        n = 0
        avg_rating = 0
        ratings = Rating.objects.all().filter(poem=poem).exclude(user=user)
        for rating in ratings:
            avg_rating += rating.rating
            n += 1
        if n != 0:
            avg_rating = avg_rating / n
        total_rating = n
        poem.average_rating = avg_rating
        poem.total_ratings = total_rating
        poem.save()

    # Delete user account
    user.delete()
    messages.success(request, "Account deleted!")
    return HttpResponseRedirect(reverse("register"))


@require_http_methods(["POST"])
@login_required(login_url="login")
def rate_view(request):
    """ Rate poem """

    # Get rating
    rating_slected = request.POST["rating_slected"]
    poem_id = request.POST["poem_id"]
    poem = Poem.objects.get(id=poem_id)
    user = request.user

    # Ensure rating is not 0.0
    if rating_slected == "0.0":
        messages.success(request, "Rating cannot be zero!")
        return HttpResponseRedirect(reverse("read", args=(poem_id,)))

    # Ensure user has not rated for the poem already
    rating = Rating.objects.filter(poem=poem, user=user)
    if rating:
        messages.success(request, "Already rated!")
        return HttpResponseRedirect(reverse("read", args=(poem_id,)))

    # Add user's rating and save it
    rating = Rating(user=user, poem=poem, rating=rating_slected)
    rating.save()

    # Add notification
    if request.user != poem.user:
        star = "stars"
        if rating_slected == "1.0":
            star = "star"
        notification_data = f"{int(float(rating_slected))} {star}"
        notification = Notification(
            receiver=poem.user,
            sender=user,
            poem=poem,
            notification_type="Rate",
            notification_data=notification_data,
        )
        notification.save()

    # Calculate current average rating and total rating of the poem
    n = 0
    avg_rating = 0
    ratings = Rating.objects.all().filter(poem=poem)
    for rating in ratings:
        avg_rating += rating.rating
        n += 1
    avg_rating = avg_rating / n
    total_rating = n
    poem.average_rating = avg_rating
    poem.total_ratings = total_rating
    poem.save()

    # Redirect back to read poem page
    messages.success(request, "Poem rated!")
    return HttpResponseRedirect(reverse("read", args=(poem_id,)))


@require_http_methods(["GET"])
@login_required(login_url="login")
def explore_view(request):
    """ Explore poetry """

    top_rated_poems = Poem.objects.all().order_by("-average_rating", "-total_ratings")[
        :6
    ]
    most_popular_poems = Poem.objects.all().order_by(
        "-total_ratings", "-average_rating"
    )[:6]
    lowest_rated_poems = Poem.objects.all().order_by("average_rating", "total_ratings")[
        :6
    ]
    recents = Poem.objects.all().order_by("-date")[:6]
    shortest_poems = Poem.objects.all().order_by(Length("poem").asc())[:6]
    longest_poems = Poem.objects.all().order_by(Length("poem").desc())[:6]
    context = {
        "top_rated_poems": top_rated_poems,
        "most_popular_poems": most_popular_poems,
        "lowest_rated_poems": lowest_rated_poems,
        "recents": recents,
        "shortest_poems": shortest_poems,
        "longest_poems": longest_poems,
    }

    # Get notifications count
    context["notif_count"] = get_notif_count(request)

    return render(request, "poems/explore.html", context)


@require_http_methods(["POST"])
@login_required(login_url="login")
def review_view(request):
    """ Rate poem """

    # Get form fields, poem object and user
    poem_id = request.POST["poem_id"]
    headline = request.POST["headline"]
    review = request.POST["review"]
    poem = Poem.objects.get(id=poem_id)
    user = request.user

    # Ensure headline and review are not empty
    if not headline:
        messages.success(request, "Must provide headline!")
        return HttpResponseRedirect(reverse("read", args=(poem_id,)))
    if not review:
        messages.success(request, "Must provide a review!")
        return HttpResponseRedirect(reverse("read", args=(poem_id,)))

    # Ensure user has not reviewed the poem already
    reviewed = Review.objects.filter(poem=poem, user=user)
    if reviewed:
        messages.success(request, "Already reviewed!")
        return HttpResponseRedirect(reverse("read", args=(poem_id,)))

    # Add user's review and save it
    add_review = Review(user=user, poem=poem, headline=headline, review=review)
    add_review.save()

    # Add notification
    if request.user != poem.user:
        notification_data = f"{headline}"
        notification = Notification(
            receiver=poem.user,
            sender=user,
            poem=poem,
            notification_type="Review",
            notification_data=notification_data,
        )
        notification.save()

    # Redirect back to read poem page
    messages.success(request, "Review added!")
    return HttpResponseRedirect(reverse("read", args=(poem_id,)))


@require_http_methods(["GET"])
@login_required(login_url="login")
def notification_view(request):
    context = {}

    cnt = 0
    # Get unread notifications and then mark them as read
    try:
        unread_notifications = (
            Notification.objects.all()
            .filter(receiver=request.user, read=False)
            .order_by("-id")
        )
        context["unread_notifications"] = unread_notifications
        for unread_notification in unread_notifications:
            cnt += 1
            unread_notification.read = True
            unread_notification.save()
    except:
        print("No notifications!")

    # Get read notifications
    try:
        read_notifications = (
            Notification.objects.all()
            .filter(receiver=request.user, read=True)
            .order_by("-id")[cnt:]
        )
        # Show 10 notifications per page
        paginator = Paginator(read_notifications, 10)
        page = request.GET.get("page")
        notifications_per_page = paginator.get_page(page)
        context["read_notifications"] = notifications_per_page
        print("Context: ", context)
        print("Context: ", read_notifications)

    except:
        print("No notifications!")

    print("Context: ", context)
    # Get notifications count
    context["notif_count"] = get_notif_count(request)
    return render(request, "poems/notifications.html", context)
