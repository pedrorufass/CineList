# CineList

Aplicação desktop desenvolvida em Python para organizar uma lista de filmes. O sistema utiliza Tkinter para a interface gráfica, Supabase para persistência dos dados e Redis como camada de cache.

## Problema

Manter uma lista de filmes manualmente pode dificultar a organização e a consulta das informações. O CineList centraliza esses dados em uma interface simples.

## Objetivo

Desenvolver uma aplicação que integre uma interface gráfica, Supabase e Redis, demonstrando persistência de dados e utilização prática de cache.

## Funcionalidades

- Cadastrar filmes
- Listar filmes
- Pesquisar filmes
- Marcar e desmarcar filmes como assistidos
- Excluir filmes
- Persistir dados no Supabase
- Utilizar Redis para cache
- Informar na interface a origem dos dados

## Tecnologias

- Python
- Tkinter
- Supabase
- Redis
- Upstash Redis
- python-dotenv

## Instalação

Instale Python 3.10 ou superior.

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

## Supabase

Crie um projeto no Supabase.

Abra o SQL Editor e execute o conteúdo de `supabase.sql`.

Depois, obtenha no painel do projeto a Project URL e a chave publicável.

Crie um arquivo `.env` na raiz do projeto:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua_chave_publicavel
UPSTASH_REDIS_REST_URL=https://seu-banco.upstash.io
UPSTASH_REDIS_REST_TOKEN=seu_token
```

## Redis

O projeto utiliza o Upstash Redis.

Crie um banco Redis no Upstash e copie o REST URL e o REST Token da área de detalhes do banco.

O Redis é usado para armazenar temporariamente a lista de filmes.

## Execução

Com o ambiente virtual ativado:

```powershell
python main.py
```

## Como o Redis é utilizado

Ao carregar a lista de filmes, a aplicação consulta primeiro o Redis.

Se existir um cache válido, a lista é carregada do Redis.

Se não existir, a aplicação consulta o Supabase, salva o resultado no Redis por 60 segundos e mostra os dados.

Quando um filme é adicionado, atualizado ou excluído, o cache é apagado. Isso evita que a interface apresente dados antigos.

A interface informa a origem dos dados no canto superior direito da lista.

## Demonstração

1. Execute a aplicação.
2. Na primeira carga, observe `Fonte dos dados: Supabase`.
3. Clique em `Atualizar lista`.
4. Observe `Fonte dos dados: Redis`.
5. Adicione um novo filme.
6. O cache será invalidado.
7. Clique em `Atualizar lista`.
8. O sistema consultará novamente o Supabase e criará um novo cache.

## Estrutura

```text
CineList/
├── main.py
├── interface.py
├── database.py
├── cache.py
├── requirements.txt
├── .env.example
├── .gitignore
├── supabase.sql
└── README.md
```

## Segurança

O arquivo `.env` não deve ser enviado ao GitHub. As credenciais devem permanecer em variáveis de ambiente.
