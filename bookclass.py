import json

 
        
class Book:
    def __init__(self, book_id,title, author, description, cover_image, price=None):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.description = description
        self.cover_image = cover_image  # path or URL to image
        self.price = price

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "description": self.description,
            "cover_page": self.cover_image,
            "price": self.price
        }


dopamine = Book(
    book_id = 1,
    title="Dopamine",
    author="Daniel Z. Lieberman and Michael E. Long",
    description="Explores the role of dopamine in motivation, pleasure, and addiction.",
    cover_image="/static/img/dopamine.png",
    price=15.99
)

let_them = Book(
    book_id = 2,
    title="Let Them",
    author="Mel Robbins",
    description=(
        "A bestselling self-help book encouraging readers to stop wasting energy trying to control others and focus on their own happiness and goals."
    ),
    cover_image="/static/img/letThem.png",
    price=12.99
)

myth_of_normal = Book(
    book_id = 3,
    title="The Myth of Normal",
    author="Gabor Maté and Daniel Maté",
    description="Challenges conventional ideas about health and wellness, emphasizing trauma's role.",
    cover_image="/static/img/mythOfNormal.png",
    price=14.99
)

the_body_keeps_the_score = Book(
    book_id = 4,
    title="The Body Keeps the Score",
    author="Bessel van der Kolk",
    description=(
        "A groundbreaking book on trauma's impact on the brain and body, "
        "offering innovative approaches to healing and recovery."
    ),
    cover_image= "/static/img/theBodyKeepsTheScore.png",
    price=18.99
)

books = []
books.append(dopamine)
books.append(let_them)
books.append(myth_of_normal)
books.append(the_body_keeps_the_score)

books_data = [book.to_dict() for book in books]

