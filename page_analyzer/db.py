import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def add_url_to_db(url):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("INSERT INTO urls (name) VALUES (%s)", (url,))
        conn.commit()
        conn.close()


def get_url_by_name(url):
    conn = get_connection()

    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("SELECT * FROM urls WHERE name = %s", (url,))

        url = cur.fetchall()

        if url:
            url_data = url
        else:
            url_data = None

        conn.commit()
        conn.close()

    return url_data


def get_url_by_id(url_id):
    conn = get_connection()

    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("SELECT * FROM urls WHERE id = %s", (url_id,))

        url_data = cur.fetchall()

        conn.commit()
        conn.close()

    return url_data


def get_all_urls_desc():
    conn = get_connection()

    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute("SELECT * FROM urls ORDER BY id DESC")

        all_urls = cur.fetchall()

        conn.commit()
        conn.close()

    return all_urls


def add_check_to_db(url_id, status_code, h1, title, description):
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("INSERT INTO url_checks ("
                    "url_id, "
                    "status_code,"
                    "h1, "
                    "title, "
                    "description "
                    ") "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (url_id, status_code, h1, title, description)
                    )
        conn.commit()
        conn.close()


def get_url_with_latest_check():
    conn = get_connection()

    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            "SELECT urls.id, "
            "urls.name, "
            "COALESCE(url_checks.status_code::text, '') as status_code, "
            "COALESCE(MAX(url_checks.created_at)::text, '') as latest_check "
            "FROM urls "
            "LEFT JOIN url_checks ON urls.id = url_checks.url_id "
            "GROUP BY urls.id, url_checks.status_code "
            "ORDER BY urls.id DESC",
        )

        all_url_with_latest_checks = cur.fetchall()

        conn.commit()
        conn.close()

        return all_url_with_latest_checks


def get_checks_desc(url_id):
    conn = psycopg2.connect(DATABASE_URL)

    with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
        cur.execute(
            "SELECT id, "
            "status_code, "
            "COALESCE(h1, '') as h1, "
            "COALESCE(title, '') as title, "
            "COALESCE(description, '') as description, "
            "created_at::text "
            "FROM url_checks "
            "WHERE url_id = %s "
            "ORDER BY id DESC",
            (url_id,)
        )

        all_checks = cur.fetchall()

        conn.commit()
        conn.close()

    return all_checks
