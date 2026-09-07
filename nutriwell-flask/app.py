"""NutriWell Flask application."""

## has started here 

from __future__ import annotations

import os

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR.parent / ".env"

load_dotenv(ENV_FILE)


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "replace-this-before-production"
)


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

database_url = os.getenv("DATABASE_URL")

if database_url:
    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql+psycopg2://",
            1
        )

    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://",
            "postgresql+psycopg2://",
            1
        )
else:
    # Local fallback database
    database_url = "sqlite:///nutriwell.db"


app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ============================================================
# DATABASE MODEL
# ============================================================

class Consultation(db.Model):
    __tablename__ = "consultations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        nullable=False
    )

    interest = db.Column(
        db.String(200),
        nullable=True
    )

    message = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<Consultation {self.id} - {self.email}>"


# ============================================================
# EMAIL CONFIGURATION
# ============================================================

app.config["MAIL_SERVER"] = os.getenv(
    "MAIL_SERVER",
    "smtp.gmail.com"
)

app.config["MAIL_PORT"] = int(
    os.getenv("MAIL_PORT", "587")
)

app.config["MAIL_USE_TLS"] = (
    os.getenv("MAIL_USE_TLS", "true").lower() == "true"
)

app.config["MAIL_USE_SSL"] = (
    os.getenv("MAIL_USE_SSL", "false").lower() == "true"
)

app.config["MAIL_USERNAME"] = os.getenv(
    "MAIL_USERNAME"
)

app.config["MAIL_PASSWORD"] = os.getenv(
    "MAIL_PASSWORD"
)

app.config["MAIL_DEFAULT_SENDER"] = os.getenv(
    "MAIL_USERNAME"
)

mail = Mail(app)


# ============================================================
# WEBSITE PAGES
# ============================================================

