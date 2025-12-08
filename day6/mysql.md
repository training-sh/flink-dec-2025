
```
USE ecommerce;
```

-- detect insert/update changes using timestamp , but HARD delete

```
create table initial_products (id int, 
                       name varchar(255), 
                       price int, 
                       create_ts timestamp DEFAULT CURRENT_TIMESTAMP, 
                       update_ts timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP );
                       
             
```

dont' insert all, go step by step per trainer 

```
insert into initial_products (id, name,price) values(1, 'product1', 100);
insert into initial_products (id, name,price) values(2, 'product2', 200);
insert into initial_products (id, name,price) values(3, 'product3', 300);
insert into initial_products (id, name,price) values(4, 'product4', 400);
```
