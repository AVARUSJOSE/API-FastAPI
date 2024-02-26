"""importamos pydantic"""
from pydantic import BaseModel


class User(BaseModel):
    """clase que representa a un usuario comun"""
    id: int
    name: str
    username: str
    email: str


list_users = [User(id=1,
                   name="Leanne Graham",
                   username="Bret",
                   email="Sincere@april.biz"),
              User(id=2,
                   name="Ervin Howell",
                   username="Antonette",
                   email="Shanna@melissa.tv"),
              User(id=3,
                   name="Clementine Bauch",
                   username="Samantha",
                   email="Nathan@yesenia.net"),
              User(id=4,
                   name="Patricia Lebsack",
                   username="Karianne",
                   email="Julianne.OConner@kory.org"),
              User(id=5,
                   name="Chelsey Dietrich",
                   username="Kamren",
                   email="Lucio_Hettinger@annie.ca"),
              User(id=6,
                   name="Mrs. Dennis Schulist",
                   username="Leopoldo_Corkery",
                   email="Karley_Dach@jasper.info"),
              User(id=7,
                   name="Kurtis Weissnat",
                   username="Elwyn.Skiles",
                   email="Telly.Hoeger@billy.biz"),
              User(id=8,
                   name="Nicholas Runolfsdottir V",
                   username="Maxime_Nienow",
                   email="Sherwood@rosamond.me"),
              User(id=9,
                   name="Glenna Reichert",
                   username="Delphine",
                   email="Chaim_McDermott@dana.io"),
              User(id=10,
                   name="Clementina DuBuque",
                   username="Moriah.Stanton",
                   email="Rey.Padberg@karina.biz")]