PAGES = {

    "about": {
        "title": "About NutriWell",
        "eyebrow": "OUR APPROACH",
        "headline": "Nutrition guidance made for real life.",
        "intro": (
            "NutriWell turns evidence-informed nutrition into "
            "practical routines you can return to on busy weekdays, "
            "shared family meals and every season in between."
        ),
        "hero_image": "boost1.jpg",

        "section_heading": (
            "A more sustainable way to feel well"
        ),

        "section_body": (
            "We look beyond one-size-fits-all meal rules. "
            "Each conversation begins with your habits, access, "
            "culture and goals, then moves toward small changes "
            "you can repeat with confidence."
        ),

        "cards": [

            {
                "title": "Listen first",
                "body": (
                    "Your lifestyle and food preferences lead the "
                    "plan — not a rigid template."
                ),
                "tag": "01"
            },

            {
                "title": "Use clear science",
                "body": (
                    "We translate credible nutrition principles "
                    "into choices that make sense at your table."
                ),
                "tag": "02"
            },

            {
                "title": "Build steady momentum",
                "body": (
                    "Simple check-ins and useful tools help you "
                    "notice progress without perfectionism."
                ),
                "tag": "03"
            }

        ]
    },


    "services": {
        "title": "Nutrition Services",
        "eyebrow": "HOW WE CAN HELP",
        "headline": (
            "Useful support for the food decisions in front of you."
        ),

        "intro": (
            "Whether you are working on energy, family meals "
            "or confidence in the kitchen, our services make "
            "the next step feel clear and manageable."
        ),

        "hero_image": "boost1.jpg",

        "section_heading": (
            "Choose the support that fits your season"
        ),

        "section_body": (
            "Every service begins with a focused conversation "
            "and ends with practical notes, food ideas and a "
            "next-step plan you can use straight away."
        ),

        "cards": [

            {
                "title": "One-to-one consultation",
                "body": (
                    "A focused 60-minute nutrition conversation "
                    "shaped around your goals, routine and current concerns."
                ),
                "tag": "PERSONALISED"
            },

            {
                "title": "Meal plan review",
                "body": (
                    "Bring your existing routine, shopping list "
                    "or meal ideas and leave with a realistic, "
                    "balanced update."
                ),
                "tag": "PRACTICAL"
            },

            {
                "title": "Family food sessions",
                "body": (
                    "Support for households building calmer, "
                    "more nourishing meals together — without "
                    "separate cooking."
                ),
                "tag": "TOGETHER"
            }

        ]
    },


    "recipes": {
        "title": "Healthy Recipes",
        "eyebrow": "THE RECIPE LIBRARY",
        "headline": (
            "Good food can be simple, colourful and satisfying."
        ),

        "intro": (
            "These recipe frameworks are designed for real "
            "schedules: flexible portions, familiar ingredients "
            "and clear options for making meals your own."
        ),

        "hero_image": "boost1.jpg",

        "section_heading": (
            "Three dependable meal ideas"
        ),

        "section_body": (
            "Use these combinations as a starting point, then "
            "switch the produce, proteins and grains based on "
            "what is fresh, affordable and appealing this week."
        ),

        "cards": [

            {
                "title": "Bright breakfast bowl",
                "body": (
                    "Creamy yogurt, fruit, toasted oats and seeds "
                    "for a balanced start that comes together "
                    "in ten minutes."
                ),
                "tag": "10 MIN"
            },

            {
                "title": "Build-your-own lunch plate",
                "body": (
                    "Combine a hearty grain, crisp vegetables, "
                    "beans or eggs and a flavourful dressing "
                    "for a lunch that lasts."
                ),
                "tag": "25 MIN"
            },

            {
                "title": "Family dinner tray",
                "body": (
                    "Roast colourful vegetables with a protein "
                    "and serve alongside a grain or flatbread "
                    "for a low-fuss shared supper."
                ),
                "tag": "40 MIN"
            }

        ]
    },


    "resources": {
        "title": "Free Resources",
        "eyebrow": "SIMPLE TOOLS",
        "headline": (
            "A little structure makes healthy choices easier to repeat."
        ),

        "intro": (
            "Explore practical checklists and gentle prompts "
            "that support meal planning, grocery shopping and "
            "balanced daily routines."
        ),

        "hero_image": "kd10.png",

        "section_heading": (
            "Start with a small useful tool"
        ),

        "section_body": (
            "Our resources focus on the details that matter "
            "most when a busy day is unfolding: what to shop "
            "for, what to make and how to keep the plan flexible."
        ),

        "cards": [

            {
                "title": "Seven-day meal rhythm",
                "body": (
                    "A printable prompt sheet for finding a "
                    "calmer pattern of breakfasts, lunches and dinners."
                ),
                "tag": "PLANNING"
            },

            {
                "title": "Balanced basket guide",
                "body": (
                    "A grocery-list framework with room for fresh "
                    "favourites, quick staples and comfort foods."
                ),
                "tag": "SHOPPING"
            },

            {
                "title": "Snack pairings",
                "body": (
                    "Straightforward ideas for combining fibre, "
                    "protein and flavour in between-meal snacks."
                ),
                "tag": "EVERYDAY"
            }

        ]
    },


    "blog": {
        "title": "The NutriWell Journal",
        "eyebrow": "PRACTICAL NOTES",
        "headline": "Thoughtful nutrition, without the noise.",

        "intro": (
            "Short, useful reads for building more ease around "
            "food, family meals and the routines that support "
            "a healthier everyday."
        ),

        "hero_image": "nutriwell-program-bowl.jpg",

        "section_heading": "Recent reading",

        "section_body": (
            "Start with an article below, then take one small "
            "note that makes your next meal, shop or planning "
            "session feel more manageable."
        ),

        "cards": [

            {
                "title": "Five affordable ways to add more colour",
                "body": (
                    "A flexible approach to shopping for produce "
                    "that works with the season and your budget."
                ),
                "tag": "4 MIN READ",
                "link": "affordable-colour"
            },

            {
                "title": "A calmer way to plan weekday lunches",
                "body": (
                    "A realistic lunch rhythm that starts with "
                    "repeatable components, not rigid recipes."
                ),
                "tag": "5 MIN READ",
                "link": "weekday-lunches"
            },

            {
                "title": "Build a balanced plate with what you have",
                "body": (
                    "A simple visual framework for combining "
                    "familiar foods into a satisfying meal."
                ),
                "tag": "6 MIN READ",
                "link": "balanced-plate"
            }

        ]
    }

}


# ============================================================
# PROGRAMS
# ============================================================

