insert into role (name) values ('ADMIN');

insert into user_table (username, email, password) values ('admin', 'admin@email.com', '$2y$10$nKMGYTzYnERShf4hhEI1M.VF.pybMZqFuQ9/pjHstxWYYxIvqSnNS');

insert into user_table_roles (users_id, roles_id) values (1, 1);
