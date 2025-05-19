 
        
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
            "cover_image": self.cover_image,
            "price": self.price
        }
    
    def matches_search(self, query):
        query_lower = query.lower()
        return (query_lower in self.title.lower() or
                query_lower in self.author.lower() or
                query_lower in self.description.lower())


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
 
atomic_habits = Book(
    book_id=5,
    title="Atomic Habits",
    author="James Clear",
    description="A practical guide to breaking bad habits and building good ones, with actionable strategies for lasting change.",
    cover_image="/static/img/atomicHabits.png",
    price=16.99
)

subtle_art = Book(
    book_id=6,
    title="The Subtle Art of Not Giving a F*ck",
    author="Mark Manson",
    description="A counterintuitive approach to living a good life, focusing on embracing limitations and accepting challenges.",
    cover_image="/static/img/subtleArt.png",
    price=13.99
)

rules_for_life = Book(
    book_id=7,
    title="12 Rules for Life",
    author="Jordan B. Peterson",
    description="A self-help classic offering practical advice for finding meaning and stability in life.",
    cover_image="/static/img/12RulesForLife.png",
    price=15.49
)

think_like_a_monk = Book(
    book_id=8,
    title="Think Like a Monk",
    author="Jay Shetty",
    description="Jay Shetty shares timeless wisdom and practical steps for reducing stress and improving focus.",
    cover_image="/static/img/thinkLikeAMonk.png",
    price=14.49
)

 
grit = Book(
    book_id=9,
    title="Grit",
    author="Angela Duckworth",
    description="Explores the power of passion and perseverance in achieving success.",
    cover_image="/static/img/grit.png",
    price=13.49
)

 
# cant_hurt_me = Book(
#     book_id=10,
#     title="Can't Hurt Me",
#     author="David Goggins",
#     description="The inspiring story of David Goggins, who overcame adversity through mental toughness and discipline.",
#     cover_image="/static/img/cantHurtMe.png",
#     price=17.99
# )

# Add the new books to your list
books.extend([
    dopamine,
    let_them,
    myth_of_normal,
    the_body_keeps_the_score,
    atomic_habits,
    subtle_art,
    rules_for_life,
    think_like_a_monk,
    grit
])



# books_data = [book.to_dict() for book in books]
# print(books_data)


 