PROGRAMS = {

    "seven-day-reset": {

        "title": "7-Day Healthy Eating Reset",

        "duration": "One week",

        "price": "UGX 36,000",

        "summary": (
            "A gentle week of meal structure, simple shopping "
            "prompts and realistic recipes designed to help "
            "you reset without starting over."
        ),

        "highlights": [
            "Daily meal guidance",
            "Fresh, flexible recipes",
            "Smart shopping prompts"
        ],

        "image": "kd9.1.jpg"
    },


    "thirty-day-lifestyle": {

        "title": "30-Day Healthy Lifestyle Program",

        "duration": "Four weeks",

        "price": "UGX 70,000",

        "summary": (
            "Four practical weeks of personalised meal planning, "
            "check-ins and supportive tools for building a "
            "steadier food routine."
        ),

        "highlights": [
            "Personalised meal plan",
            "Weekly check-ins",
            "Progress tracker",
            "Exclusive resources"
        ],

        "image": "nutriwell-program-bowl.jpg"
    },


    "physical-exercise": {

        "title": "Physical Exercise",

        "duration": "Six weeks",

        "price": "UGX 100,000",

        "summary": (
            "A personalised wellness programme designed to help "
            "you build strength, improve fitness, boost energy "
            "and support a healthier lifestyle through safe and "
            "practical physical activity."
        ),

        "highlights": [
            "Personalised exercise guidance",
            "Strength and fitness improvement",
            "Healthy lifestyle support"
        ],

        "image": "jimm1.jpg"
    }

}


# ============================================================
# BLOG ARTICLES
# ============================================================

ARTICLES = {

    "affordable-colour": {

        "title": "Five affordable ways to add more colour",

        "category": "SMART SHOPPING",

        "lede": (
            "A bright plate does not need an expensive grocery "
            "receipt. Here are five gentle ways to work with "
            "the colour already around you."
        ),

        "paragraphs": [

            (
                "Start by treating colour as an invitation rather "
                "than a rule. One green vegetable, one orange "
                "fruit or a handful of beans can make a meal feel "
                "more varied without making it complicated."
            ),

            (
                "Frozen produce is a helpful equal partner to "
                "fresh options. It is picked at peak ripeness, "
                "keeps for longer and can be added directly to "
                "soups, rice bowls, omelettes and smoothies."
            ),

            (
                "When you shop, choose one new ingredient and "
                "one familiar staple. The mix keeps food "
                "interesting while making the week ahead feel "
                "easy to manage."
            )

        ]
    },


    "weekday-lunches": {

        "title": "A calmer way to plan weekday lunches",

        "category": "MEAL RHYTHMS",

        "lede": (
            "The easiest lunch plan is not seven different "
            "recipes. It is a short list of components you "
            "enjoy repeating in different combinations."
        ),

        "paragraphs": [

            (
                "Choose one grain or starchy base, one protein, "
                "two vegetables and one punchy dressing or sauce. "
                "Prepare what helps on a day you have time, then "
                "assemble during the week."
            ),

            (
                "A favourite container, a clear spot in the fridge "
                "and ingredients you genuinely like are small "
                "logistical details that make a plan more likely "
                "to happen."
            ),

            (
                "If you miss a day, nothing is ruined. Use the "
                "remaining components for supper or freeze them "
                "for the next busy week."
            )

        ]
    },


    "balanced-plate": {

        "title": "Build a balanced plate with what you have",

        "category": "FOOD CONFIDENCE",

        "lede": (
            "Balanced meals can be made from a supermarket "
            "basket, a roadside market haul or the leftover "
            "ingredients already in your kitchen."
        ),

        "paragraphs": [

            (
                "Picture your plate as a conversation between "
                "satisfying foods. Add a source of protein, a "
                "colourful fruit or vegetable, and a carbohydrate "
                "that helps you feel comfortably fuelled."
            ),

            (
                "There is no perfect percentage to chase. The "
                "useful question is whether the meal includes "
                "enough variety to feel steady and satisfying "
                "for you."
            ),

            (
                "Start with what is available, then add rather "
                "than subtract. A boiled egg, a scoop of beans "
                "or fresh sliced fruit can make a familiar meal "
                "feel more supportive."
            )

        ]
    }

}


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/")
def home():

    return render_template(
        "home.html",
        page="home",
        title=(
            "KD Nutrition and Wellness Centre | "
            "Nutrition for a Better You"
        ),
        programs=PROGRAMS
    )


# ============================================================
# PROGRAMS PAGE
# ============================================================

@app.get("/programs")
def programs():

    return render_template(
        "programs.html",
        page="programs",
        title=(
            "Nutrition Programs | "
            "KD Nutrition and Wellness Centre"
        ),
        programs=PROGRAMS
    )


# ============================================================
# PROGRAM DETAIL
# ============================================================

@app.get("/programs/<slug>")
def program_detail(slug):

    program = PROGRAMS.get(slug)

    if not program:
        abort(404)

    return render_template(
        "program_detail.html",
        page="programs",
        title=(
            f"{program['title']} | "
            "KD Nutrition and Wellness Centre"
        ),
        program=program
    )


