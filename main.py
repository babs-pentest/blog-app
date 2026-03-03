from datetime import datetime
from dotenv import load_dotenv
from flask import Flask,render_template, url_for, request
import os
import requests
from post import Post
from smtplib import SMTP

load_dotenv()
blog_url = os.environ.get("BLOG_URL")
response = requests.get(url=blog_url)
response.raise_for_status()
all_blog_post = response.json()
all_blog_post_objects = []
for each_post in all_blog_post:
    all_blog_post_objects.append(Post(each_post))

now = datetime.now()
app = Flask(__name__)

def send_email(sender_email, message_body, user_name):
    recipient_addr = os.environ.get("RECIPIENT_ADDR")
    blog_password = os.environ.get("BLOG_PASSWORD")
    with SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=recipient_addr, password=blog_password)
        connection.sendmail(from_addr=sender_email, to_addrs=recipient_addr, msg=f"Subject: Message from Babs-Dev\n\n\n Message from: {user_name} \n{message_body}")


def form_submission():
    name = request.form["name_input"]
    email_address = request.form["email_input"]
    contact_number = request.form["contact_input"]
    message = request.form["message_input"]
    send_email(email_address, message, name)
        #print(f"Username: {name}\n Email Address: {email_address}\n Contact Number: {contact_number}")


@app.route("/")
def index():
    return render_template("index.html", all_posts=all_blog_post_objects, now=now)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        form_submission()
        message = "Successfully sent message"
        return render_template("contact.html", message=message)
    else:
        message = "Contact Me"
        return render_template("contact.html", message=message)


@app.route("/post/<int:id>")
def show_post(id):
    return render_template("post.html", all_posts=all_blog_post_objects, now=now, post_id=id)





if __name__ == "__main__":
    app.run(debug=True, port=5000)