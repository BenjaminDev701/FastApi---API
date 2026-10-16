
from fastapi import Body
from fastapi import HTTPException
from fastapi import Query
from fastapi import FastAPI

app = FastAPI(title="Mi Blog")

BLOG_POST = [
    {"id": 1, "title": "Hola desde FastAPI",
        "Content": "Mi primer post en FastAPI"},
    {"id": 2, "title": "Hola desde FastAPI",
     "Content": "Mi segundo post en FastAPI"},
    {"id": 3, "title": "Django vs FastAPI",
     "Content": "Mi tercer post en FastAPI"}

]


@app.get("/")
def home():
    return {"message": "Bienvenido al primer endpoint"}


@app.get("/posts")
def list_posts(query: str | None = Query(default=None, description="Buscar por titulo")):

    if query:
        result = [post for post in BLOG_POST if query.lower()
                  in post["title"].lower()]

        return {"data": result, "query": query}
    return {"data": BLOG_POST}


@app.get("/posts/{post_id}")
def get_post(post_id: int, query: bool | None = Query(default=None, description="Agregar el contenido del post")):
    result = [post for post in BLOG_POST if post_id == post["id"]]
    if not result:
        raise HTTPException(status_code=404, detail="Post no encontrado")

    # usamos copy por que es para copiar el valor sin afectar el post original
    post = result[0].copy()

# si es falso entonces eliminamos el contentn con pop y mandamos el post,
# si el query es nulo osea que no enviamos nada de query entonces se envia por default el post con content
    if query is True:
        post.pop("Content")
    return {"data": post}


@app.post("/posts")
def create_post(post: dict = Body(...)):
    if "title" not in post or "Content" not in post:
        return {"error": "Title y content son requeridos"}
        # strip elimina los espacios
    if not str(post["title"].strip()):
        return {"error": "Title es requerido"}

    new_id = BLOG_POST[-1]["id"]+1 if BLOG_POST else 1
    new_post = {"id": new_id,
                "title": post["title"], "Content": post["Content"]}

    BLOG_POST.append(new_post)
    return {"data": "Post Creado"}


@app.put("/posts/{post_id}")
def update_post(post_id: int, data: dict = Body(...)):
    for post in BLOG_POST:
        if post_id == post["id"]:
            if "title" in data:
                post["title"] = data["title"]
            if "Content" in data:
                post["Content"] = data["Content"]
            return {"message": "Post actualizado correctamente"}
    raise HTTPException(status_code=404, detail="No se encontro el post")


@app.delete("/posts/{post_id}")
def delete_posst(post_id: int):
    # index es un identificador de pocision en el cual nosotros eliminamos haci son tomar en cuenta el id que es mejor por que puede que sea id:1,5,7
    for index, post in enumerate(BLOG_POST):
        if post["id"] == post_id:
            BLOG_POST.pop(index)
            return {"message": "Ha sido borrado correctamente"}
    raise HTTPException(status_code=404, detail="No se encontro el pos")