# ============================================================
# BLOG ARTICLE
# ============================================================

@app.get("/blog/<slug>")
def article_detail(slug):

    article = ARTICLES.get(slug)

    if not article:
        abort(404)

    return render_template(
        "article.html",
        page="blog",
        title=(
            f"{article['title']} | "
            "KD Nutrition and Wellness Centre"
        ),
        article=article
    )


# ============================================================
# CONTACT / CONSULTATION
# ============================================================

@app.route(
    "/contact",
    methods=["GET", "POST"]
)
@app.route(
    "/consultation",
    methods=["GET", "POST"]
)
def contact():

    if request.method == "POST":

        # Get form values
        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        interest = request.form.get(
            "interest",
            ""
        ).strip()

        message = request.form.get(
            "message",
            ""
        ).strip()


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not name:

            flash(
                "Please enter your name.",
                "error"
            )

            return redirect(
                url_for("contact")
            )


        if not email:

            flash(
                "Please enter your email address.",
                "error"
            )

            return redirect(
                url_for("contact")
            )


        # ----------------------------------------------------
        # CREATE CONSULTATION
        # ----------------------------------------------------

        consultation = Consultation(
            name=name,
            email=email,
            interest=interest,
            message=message
        )


        try:

            # Add consultation to database
            db.session.add(consultation)


            # ------------------------------------------------
            # EMAIL SETTINGS
            # ------------------------------------------------

            mail_username = app.config.get(
                "MAIL_USERNAME"
            )

            if not mail_username:

                raise RuntimeError(
                    "MAIL_USERNAME is not configured."
                )


            # ------------------------------------------------
            # CREATE EMAIL
            # ------------------------------------------------

            msg = Message(

                subject=(
                    "New Consultation Request: "
                    f"{interest or 'General Consultation'}"
                ),

                sender=mail_username,

                recipients=[
                    mail_username
                ],

                reply_to=email
            )


            # ------------------------------------------------
            # EMAIL BODY
            # ------------------------------------------------

            msg.body = f"""
New consultation request from the
KD Nutrition and Wellness Centre website.

Name:
{name}

Email:
{email}

Support needed:
{interest or "Not specified"}

Client's message:
{message}
"""


            # ------------------------------------------------
            # SEND EMAIL
            # ------------------------------------------------

            mail.send(msg)


            # ------------------------------------------------
            # SAVE TO DATABASE
           

            db.session.commit()

            # SUCCESS MESSAGE

            flash(
                (
                    f"Thank you, {name}. "
                    "Your consultation request has been "
                    "sent successfully. We will be in touch shortly."
                ),
                "success"
            )


        except Exception as error:

            # Undo database changes
            db.session.rollback()


            # Print full error to Flask console
            app.logger.exception(
                "Consultation submission failed: %s",
                error
            )


            flash(
                (
                    "Sorry, your request could not be sent. "
                    "Please try again later."
                ),
                "error"
            )


        return redirect(
            url_for("contact")
        )
    # GET REQUEST
    return render_template(
        "contact.html",
        page="contact",
        title=(
            "Book a Consultation | "
            "KD Nutrition and Wellness Centre"
        )
    )
# CLIENT PORTAL
@app.get("/login")
def login():

    return render_template(
        "portal.html",
        page="portal",
        title=(
            "Client Portal | "
            "KD Nutrition and Wellness Centre"
        )
    )

# GENERAL PAGES
@app.get("/<page>")
def landing_page(page):

    data = PAGES.get(page)

    if not data:
        abort(404)

    return render_template(
        "landing.html",
        page=page,
        title=(
            f"{data['title']} | "
            "KD Nutrition and Wellness Centre"
        ),
        data=data
    )



# 404 ERROR PAGE


@app.errorhandler(404)
def not_found(error):

    return (
        render_template(
            "404.html",
            page="not-found",
            title=(
                "Page not found | "
                "KD Nutrition and Wellness Centre"
            )
        ),
        404
    )
# CREATE DATABASE TABLES


with app.app_context():
    db.create_all()

# START APPLICATION
if __name__ == "__main__":

    port = int(
        os.getenv(
            "PORT",
            "5000"
        )
    )

    debug_mode = (
        os.getenv(
            "FLASK_DEBUG",
            "false"
        ).lower() == "true"
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug_mode
    )