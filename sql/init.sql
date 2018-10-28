--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.14
-- Dumped by pg_dump version 9.5.14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: messenger; Type: SCHEMA; Schema: -; Owner: fenya
--

CREATE SCHEMA messenger;


ALTER SCHEMA messenger OWNER TO fenya;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: attachments; Type: TABLE; Schema: messenger; Owner: postgres
--

CREATE TABLE messenger.attachments (
    attach_id integer NOT NULL,
    chat_id integer NOT NULL,
    user_id integer NOT NULL,
    message_id integer NOT NULL,
    type text NOT NULL,
    url text NOT NULL,
    CONSTRAINT attachment_type_check CHECK ((length(type) < 16)),
    CONSTRAINT attachment_url_check CHECK ((length(url) < 64))
);


ALTER TABLE messenger.attachments OWNER TO postgres;

--
-- Name: attachments_attach_id_seq; Type: SEQUENCE; Schema: messenger; Owner: postgres
--

CREATE SEQUENCE messenger.attachments_attach_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE messenger.attachments_attach_id_seq OWNER TO postgres;

--
-- Name: attachments_attach_id_seq; Type: SEQUENCE OWNED BY; Schema: messenger; Owner: postgres
--

ALTER SEQUENCE messenger.attachments_attach_id_seq OWNED BY messenger.attachments.attach_id;


--
-- Name: chats; Type: TABLE; Schema: messenger; Owner: postgres
--

CREATE TABLE messenger.chats (
    chat_id integer NOT NULL,
    is_group_chat boolean NOT NULL,
    topic text DEFAULT ''::text NOT NULL,
    last_message text NOT NULL,
    CONSTRAINT chat_last_message_check CHECK ((length(last_message) < 65536)),
    CONSTRAINT chat_topic_check CHECK ((length(topic) < 100))
);


ALTER TABLE messenger.chats OWNER TO postgres;

--
-- Name: chats_chat_id_seq; Type: SEQUENCE; Schema: messenger; Owner: postgres
--

CREATE SEQUENCE messenger.chats_chat_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE messenger.chats_chat_id_seq OWNER TO postgres;

--
-- Name: chats_chat_id_seq; Type: SEQUENCE OWNED BY; Schema: messenger; Owner: postgres
--

ALTER SEQUENCE messenger.chats_chat_id_seq OWNED BY messenger.chats.chat_id;


--
-- Name: members; Type: TABLE; Schema: messenger; Owner: postgres
--

CREATE TABLE messenger.members (
    member_id integer NOT NULL,
    user_id integer NOT NULL,
    chat_id integer NOT NULL,
    new_messages integer NOT NULL,
    last_read_message_id integer NOT NULL
);


ALTER TABLE messenger.members OWNER TO postgres;

--
-- Name: members_member_id_seq; Type: SEQUENCE; Schema: messenger; Owner: postgres
--

CREATE SEQUENCE messenger.members_member_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE messenger.members_member_id_seq OWNER TO postgres;

--
-- Name: members_member_id_seq; Type: SEQUENCE OWNED BY; Schema: messenger; Owner: postgres
--

ALTER SEQUENCE messenger.members_member_id_seq OWNED BY messenger.members.member_id;


--
-- Name: messages; Type: TABLE; Schema: messenger; Owner: postgres
--

CREATE TABLE messenger.messages (
    message_id integer NOT NULL,
    user_id integer NOT NULL,
    chat_id integer NOT NULL,
    content text NOT NULL,
    added_at timestamp without time zone DEFAULT now() NOT NULL,
    CONSTRAINT message_content_check CHECK ((length(content) < 65536))
);


ALTER TABLE messenger.messages OWNER TO postgres;

--
-- Name: messages_message_id_seq; Type: SEQUENCE; Schema: messenger; Owner: postgres
--

CREATE SEQUENCE messenger.messages_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE messenger.messages_message_id_seq OWNER TO postgres;

--
-- Name: messages_message_id_seq; Type: SEQUENCE OWNED BY; Schema: messenger; Owner: postgres
--

ALTER SEQUENCE messenger.messages_message_id_seq OWNED BY messenger.messages.message_id;


--
-- Name: users; Type: TABLE; Schema: messenger; Owner: postgres
--

CREATE TABLE messenger.users (
    user_id integer NOT NULL,
    nick text NOT NULL,
    name text NOT NULL,
    avatar text DEFAULT ''::text NOT NULL,
    CONSTRAINT user_avatar_check CHECK ((length(avatar) < 100)),
    CONSTRAINT user_name_check CHECK ((length(name) < 64)),
    CONSTRAINT user_nick_check CHECK ((length(nick) < 32))
);


ALTER TABLE messenger.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: messenger; Owner: postgres
--

CREATE SEQUENCE messenger.users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE messenger.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: messenger; Owner: postgres
--

ALTER SEQUENCE messenger.users_user_id_seq OWNED BY messenger.users.user_id;


--
-- Name: attach_id; Type: DEFAULT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.attachments ALTER COLUMN attach_id SET DEFAULT nextval('messenger.attachments_attach_id_seq'::regclass);


