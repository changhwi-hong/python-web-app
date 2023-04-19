from flask import Flask
import psycopg

app = Flask(__name__)
app.config.from_prefixed_env("POSTGRES")

@app.route("/ping")
def health_check():
    return "pong"

@app.route("/sample")
def sample():
    with psycopg.connect(f"postgresql://{app.config['HOST']}:{app.config['PORT']}/{app.config['DATABASE']}",
        user=app.config['USER'], password=app.config['PASSWD']) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM actor")
            return str(cur.fetchmany(10)[0])
