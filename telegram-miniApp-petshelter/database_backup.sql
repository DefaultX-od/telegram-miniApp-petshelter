CREATE FUNCTION public.add_pet(_type character varying, _status character varying, _name character varying, _sex character varying, _age integer, _fertility character varying, _id_album character varying, _description text) RETURNS void
    LANGUAGE sql
    AS $$
	INSERT INTO pets( id_pet, id_type, id_status, name, sex, fertility, description, id_album, age)
	VALUES(
		nextval('pets_id_pet_seq'::regclass),
		(SELECT id_type from pet_type pt WHERE pt.name = _type),
		(SELECT id_status from pet_status ps WHERE ps.name = _status),
		_name,
		_sex,
		CASE
            WHEN _fertility = 'Да' THEN TRUE::bool
            WHEN _fertility = 'Нет' THEN FALSE::bool
        END,
		_description,
		_id_album,
		_age
	);
$$;

CREATE FUNCTION public.add_pet_to_favorites(_id_pet bigint, _id_user double precision) RETURNS void
    LANGUAGE sql
    AS $$
	INSERT INTO pets_favorites (id_pet, id_user) VALUES (_id_pet, _id_user);
$$;

CREATE FUNCTION public.cancel_application(_id_aplication bigint) RETURNS void
    LANGUAGE sql
    AS $$
	UPDATE aplications SET id_status = 6 WHERE id_aplication = _id_aplication;
	UPDATE pets p SET id_status = 1 FROM aplications a WHERE p.id_pet = a.id_pet AND a.id_aplication = _id_aplication;
$$;

CREATE FUNCTION public.create_application(_id_pet bigint, _id_user double precision) RETURNS void
    LANGUAGE sql
    AS $$
	INSERT INTO aplications (id_aplication, id_status, id_user, id_pet, stage)
	VALUES (
	nextval('aplications_id_aplication_seq'::regclass),
	1,
	_id_user,
	_id_pet,
	1	
	);
$$;

CREATE FUNCTION public.get_aplications(_id_user double precision) RETURNS TABLE(id bigint, id_type bigint, name character varying, age integer, sex character varying, fertility character varying, album_link character varying, type character varying, pet_status character varying, description text, id_aplication bigint, aplication_status character varying, aplication_description character varying, stage integer)
    LANGUAGE sql
    AS $$
	select 
		p.id_pet,
		p.id_type,
		p.name,
		p.age,
		p.sex,
		CASE
            WHEN p.fertility = TRUE THEN 'Да'::text
            WHEN p.fertility = FALSE THEN 'Нет'::text
            ELSE 'ошибка'::text
        END AS "fertility",
		p.id_album,
		pt.name,
		ps.name,
		p.description,
		a.id_aplication,
		ast.name,
		ast.description,
		a.stage
	FROM pets p 
	JOIN pet_type pt ON p.id_type = pt.id_type
	JOIN pet_status ps ON p.id_status = ps.id_status
	JOIN aplications a ON p.id_pet = a.id_pet AND a.id_user = _id_user
	JOIN aplication_status ast ON ast.id_status = a.id_status
	WHERE a.id_status != 6
$$;

CREATE FUNCTION public.get_application_bot(_id_application integer) RETURNS TABLE(id_application bigint, id_pet bigint, id_user double precision, pet_name character varying, pet_age integer, pet_sex character varying, album_link character varying, stage integer)
    LANGUAGE sql
    AS $$
	select 
		a.id_aplication,
		p.id_pet,
		a.id_user,
		p.name,
		p.age,
		p.sex,
		('https://imgur.com/a/'||p.id_album)::varchar as album_link,
		a.stage
	FROM aplications a join pets p on a.id_pet = p.id_pet
	where a.id_aplication = _id_application;
$$;

CREATE FUNCTION public.get_applications_bot(_stage integer) RETURNS TABLE(id_application bigint)
    LANGUAGE sql
    AS $$
	SELECT id_aplication from aplications where stage = _stage and id_status != 6;
$$;

CREATE FUNCTION public.get_fav_pets(_id_user double precision) RETURNS TABLE(id bigint, id_type bigint, name character varying, age integer, sex character varying, fertility character varying, album_link character varying, type character varying, status character varying, description text)
    LANGUAGE sql
    AS $$
	select 
		p.id_pet,
		p.id_type,
		p.name,
		p.age,
		p.sex,
		CASE
            WHEN p.fertility = TRUE THEN 'Да'::text
            WHEN p.fertility = FALSE THEN 'Нет'::text
            ELSE 'ошибка'::text
        END AS "fertility",
		p.id_album,
		pt.name,
		ps.name,
		p.description
	FROM pets p JOIN pet_type pt ON p.id_type = pt.id_type JOIN pet_status ps on p.id_status = ps.id_status
			JOIN pets_favorites pf ON p.id_pet=pf.id_pet
	WHERE pf.id_user=_id_user;
