create table users
(
    id       serial primary key,
    email    varchar(250) null,
    password varchar(50) null,
    name     varchar(50) null
);

create table chat_messages
(
    id           serial primary key,
    user_ref     int not null,
    chatbot_id   varchar(50),
    message      text,
    is_bot_reply boolean,
    createdat    timestamp default (now() AT TIME ZONE 'UTC'::text),
    CONSTRAINT fk_user
      FOREIGN KEY(user_ref) 
	  REFERENCES users(id)
);

alter table chat_messages
    owner to chatux;

create index idx_timestamp
    on chat_messages (createdat);

create index idx_chatbot_id
    on chat_messages (chatbot_id);

create index idx_user_email
    on users (email);
