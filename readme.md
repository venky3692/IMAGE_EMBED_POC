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