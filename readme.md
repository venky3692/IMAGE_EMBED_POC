## To run oracle db docker:
```
docker pull container-registry.oracle.com/database/express:latest
docker run \
-it --name oracledb \
-p 1521:1521 -p 5500:5500 \
-e ORACLE_PDB=TESTDB \
-e ORACLE_PWD=Password1! \
-v oracledata:/opt/oracle/oradata \
container-registry.oracle.com/database/express:latest
```

## Once the above db is setup
```
get inside docker container: sudo docker exec -it <docker-id> bash
connect to db cli: sqlplus sys/Password1!@sys as sysdba

Run below commands
CREATE TABLE images (
    id NUMBER GENERATED ALWAYS AS IDENTITY,
    image_data BLOB,
    image_name VARCHAR2(255),
    CONSTRAINT image_pk PRIMARY KEY (image_id)
);
CREATE USER imageUser IDENTIFIED BY imageUser123;
GRANT CONNECT TO imageUser;
GRANT SELECT, INSERT, UPDATE, DELETE ON images TO imageUser;
```