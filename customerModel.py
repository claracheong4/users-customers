import os

import psycopg2

from flask import Flask, jsonify, request

from dotenv import load_dotenv
load_dotenv()

import jwt

# from .env
DATABASE = os.getenv('DATABASE')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('HOST')
DATABASE_PORT = os.getenv('PORT')

def fetchAll():
    con = None
    try:
        con = psycopg2.connect(
        dbname=DATABASE,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT)

        cur = con.cursor()

        cur.callproc('get_all_customers')

        rows = cur.fetchall()
        print(rows)

        return jsonify(rows)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if con is not None:
            cur.close()
            con.close()

        return False

    finally:
        if con is not None:
            cur.close()
            con.close()

def deleteAll():
    con = None
    try:
        con = psycopg2.connect(
        dbname=DATABASE,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT)

        cur = con.cursor()

        cur.execute('CALL reset_customers()');
        con.commit()

        return True

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if con is not None:
            cur.close()
            con.close()

        return False

    finally:
        if con is not None:
            cur.close()
            con.close()

def add(id, name, dob):
    con = None
    try:
        con = psycopg2.connect(
        dbname=DATABASE,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT)

        cur = con.cursor()

        cur.callproc('add_customer', (id, name, dob))

        row = cur.fetchone()
        print(row)

        con.commit()

        return jsonify(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if con is not None:
            cur.close()
            con.close()

        return False

    finally:
        if con is not None:
            cur.close()
            con.close()

def update(id, name, dob):
    con = None
    try:
        con = psycopg2.connect(
        dbname=DATABASE,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT)

        cur = con.cursor()

        cur.callproc('update_customer', (id, name, dob))

        row = cur.fetchone()
        print(row)

        con.commit()

        return jsonify(row)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if con is not None:
            cur.close()
            con.close()

        return False

    finally:
        if con is not None:
            cur.close()
            con.close()

def delete(id):
    con = None
    try:
        con = psycopg2.connect(
        dbname=DATABASE,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT)

        cur = con.cursor()

        cur.callproc('delete_customer', (id))
        isSuccessful = cur.fetchone()

        con.commit()

        return isSuccessful[0]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if con is not None:
            cur.close()
            con.close()

        return False

    finally:
        if con is not None:
            cur.close()
            con.close()

def fetch_youngest_customers(n):
    con = None
    try:
        con = psycopg2.connect(
        dbname=DATABASE,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT)

        cur = con.cursor()
        cur.callproc('get_youngest_customers', (n))

        rows = cur.fetchall()
        print(rows)

        return jsonify(rows)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if con is not None:
            cur.close()
            con.close()

        return False

    finally:
        if con is not None:
            cur.close()
            con.close()