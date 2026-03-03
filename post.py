class Post:
    def __init__(self, blog_data):
        self.id = blog_data["id"]
        self.title = blog_data["title"]
        self.body = blog_data['body']
        self.subtitle = blog_data["subtitle"]

