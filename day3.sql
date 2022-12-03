-- Turn on column names
.headers on
.mode column

-- Read input txt file into a table
DROP TABLE IF EXISTS input;
CREATE TABLE input(inline TEXT);
.import day3.txt input

SELECT * FROM input limit 5;

-- New table for left sides
DROP TABLE IF EXISTS column_splits_left;
CREATE TABLE column_splits_left AS
  SELECT
    ROW_NUMBER() OVER() as rn,
    substr(inline, 1, LENGTH(inline)/2) as txt
  FROM input;
SELECT * FROM column_splits_left limit 5;

-- New table for right sides
DROP TABLE IF EXISTS column_splits_right;
CREATE TABLE column_splits_right AS
  SELECT
    ROW_NUMBER() OVER() as rn,
    substr(inline, LENGTH(inline)/2 + 1, LENGTH(inline)/2) as txt
  FROM input;
SELECT * FROM column_splits_right limit 5;

-- Split every character in the left side into a row
DROP TABLE IF EXISTS chars_right;
CREATE TABLE chars_right AS
WITH RECURSIVE
split_left(rn, content, last, rest) AS (
    SELECT
        rn,
        txt,
        substr(txt, 1, 1),
        substr(txt, 2, LENGTH(txt))
    FROM column_splits_left
    UNION ALL
    SELECT
        rn,
        rest,
        substr(rest, 1, 1),
        substr(rest, 2, LENGTH(rest))
    FROM split_left
    WHERE LENGTH(rest) > 0
)
SELECT rn, last as c FROM split_left ORDER BY rn;

-- Split every character in the right side into a row
DROP TABLE IF EXISTS chars_left;
CREATE TABLE chars_left AS
WITH RECURSIVE
split_right(rn, content, last, rest) AS (
    SELECT
        rn,
        txt,
        substr(txt, 1, 1),
        substr(txt, 2, LENGTH(txt))
    FROM column_splits_right
    UNION ALL
    SELECT
        rn,
        rest,
        substr(rest, 1, 1),
        substr(rest, 2, LENGTH(rest))
    FROM split_right
    WHERE LENGTH(rest) > 0
)
SELECT rn, last as c FROM split_right ORDER BY rn;

-- Join the two tables and compute character values
DROP TABLE IF EXISTS matched_chars;
CREATE TABLE matched_chars AS
    SELECT DISTINCT
        chars_left.rn,
        chars_left.c,
        CASE
            WHEN regexp('[a-z]', chars_left.c) THEN unicode(chars_left.c) - unicode('a') + 1
            ELSE unicode(chars_left.c) - unicode('A') + 27
        END as val
        FROM chars_left
        JOIN chars_right
            ON chars_left.rn = chars_right.rn
        WHERE chars_left.c = chars_right.c;

-- Sum the values for part1 answer
SELECT sum(val) FROM matched_chars;

-- Part 2
SELECT "PART 2";

-- Div 3 rn's to get new groups
-- Split every character into a row
DROP TABLE IF EXISTS chars;
CREATE TABLE chars AS
WITH RECURSIVE
split(rn, content, last, rest) AS (
    SELECT
        rn,
        txt,
        substr(txt, 1, 1),
        substr(txt, 2, LENGTH(txt))
    FROM (SELECT ROW_NUMBER() OVER() as rn, inline as txt FROM input)
    UNION ALL
    SELECT
        rn,
        rest,
        substr(rest, 1, 1),
        substr(rest, 2, LENGTH(rest))
    FROM split
    WHERE LENGTH(rest) > 0
)
SELECT rn, (rn - 1) / 3 as grp, (rn - 1) % 3 as mod, last as c FROM split ORDER BY rn;

-- Make table of all 1st rows inside a group
DROP TABLE IF EXISTS chars0;
CREATE TABLE chars0 AS SELECT * FROM chars WHERE mod = 0;

-- Make table of all 2nd rows inside a group
DROP TABLE IF EXISTS chars1;
CREATE TABLE chars1 AS SELECT * FROM chars WHERE mod = 1;

-- Make table of all 3rd rows inside a group
DROP TABLE IF EXISTS chars2;
CREATE TABLE chars2 AS SELECT * FROM chars WHERE mod = 2;

-- Same a part 1, but with 3 tables
DROP TABLE IF EXISTS triple_match_chars;
CREATE TABLE triple_match_chars AS
    SELECT DISTINCT
        chars0.rn,
        chars0.c,
        CASE
            WHEN regexp('[a-z]', chars0.c) THEN unicode(chars0.c) - unicode('a') + 1
            ELSE unicode(chars0.c) - unicode('A') + 27
        END as val
        FROM chars0
        JOIN chars1
            ON chars0.grp = chars1.grp
        JOIN chars2
            ON chars0.grp = chars2.grp
        WHERE chars0.c = chars1.c
        AND chars0.c = chars2.c;

-- Sum the values for part2 answer
SELECT sum(val) from triple_match_chars;