--
-- Name: chat_id; Type: DEFAULT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.chats ALTER COLUMN chat_id SET DEFAULT nextval('messenger.chats_chat_id_seq'::regclass);


--
-- Name: member_id; Type: DEFAULT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.members ALTER COLUMN member_id SET DEFAULT nextval('messenger.members_member_id_seq'::regclass);


--
-- Name: message_id; Type: DEFAULT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.messages ALTER COLUMN message_id SET DEFAULT nextval('messenger.messages_message_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.users ALTER COLUMN user_id SET DEFAULT nextval('messenger.users_user_id_seq'::regclass);


--
-- Data for Name: attachments; Type: TABLE DATA; Schema: messenger; Owner: postgres
--

COPY messenger.attachments (attach_id, chat_id, user_id, message_id, type, url) FROM stdin;
\.


--
-- Name: attachments_attach_id_seq; Type: SEQUENCE SET; Schema: messenger; Owner: postgres
--

SELECT pg_catalog.setval('messenger.attachments_attach_id_seq', 1, false);


--
-- Data for Name: chats; Type: TABLE DATA; Schema: messenger; Owner: postgres
--

COPY messenger.chats (chat_id, is_group_chat, topic, last_message) FROM stdin;
\.


--
-- Name: chats_chat_id_seq; Type: SEQUENCE SET; Schema: messenger; Owner: postgres
--

SELECT pg_catalog.setval('messenger.chats_chat_id_seq', 1, false);


--
-- Data for Name: members; Type: TABLE DATA; Schema: messenger; Owner: postgres
--

COPY messenger.members (member_id, user_id, chat_id, new_messages, last_read_message_id) FROM stdin;
\.


--
-- Name: members_member_id_seq; Type: SEQUENCE SET; Schema: messenger; Owner: postgres
--

SELECT pg_catalog.setval('messenger.members_member_id_seq', 1, false);


--
-- Data for Name: messages; Type: TABLE DATA; Schema: messenger; Owner: postgres
--

COPY messenger.messages (message_id, user_id, chat_id, content, added_at) FROM stdin;
\.


--
-- Name: messages_message_id_seq; Type: SEQUENCE SET; Schema: messenger; Owner: postgres
--

SELECT pg_catalog.setval('messenger.messages_message_id_seq', 1, false);


--
-- Data for Name: users; Type: TABLE DATA; Schema: messenger; Owner: postgres
--

COPY messenger.users (user_id, nick, name, avatar) FROM stdin;
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: messenger; Owner: postgres
--

SELECT pg_catalog.setval('messenger.users_user_id_seq', 1, false);


--
-- Name: attachments_pkey; Type: CONSTRAINT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.attachments
    ADD CONSTRAINT attachments_pkey PRIMARY KEY (attach_id);


--
-- Name: chats_pkey; Type: CONSTRAINT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.chats
    ADD CONSTRAINT chats_pkey PRIMARY KEY (chat_id);


--
-- Name: members_pkey; Type: CONSTRAINT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (member_id);


--
-- Name: messages_pkey; Type: CONSTRAINT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (message_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: attachments_chat_id_fkey; Type: FK CONSTRAINT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.attachments
    ADD CONSTRAINT attachments_chat_id_fkey FOREIGN KEY (chat_id) REFERENCES messenger.chats(chat_id);


--
-- Name: attachments_message_id_fkey; Type: FK CONSTRAINT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.attachments
    ADD CONSTRAINT attachments_message_id_fkey FOREIGN KEY (message_id) REFERENCES messenger.messages(message_id);


--
-- Name: attachments_user_id_fkey; Type: FK CONSTRAINT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.attachments
    ADD CONSTRAINT attachments_user_id_fkey FOREIGN KEY (user_id) REFERENCES messenger.users(user_id);


--
-- Name: members_chat_id_fkey; Type: FK CONSTRAINT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.members
    ADD CONSTRAINT members_chat_id_fkey FOREIGN KEY (chat_id) REFERENCES messenger.chats(chat_id);


--
-- Name: members_last_read_message_id_fkey; Type: FK CONSTRAINT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.members
    ADD CONSTRAINT members_last_read_message_id_fkey FOREIGN KEY (last_read_message_id) REFERENCES messenger.messages(message_id);


--
-- Name: members_user_id_fkey; Type: FK CONSTRAINT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.members
    ADD CONSTRAINT members_user_id_fkey FOREIGN KEY (user_id) REFERENCES messenger.users(user_id);


--
-- Name: messages_chat_id_fkey; Type: FK CONSTRAINT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.messages
    ADD CONSTRAINT messages_chat_id_fkey FOREIGN KEY (chat_id) REFERENCES messenger.chats(chat_id);


--
-- Name: messages_user_id_fkey; Type: FK CONSTRAINT; Schema: messenger; Owner: postgres
--

ALTER TABLE ONLY messenger.messages
    ADD CONSTRAINT messages_user_id_fkey FOREIGN KEY (user_id) REFERENCES messenger.users(user_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

