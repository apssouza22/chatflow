

create table chat_messages
(
    id           serial
        primary key,
    user_id      varchar(250),
    chatbot_id   varchar(50),
    message      text,
    is_bot_reply boolean,
    createdat    timestamp default (now() AT TIME ZONE 'UTC'::text)
);

alter table chat_messages
    owner to chatux;

create index idx_timestamp
    on chat_messages (createdat);

create index idx_chatbot_id
    on chat_messages (chatbot_id);

create index idx_user_id
    on chat_messages (user_id);

