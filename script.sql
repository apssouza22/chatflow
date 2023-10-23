CREATE TABLE apps (
    id serial primary key NOT NULL,
    user_ref integer NOT NULL,
    app_name character varying(100) NOT NULL,
    app_description text NOT NULL,
    app_key character varying(50) NOT NULL,
    app_model character varying(50) NOT NULL,
    app_temperature double precision NOT NULL
);

CREATE TABLE chat_messages (
    id serial primary key NOT NULL,
    user_ref integer NOT NULL,
    chatbot_id character varying(50) NOT NULL,
    message text NOT NULL,
    is_bot_reply boolean NOT NULL,
    createdat timestamp without time zone DEFAULT now() NOT NULL
);

CREATE TABLE users (
    id serial primary key NOT NULL,
    email character varying(250) NOT NULL,
    password character varying(200) NOT NULL,
    name character varying(50) NOT NULL
);

ALTER TABLE ONLY apps
    ADD CONSTRAINT _app_key_unique UNIQUE (user_ref, app_key);

ALTER TABLE ONLY apps
    ADD CONSTRAINT _app_name_unique UNIQUE (user_ref, app_name);

ALTER TABLE ONLY users
    ADD CONSTRAINT users_email_key UNIQUE (email);

CREATE INDEX ix_chat_messages_createdat ON chat_messages USING btree (createdat);

ALTER TABLE ONLY apps
    ADD CONSTRAINT apps_user_ref_fkey FOREIGN KEY (user_ref) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY chat_messages
    ADD CONSTRAINT chat_messages_user_ref_fkey FOREIGN KEY (user_ref) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;
