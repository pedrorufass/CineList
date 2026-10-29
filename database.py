import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise RuntimeError("Configure SUPABASE_URL e SUPABASE_KEY no arquivo .env.")

supabase = create_client(url, key)

def listar_filmes():
    response = (
        supabase
        .table("movies")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return response.data

def adicionar_filme(titulo, genero, ano):
    response = (
        supabase
        .table("movies")
        .insert({
            "title": titulo,
            "genre": genero,
            "year": ano,
            "watched": False
        })
        .execute()
    )
    return response.data[0]

def atualizar_assistido(movie_id, watched):
    response = (
        supabase
        .table("movies")
        .update({"watched": watched})
        .eq("id", movie_id)
        .execute()
    )
    return response.data[0]

def excluir_filme(movie_id):
    (
        supabase
        .table("movies")
        .delete()
        .eq("id", movie_id)
        .execute()
    )
