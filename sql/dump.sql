create database db
	with owner fenya
;

create sequence users_user_id_seq
;

alter sequence users_user_id_seq owner to postgres
;

create sequence chats_chat_id_seq
;

alter sequence chats_chat_id_seq owner to postgres
;

create sequence messages_message_id_seq
;

alter sequence messages_message_id_seq owner to postgres
;

create sequence members_member_id_seq
;

alter sequence members_member_id_seq owner to postgres
;

create sequence attachments_attach_id_seq
;

alter sequence attachments_attach_id_seq owner to postgres
;

create table users
(
	user_id serial not null
		constraint users_pkey
			primary key,
	nick text not null
		constraint user_nick_check
			check (length(nick) < 32),
	name text not null
		constraint user_name_check
			check (length(name) < 64),
	avatar text default ''::text not null
		constraint user_avatar_check
			check (length(avatar) < 100)
)
;

alter table users owner to postgres
;

create table chats
(
	chat_id serial not null
		constraint chats_pkey
			primary key,
	is_group_chat boolean not null,
	topic text default ''::text not null
		constraint chat_topic_check
			check (length(topic) < 100),
	last_message text not null
		constraint chat_last_message_check
			check (length(last_message) < 65536)
)
;

alter table chats owner to postgres
;

create table messages
(
	message_id serial not null
		constraint messages_pkey
			primary key,
	user_id integer not null
		constraint messages_user_id_fkey
			references users,
	chat_id integer not null
		constraint messages_chat_id_fkey
			references chats,
	content text not null
		constraint message_content_check
			check (length(content) < 65536),
	added_at timestamp default now() not null
)
;

alter table messages owner to postgres
;

create table members
(
	member_id serial not null
		constraint members_pkey
			primary key,
	user_id integer not null
		constraint members_user_id_fkey
			references users,
	chat_id integer not null
		constraint members_chat_id_fkey
			references chats,
	new_messages integer not null,
	last_read_message_id integer not null
		constraint members_last_read_message_id_fkey
			references messages
)
;

alter table members owner to postgres
;

create table attachments
(
	attach_id serial not null
		constraint attachments_pkey
			primary key,
	chat_id integer not null
		constraint attachments_chat_id_fkey
			references chats,
	user_id integer not null
		constraint attachments_user_id_fkey
			references users,
	message_id integer not null
		constraint attachments_message_id_fkey
			references messages,
	type text not null
		constraint attachment_type_check
			check (length(type) < 16),
	url text not null
		constraint attachment_url_check
			check (length(url) < 64)
)
;

alter table attachments owner to postgres
;