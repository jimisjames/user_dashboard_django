from django.shortcuts import render, redirect
from .models import *
import bcrypt



def index(request):

    return render(request, "user_dash/index.html")


def dashboard(request):

    if "user_id" in request.session.keys():
        users = User.objects.exclude(id=request.session["user_id"])
        logged_user = User.objects.get(id=request.session["user_id"])

        context = {
            "users" : users,
            "logged_user" : logged_user
        }
        return render(request, "user_dash/dashboard.html", context)

    return redirect("/")


def edit(request, user_id=None):

    context = {}
    if user_id:
        user = User.objects.get(id=user_id)
        context["user"] = user

    return render(request, "user_dash/edit.html", context)


def wall(request, id):

    messages = Message.objects.filter(user_id=id).order_by("-created_at")
    user = User.objects.get(id=id)
    context = {
        "messages" : messages,
        "user" : user
    }
    return render(request, "user_dash/wall.html", context)


def form(request, user_id=None): 

    errors = User.objects.validate_reg(request.POST)

    if errors:
        if user_id and len(errors) == 1 and errors["email"] == "You are already registered with this Email Address":
            user = User.objects.get(id=user_id)
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.email = request.POST["email"]
            user.password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            user.save()
            return redirect("/dashboard")     #success

        else:
            if user_id:
                if "email" in errors and errors["email"] == "You are already registered with this Email Address":
                    errors.pop("email")
                for key, val in errors.items():
                    messages.info(request, val, extra_tags=key)
                return redirect("/edit/%s" % user_id)     #failure

            else:
                for key, val in errors.items():
                    messages.info(request, val, extra_tags=key)
                request.session["first_name"] = request.POST["first_name"]
                request.session["last_name"] = request.POST["last_name"]
                request.session["email"] = request.POST["email"]
                return redirect("/edit")     #failure

    else:
        hash_pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], password=hash_pw, level=0)
        return redirect("/dashboard")     #success

def reg(request):

    errors = User.objects.validate_reg(request.POST)

    if errors:
        for key, val in errors.items():
            messages.info(request, val, extra_tags=key)
        request.session["first_name"] = request.POST["first_name"]
        request.session["last_name"] = request.POST["last_name"]
        request.session["email"] = request.POST["email"]
        request.session["description"] = request.POST["description"]
        return redirect("/")    # failure
    else:
        request.session.clear()
        hash_pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        new_user = User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"], email=request.POST["email"], desc=request.POST["description"], password=hash_pw, level=0)
        request.session["user_id"] = new_user.id
        request.session["user_name"] = new_user.first_name + " " + new_user.last_name
        request.session["user_level"] = new_user.level

        return redirect("/dashboard")    # success


def login(request):

    result = User.objects.validate_login(request.POST)
    errors = result[0]

    if len(errors):
        for val in errors:
            messages.warning(request, val)
            request.session["email2"] = request.POST["email"]
        return redirect("/")    # failure
    else:
        request.session["user_id"] = result[1]["id"]
        request.session["user_name"] = result[1]["first_name"] + " " + result[1]["last_name"]
        request.session["user_level"] = result[1]["level"]
        request.session["secret_key"] = bcrypt.hashpw(str(result[1]["created_at"]).encode(), bcrypt.gensalt()).decode('utf8')

        return redirect("/dashboard")    # success


def message(request, id):

    if len(request.POST["message"]):
        Message.objects.create(user=User.objects.get(id=id), message=request.POST["message"], poster=User.objects.get(id=request.session["user_id"]))

    return redirect("/wall/%s" % id)


def delete_message(request, message_id, user_id):

    message = Message.objects.get(id=message_id)

    if message.poster.id == request.session["user_id"] or message.user.id == request.session["user_id"]:
        message.delete()

    return redirect("/wall/%s" % user_id)


def comment(request, id):

    if len(request.POST["comment"]):
        Comment.objects.create(message=Message.objects.get(id=request.POST["message_id"]), user=User.objects.get(id=request.session["user_id"]), comment=request.POST["comment"])

    return redirect("/wall/%s" % id)


def delete_comment(request, comment_id, user_id):

    comment = Comment.objects.get(id=comment_id)

    if comment.user.id == request.session["user_id"] or comment.message.user.id == request.session["user_id"]:
        comment.delete()

    return redirect("/wall/%s" % user_id)


def delete(request, id):

    if request.session["user_level"] == 9:
        user = User.objects.get(id=id)
        user.delete()

    return redirect("/dashboard")


def toggle_admin(request, id):

    if request.session["user_level"] == 9:
        user = User.objects.get(id=id)
        if user.level == 9:
            user.level = 0
        elif user.level == 0:
            user.level = 9
        user.save()

    return redirect("/dashboard")


def logout(request):

    request.session.clear()

    return redirect("/")