$$;

CREATE FUNCTION public.get_pet(_id bigint) RETURNS TABLE(id bigint, id_type bigint, name character varying, age integer, sex character varying, fertility character varying, description text, album_link text)
    LANGUAGE sql
    AS $$
	select id_pet,
		id_type,
		name,
		age,
		sex,
		CASE
            WHEN fertility = TRUE THEN 'не кастрирован'::text
            WHEN fertility = FALSE THEN 'кастрирован'::text
            ELSE 'ошибка'::text
        END AS "fertility",
		description,
		id_album,
		id_status
	from pets where id_pet = _id;
$$;

CREATE FUNCTION public.get_pet_statuses() RETURNS TABLE(pet_status character varying)
    LANGUAGE sql
    AS $$
	select name from pet_status;
$$;

CREATE FUNCTION public.get_pet_types() RETURNS TABLE(pet_type character varying)
    LANGUAGE sql
    AS $$
	select name from pet_type;
$$;

CREATE FUNCTION public.get_pets() RETURNS TABLE(id bigint, id_type bigint, name character varying, age integer, sex character varying, fertility character varying, album_link character varying, type character varying, status character varying, description text)
    LANGUAGE sql
    AS $$
	select id_pet,
		p.id_type,
		p.name,
		p.age,
		p.sex,
		CASE
            WHEN p.fertility = TRUE THEN 'Да'::text
            WHEN p.fertility = FALSE THEN 'Нет'::text
            ELSE 'ошибка'::text
        END AS "fertility",
		p.id_album,
		pt.name,
		ps.name,
		p.description
	FROM pets p JOIN pet_type pt ON p.id_type = pt.id_type JOIN pet_status ps on p.id_status = ps.id_status
	where p.id_status !=2;
$$;

CREATE FUNCTION public.get_pets(_id_type bigint) RETURNS TABLE(id bigint, id_type bigint, name character varying, age integer, sex character varying, fertility character varying, album_link text)
    LANGUAGE sql
    AS $$
	select id_pet,
		id_type,
		name,
		age,
		sex,
		CASE
            WHEN fertility = TRUE THEN 'Да'::text
            WHEN fertility = FALSE THEN 'Нет'::text
            ELSE 'ошибка'::text
        END AS "fertility",
		id_album
	from pets where id_type=_id_type and id_status !=2;
$$;

CREATE FUNCTION public.is_on_favorites(_id_pet bigint, _id_user double precision) RETURNS bigint
    LANGUAGE sql
    AS $$
	SELECT COUNT(*) FROM pets_favorites WHERE _id_pet = id_pet AND _id_user = id_user;
$$;

CREATE FUNCTION public.is_there_application(_id_pet bigint, _id_user double precision) RETURNS bigint
    LANGUAGE sql
    AS $$
	SELECT COUNT(*) FROM aplications WHERE _id_pet = id_pet AND _id_user = id_user AND id_status NOT IN (5, 6);
$$;

CREATE FUNCTION public.remove_pet_from_favorites(_id_pet bigint, _id_user double precision) RETURNS void
    LANGUAGE sql
    AS $$
	DELETE FROM pets_favorites where id_pet=_id_pet AND id_user=_id_user;
$$;

CREATE FUNCTION public.update_application_stage(_id_application bigint, _stage integer, _id_applicattion_status bigint, _id_pet_status bigint) RETURNS void
    LANGUAGE sql
    AS $$
	UPDATE aplications SET stage = _stage, id_status = _id_applicattion_status WHERE id_aplication = _id_application;
	UPDATE pets p SET id_status = _id_pet_status FROM aplications a WHERE p.id_pet = a.id_pet AND a.id_aplication = _id_application;
	UPDATE aplications SET id_status = 5 WHERE id_aplication != _id_application AND id_status != 6
  	AND id_pet = (SELECT id_pet FROM aplications WHERE id_aplication = _id_application);
$$;

CREATE FUNCTION public.update_pet(_id bigint, _type character varying, _status character varying, _name character varying, _sex character varying, _age integer, _id_album character varying, _fertility character varying, _description text) RETURNS void
    LANGUAGE sql
    AS $$
	
	UPDATE pets
	SET
		id_type = (SELECT id_type from pet_type where name=_type),
		id_status = (SELECT id_status from pet_status where name = _status),
		name = _name,
		sex = _sex,
		id_album = _id_album,
		age = _age,
		fertility = (
			CASE
            	WHEN _fertility = 'Да' THEN TRUE::bool
            	WHEN _fertility = 'Нет' THEN FALSE::bool
        END
		),
		description = _description
	WHERE id_pet = _id;

$$;

SET default_tablespace = '';

SET default_table_access_method = heap;

