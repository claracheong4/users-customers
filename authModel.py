import os

import psycopg2

from flask import Flask, jsonify

from dotenv import load_dotenv
load_dotenv()

import jwt

# from .env
DATABASE = os.getenv('DATABASE')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('HOST')
DATABASE_PORT = os.getenv('PORT')
AUTHSECRET = os.getenv("AUTHSECRET")
EXPIRESSECONDS = os.getenv('EXPIRESSECONDS')

def addUser(userId, userSecret):
    con = None
    try:
        con = psycopg2.connect(
        dbname=DATABASE,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT)

        cur = con.cursor()

        cur.callproc('add_user', (userId, userSecret))

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

def authenticate(userId, userSecret):

    con = None
    try:
        con = psycopg2.connect(
        dbname=DATABASE,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT)

        cur = con.cursor()

        cur.callproc('query_user', (userId, userSecret))

        isUser = cur.fetchone()

        if isUser :
            encoded_jwt = jwt.encode(
                {"secret": userSecret}, AUTHSECRET,
                algorithm='HS256')
            token = encoded_jwt.decode('utf-8')

            cur.execute("SELECT query_blacklist(%s)", (token, ))
            isBlacklisted = cur.fetchone()
            if isBlacklisted:
                cur.execute("SELECT delete_blacklist(%s)", (token, ))

            con.commit()

            return {
                "token": token,
                "expiresin" : EXPIRESSECONDS
            }
        else:
            return False

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

def verify(token):

    con = None
    try:
        con = psycopg2.connect(
        dbname=DATABASE,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT)

        cur = con.cursor()

        cur.execute("SELECT query_blacklist(%s)", (token, ))

        isBlacklisted = cur.fetchone()

        return not isBlacklisted[0]

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

def blacklist(token):
    con = None
    try:
        con = psycopg2.connect(
        dbname=DATABASE,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT)

        cur = con.cursor()

        cur.execute("SELECT add_blacklist(%s)", (token, ))

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