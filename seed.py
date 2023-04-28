from models import db, User, Post, Tag, PostTag
from app import app
import random


db.drop_all()
db.create_all()

names = [
    "Olivia Johnson",
    "Alexander Wilson",
    "Emma Hernandez",
    "William Davis",
    "Charlotte Martin",
    "Daniel Thompson",
    "Sophia Anderson",
    "Lucas Lee",
    "Ava Garcia",
    "Nicholas Wright"
]


for name in names:
    fullname = name.split(' ')
    user = User(first_name = fullname[0], last_name = fullname[1], image_url = f"https://picsum.photos/id/{names.index(name) + 27}/300/300")
    db.session.add(user)

db.session.commit()

placeholder_text = """
Placeholder text, oh what a sight,
A jumble of words with no insight,
Random letters and numbers galore,
With no meaning or purpose to explore.

A placeholder for words to come,
A temporary fix for a code to run,
But oh, how it lacks any grace,
A chaotic mess that's hard to trace.

Yet, in its own strange way,
Placeholder text has something to say,
A reminder of the work ahead,
A promise of what's to be said.

For in the world of code and design,
The beauty lies in what's yet to shine,
So let the placeholder text reside,
Until the real words come alive.

And when the time comes to replace,
The gibberish with meaningful grace,
Let the placeholder text remind,
Of the journey that's left behind.

For every keystroke and every click,
A new line of text, oh so slick,
A placeholder text so grand,
Crafted with the help of a robot's hand.

For besides these last two lines you see,
This is a prompt from chat GPT.
"""

posts = [
    "Understanding the Importance of Placeholder Text in UI Design",
    "The Evolution of Placeholder Text: A Brief History",
    "5 Tips for Crafting Effective Placeholder Text",
    "Why Placeholder Text is Essential for Web Development",
    "The Psychology of Placeholder Text: How it Affects User Experience",
    "Maximizing Your Use of Placeholder Text for Better Design",
    "The Dos and Don'ts of Creating Placeholder Text",
    "Placeholder Text Best Practices: What You Need to Know",
    "Making the Most of Placeholder Text in Your Next Web Project",
    "The Art of Crafting Compelling Placeholder Text",
    "Lorem Ipsum: The Design World's Go-To Filler Text",
    "The History of Lorem Ipsum and Its Use in Design",
    "10 Creative Ways to Use Lorem Ipsum in Your Design Projects",
    "Mastering the Art of Lorem Ipsum in Your Writing",
    "The Dos and Don'ts of Using Lorem Ipsum in Your Design",
    "Why Lorem Ipsum is Still a Relevant Design Tool Today",
    "Designing with Lorem Ipsum: Tips and Tricks",
    "Maximizing Your Use of Lorem Ipsum for Web Design",
    "10 Alternatives to Lorem Ipsum You Need to Know",
    "Creating Effective Lorem Ipsum for Your Website Design"
]

for title in posts:
    post = Post(title = title, content = placeholder_text, user_id = random.randint(1, 10))
    db.session.add(post)




db.session.commit()

tags = [ 
    "lifestyle",
        "fashion",
        "travel",
        "food",
        "health",
        "fitness",
        "parenting",
        "technology",
        "business",
        "marketing",
        "finance",
        "education",
        "politics",
        "entertainment",
        "sports",
        "music",
        "art",
        "books",
        "culture",
        "personal development"
        ]

for name in tags:
    tag = Tag(tag_name = name )
    db.session.add(tag)
    post = Post.query.get(random.randint(1, 20))
    tag.posts.append(post)

db.session.commit()