CREATE TABLE public.aplication_status (
    id_status bigint NOT NULL,
    name character varying(255) NOT NULL,
    description character varying(255) NOT NULL
);

CREATE SEQUENCE public.aplication_status_id_status_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.aplications (
    id_aplication bigint NOT NULL,
    id_status bigint NOT NULL,
    id_user double precision NOT NULL,
    id_pet bigint NOT NULL,
    stage integer NOT NULL
);

CREATE SEQUENCE public.aplications_id_aplication_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.pet_status (
    id_status bigint NOT NULL,
    name character varying(255) NOT NULL,
    description character varying(255) NOT NULL
);

CREATE SEQUENCE public.pet_status_id_status_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.pet_type (
    id_type bigint NOT NULL,
    name character varying(255) NOT NULL,
    description character varying(255)
);

CREATE SEQUENCE public.pet_type_id_type_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.pets (
    id_pet bigint NOT NULL,
    id_type bigint NOT NULL,
    id_status bigint NOT NULL,
    name character varying(255) NOT NULL,
    sex character varying(255) NOT NULL,
    fertility boolean NOT NULL,
    description text NOT NULL,
    id_album character varying,
    age integer
);

CREATE TABLE public.pets_favorites (
    id_pet bigint NOT NULL,
    id_user double precision NOT NULL
);

CREATE SEQUENCE public.pets_id_pet_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ONLY public.aplication_status ALTER COLUMN id_status SET DEFAULT nextval('public.aplication_status_id_status_seq'::regclass);

ALTER TABLE ONLY public.aplications ALTER COLUMN id_aplication SET DEFAULT nextval('public.aplications_id_aplication_seq'::regclass);

ALTER TABLE ONLY public.pet_status ALTER COLUMN id_status SET DEFAULT nextval('public.pet_status_id_status_seq'::regclass);

ALTER TABLE ONLY public.pet_type ALTER COLUMN id_type SET DEFAULT nextval('public.pet_type_id_type_seq'::regclass);

ALTER TABLE ONLY public.pets ALTER COLUMN id_pet SET DEFAULT nextval('public.pets_id_pet_seq'::regclass);

COPY public.aplication_status (id_status, name, description) FROM stdin;
1	Ожидание	Администратор, еще не приступил к обработке заявки.
2	В работе	Администратор начал обрабатывать заявку.
3	Истекла	Заявка не была заверщена в указынный срок.
4	Одобрена	Администратор одобрил заявку.
5	Отклонена	Администратор отклонил заявку.
6	Отменена	Отменена пользователем.
\.

COPY public.pet_status (id_status, name, description) FROM stdin;
1	В поиске	Ищет хозяина
2	Не в поиске	Не ищет хозяина
\.

COPY public.pet_type (id_type, name, description) FROM stdin;
3	Собака	\N
2	Кошка	\N
\.

SELECT pg_catalog.setval('public.aplication_status_id_status_seq', 6, true);

SELECT pg_catalog.setval('public.pet_status_id_status_seq', 2, true);

SELECT pg_catalog.setval('public.pet_type_id_type_seq', 3, true);

ALTER TABLE ONLY public.aplication_status
    ADD CONSTRAINT aplication_status_pkey PRIMARY KEY (id_status);

ALTER TABLE ONLY public.aplications
    ADD CONSTRAINT aplications_pkey PRIMARY KEY (id_aplication);

ALTER TABLE ONLY public.pet_status
    ADD CONSTRAINT pet_status_pkey PRIMARY KEY (id_status);

ALTER TABLE ONLY public.pet_type
    ADD CONSTRAINT pet_type_pkey PRIMARY KEY (id_type);

ALTER TABLE ONLY public.pets_favorites
    ADD CONSTRAINT pets_favorites_pk PRIMARY KEY (id_pet, id_user);

ALTER TABLE ONLY public.pets
    ADD CONSTRAINT pets_pkey PRIMARY KEY (id_pet);

ALTER TABLE ONLY public.aplications
    ADD CONSTRAINT aplications_id_pet_foreign FOREIGN KEY (id_pet) REFERENCES public.pets(id_pet);

ALTER TABLE ONLY public.aplications
    ADD CONSTRAINT aplications_id_status_foreign FOREIGN KEY (id_status) REFERENCES public.aplication_status(id_status);

ALTER TABLE ONLY public.pets_favorites
    ADD CONSTRAINT pets_favorites_pets_fk FOREIGN KEY (id_pet) REFERENCES public.pets(id_pet);

ALTER TABLE ONLY public.pets
    ADD CONSTRAINT pets_id_status_foreign FOREIGN KEY (id_status) REFERENCES public.pet_status(id_status);

ALTER TABLE ONLY public.pets
    ADD CONSTRAINT pets_id_type_foreign FOREIGN KEY (id_type) REFERENCES public.pet_type(id_type);

