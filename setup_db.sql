\connect customers_db customers_admin;

DROP TABLE IF EXISTS Customers, Users, BlackList CASCADE;

-- Users

CREATE TABLE Users (
	id integer,
	secret text NOT NULL,
	CONSTRAINT users_pri_key PRIMARY KEY (id)
);

ALTER TABLE Users OWNER TO customers_admin;

CREATE OR REPLACE FUNCTION add_user (INOUT id int, INOUT secret text) RETURNS RECORD AS $$
BEGIN
	INSERT INTO Users
		VALUES (id, secret);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION query_user (IN user_id int, IN user_secret text) RETURNS boolean AS $$
BEGIN
	RETURN (SELECT COUNT(*) FROM Users
		WHERE id = user_id AND secret = user_secret) > 0;
END;
$$ LANGUAGE plpgsql;

-- BlackList

CREATE TABLE BlackList (
	token text PRIMARY KEY
);

ALTER TABLE BlackList OWNER TO customers_admin;

CREATE OR REPLACE FUNCTION add_blacklist (INOUT token text) RETURNS text AS $$
BEGIN
	INSERT INTO BlackList (token)
		VALUES (token);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION query_blacklist (IN curr_token text) RETURNS boolean AS $$
BEGIN
	RETURN (SELECT COUNT(*) FROM BlackList WHERE
		token = curr_token) > 0;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_blacklist (IN curr_token text) RETURNS boolean AS $$
DECLARE
	curr_count int := (SELECT COUNT(*) FROM BlackList);
BEGIN
	DELETE FROM BlackList
		where token = curr_token;
	IF curr_count - 1 = (SELECT COUNT(*) FROM BlackList) THEN
		RETURN TRUE;
	END IF;
	RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

-- Customers

CREATE TABLE Customers (
	id integer,
	name text,
	dob date,
	updated_at timestamp,
	CONSTRAINT customers_pri_key PRIMARY KEY (id)
);

ALTER TABLE Customers OWNER TO customers_admin;

-- maintain updated_at attribute
CREATE OR REPLACE FUNCTION customers_updated_at_func() RETURNS trigger
AS $$
BEGIN
	new.updated_at := NOW()::timestamp;
	RETURN new;
END;
$$ LANGUAGE plpgsql;

CREATE trigger customers_updated_at_trigger
BEFORE INSERT OR UPDATE ON Customers
FOR EACH ROW EXECUTE FUNCTION customers_updated_at_func();

CREATE OR REPLACE PROCEDURE reset_customers ()
AS $$
BEGIN
DELETE FROM Customers;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_all_customers () RETURNS TABLE (
	id integer,
	name text,
	dob date,
	updated_at timestamp
) AS $$
BEGIN
	RETURN QUERY (
		SELECT *
		FROM Customers
	);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION add_customer (
	INOUT cust_id integer,
	INOUT name text,
	INOUT dob date,
	OUT updated_at timestamp
) RETURNS RECORD AS $$
BEGIN
	INSERT INTO Customers (id, name, dob)
	VALUES (cust_id, name, dob);
	updated_at := (SELECT Customers.updated_at FROM Customers WHERE id = cust_id);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_customer (
	INOUT cust_id integer,
	INOUT cust_name text,
	INOUT cust_dob date,
	OUT updated_at timestamp
) RETURNS RECORD AS $$
BEGIN
	IF (SELECT COUNT(*) FROM Customers WHERE id = cust_id) = 0 THEN
		RAISE EXCEPTION 'Customer to update does not exist.';
	END IF;

	UPDATE Customers
		SET name = cust_name,
			dob = cust_dob
		WHERE id = cust_id;
	updated_at := (SELECT Customers.updated_at FROM Customers WHERE id = cust_id);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_customer (IN cust_id integer) RETURNS boolean AS $$
DECLARE
	curr_count int := (SELECT COUNT(*) FROM Customers);
BEGIN
	DELETE FROM Customers
		WHERE id = cust_id;
	IF curr_count - 1 = (SELECT COUNT(*) FROM Customers) THEN
		RETURN TRUE;
	END IF;
	RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_youngest_customers (n integer) RETURNS TABLE (
	id integer,
	name text,
	dob date,
	updated_at timestamp
) AS $$
BEGIN
	RETURN QUERY (
		SELECT *
		FROM Customers
		ORDER BY dob asc
		LIMIT n
	);
END;
$$ LANGUAGE plpgsql;


