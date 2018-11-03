insert into party (party_id, frat_id, party_desc, type, status, location) values
  (1, 72, 'public', 'open','super cool party', 'here'),
  (2, 56, 'private', 'closed','a lame party', 'also here')
;

insert into rating (rating_id, party_id, user_id, rating, rating_desc) values
  (1, 1, 1, 4.3, 'i liek dis'),
  (2, 2, 2, 2.5, 'prolly dont go')
;

insert into user (user_id, status_type, first_name, last_name, email, passwd, gender, age) values
  (1, 'admin', 'john', 'doe', 'john@gmail.com', 'john123', 'M', 19),
  (2, 'quest', 'jane', 'smith', 'jane@yahoo.com', 'jane123', 'F', 20)
;

insert into invite_lst (invite_lst_id, party_id, user_id) values
  (1, 1, 1),
  (2, 1, 2),
  (3, 2, 1),
  (4, 2, 2)
;
/*
insert into invite (invite_id, invite_desc) values
  (1, 'You are invited!'),
  (2, 'This is an invite')
;
*/
insert into frat (frat_id) values
  (1)
;
