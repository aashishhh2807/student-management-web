-- this is a record of how your database is created 

create database student_db;
use student_db;

create table student_details(
	id INT Auto_increment primary key,
    name varchar(20) not null,
    age int,
    dept varchar(20),
    email varchar(100)
);