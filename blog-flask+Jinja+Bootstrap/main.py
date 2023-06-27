from flask import Flask, render_template, request
import requests
import smtplib
import os

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        message=request.form['message']
        try:
            with smtplib.SMTP(host='smtp.office365.com', port=587) as connection:
                connection.starttls()
                connection.login(user=os.environ.get('username'), password=os.environ.get('password'))
                connection.sendmail(
                    to_addrs='woaiwojialuther@gmail.com',
                    from_addr=os.environ.get('username'),
                    msg=f"Subject: {name} sent you a message\n\nName: {name}\n\nEmail: {email}\n\nPhone: {phone}\n\nMessage: {message}"
                )
        except:
            return "<h1>Email didn't send successfully, please try again!</h1>"
        else:
            return render_template('contact.html', msg=True)
    return render_template('contact.html', msg=False)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
