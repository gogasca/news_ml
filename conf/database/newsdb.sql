--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.15
-- Dumped by pg_dump version 12.0

-- Started on 2019-10-31 00:21:33 PDT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2778 (class 1262 OID 16410)
-- Name: newsml; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE newsml WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF8' LC_CTYPE = 'en_US.UTF8';


ALTER DATABASE newsml OWNER TO postgres;

\connect newsml

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: newsml
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO newsml;

--
-- TOC entry 2780 (class 0 OID 0)
-- Dependencies: 3
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: newsml
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

--
-- TOC entry 193 (class 1259 OID 16473)
-- Name: api_users; Type: TABLE; Schema: public; Owner: newsml
--

CREATE TABLE public.api_users (
    id integer NOT NULL,
    username character varying(256) NOT NULL,
    password_hash character varying(256) NOT NULL,
    created timestamp(6) with time zone
);


ALTER TABLE public.api_users OWNER TO newsml;

--
-- TOC entry 192 (class 1259 OID 16471)
-- Name: api_users_id_seq; Type: SEQUENCE; Schema: public; Owner: newsml
--

CREATE SEQUENCE public.api_users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.api_users_id_seq OWNER TO newsml;

--
-- TOC entry 2783 (class 0 OID 0)
-- Dependencies: 192
-- Name: api_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: newsml
--

ALTER SEQUENCE public.api_users_id_seq OWNED BY public.api_users.id;


--
-- TOC entry 195 (class 1259 OID 16486)
-- Name: campaign; Type: TABLE; Schema: public; Owner: newsml
--

CREATE TABLE public.campaign (
    id integer NOT NULL,
    description character varying(256),
    reference character varying(32) NOT NULL,
    campaign_start timestamp(6) without time zone,
    campaign_end timestamp(6) without time zone,
    is_cancelled boolean DEFAULT false,
    status integer DEFAULT 0,
    request_data character varying(4096),
    provider character varying(256),
    report boolean DEFAULT false,
    is_test boolean DEFAULT false,
    articles integer
);


ALTER TABLE public.campaign OWNER TO newsml;

--
-- TOC entry 194 (class 1259 OID 16484)
-- Name: campaign_id_seq; Type: SEQUENCE; Schema: public; Owner: newsml
--

CREATE SEQUENCE public.campaign_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.campaign_id_seq OWNER TO newsml;

--
-- TOC entry 2785 (class 0 OID 0)
-- Dependencies: 194
-- Name: campaign_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: newsml
--

ALTER SEQUENCE public.campaign_id_seq OWNED BY public.campaign.id;


--
-- TOC entry 188 (class 1259 OID 16454)
-- Name: companies; Type: TABLE; Schema: public; Owner: newsml
--

CREATE TABLE public.companies (
    company_id integer NOT NULL,
    name character varying(64) NOT NULL,
    mention_date time(6) with time zone
);


ALTER TABLE public.companies OWNER TO newsml;

--
-- TOC entry 187 (class 1259 OID 16452)
-- Name: companies_company_id_seq; Type: SEQUENCE; Schema: public; Owner: newsml
--

CREATE SEQUENCE public.companies_company_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_company_id_seq OWNER TO newsml;

--
-- TOC entry 2787 (class 0 OID 0)
-- Dependencies: 187
-- Name: companies_company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: newsml
--

ALTER SEQUENCE public.companies_company_id_seq OWNED BY public.companies.company_id;


--
-- TOC entry 186 (class 1259 OID 16443)
-- Name: news; Type: TABLE; Schema: public; Owner: newsml
--

CREATE TABLE public.news (
    news_id integer NOT NULL,
    author character varying(128),
    source character varying(64),
    source_id character varying(64),
    title character varying(256) NOT NULL,
    description character varying(65536) NOT NULL,
    url character varying(512),
    url_to_image character varying(512),
    published_at date,
    content character varying(65536),
    campaign character varying(16),
    score double precision,
    magnitude double precision,
    sentiment character varying(16),
    rank_score double precision,
    rank_order integer,
    translated_content character varying(65536),
    detected_language character varying(128),
    inserted_at time without time zone
);


ALTER TABLE public.news OWNER TO newsml;

--
-- TOC entry 185 (class 1259 OID 16441)
-- Name: news_news_id_seq; Type: SEQUENCE; Schema: public; Owner: newsml
--

CREATE SEQUENCE public.news_news_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.news_news_id_seq OWNER TO newsml;

--
-- TOC entry 2789 (class 0 OID 0)
-- Dependencies: 185
-- Name: news_news_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: newsml
--

ALTER SEQUENCE public.news_news_id_seq OWNED BY public.news.news_id;


--
-- TOC entry 197 (class 1259 OID 16524)
-- Name: persons; Type: TABLE; Schema: public; Owner: newsml
--

CREATE TABLE public.persons (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    mention_date timestamp(6) with time zone,
    valid boolean DEFAULT true
);


ALTER TABLE public.persons OWNER TO newsml;

--
-- TOC entry 196 (class 1259 OID 16522)
-- Name: persons_id_seq; Type: SEQUENCE; Schema: public; Owner: newsml
--

CREATE SEQUENCE public.persons_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.persons_id_seq OWNER TO newsml;

--
-- TOC entry 2791 (class 0 OID 0)
-- Dependencies: 196
-- Name: persons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: newsml
--

ALTER SEQUENCE public.persons_id_seq OWNED BY public.persons.id;


--
-- TOC entry 190 (class 1259 OID 16462)
-- Name: tags; Type: TABLE; Schema: public; Owner: newsml
--

CREATE TABLE public.tags (
    tag_id integer NOT NULL,
    tag_name character varying(128) NOT NULL
);


ALTER TABLE public.tags OWNER TO newsml;

--
-- TOC entry 191 (class 1259 OID 16468)
-- Name: tags_news; Type: TABLE; Schema: public; Owner: newsml
--

CREATE TABLE public.tags_news (
    tag_id bigint,
    news_id bigint
);


ALTER TABLE public.tags_news OWNER TO newsml;

--
-- TOC entry 189 (class 1259 OID 16460)
-- Name: tags_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: newsml
--

CREATE SEQUENCE public.tags_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tags_tag_id_seq OWNER TO newsml;

--
-- TOC entry 2794 (class 0 OID 0)
-- Dependencies: 189
-- Name: tags_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: newsml
--

ALTER SEQUENCE public.tags_tag_id_seq OWNED BY public.tags.tag_id;


--
-- TOC entry 2634 (class 2604 OID 16476)
-- Name: api_users id; Type: DEFAULT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.api_users ALTER COLUMN id SET DEFAULT nextval('public.api_users_id_seq'::regclass);


--
-- TOC entry 2635 (class 2604 OID 16489)
-- Name: campaign id; Type: DEFAULT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.campaign ALTER COLUMN id SET DEFAULT nextval('public.campaign_id_seq'::regclass);


--
-- TOC entry 2632 (class 2604 OID 16457)
-- Name: companies company_id; Type: DEFAULT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.companies ALTER COLUMN company_id SET DEFAULT nextval('public.companies_company_id_seq'::regclass);


--
-- TOC entry 2631 (class 2604 OID 16446)
-- Name: news news_id; Type: DEFAULT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.news ALTER COLUMN news_id SET DEFAULT nextval('public.news_news_id_seq'::regclass);


--
-- TOC entry 2640 (class 2604 OID 16527)
-- Name: persons id; Type: DEFAULT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.persons ALTER COLUMN id SET DEFAULT nextval('public.persons_id_seq'::regclass);


--
-- TOC entry 2633 (class 2604 OID 16465)
-- Name: tags tag_id; Type: DEFAULT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.tags ALTER COLUMN tag_id SET DEFAULT nextval('public.tags_tag_id_seq'::regclass);


--
-- TOC entry 2649 (class 2606 OID 16481)
-- Name: api_users api_users_pkey; Type: CONSTRAINT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.api_users
    ADD CONSTRAINT api_users_pkey PRIMARY KEY (id);


--
-- TOC entry 2651 (class 2606 OID 16483)
-- Name: api_users api_users_username_key; Type: CONSTRAINT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.api_users
    ADD CONSTRAINT api_users_username_key UNIQUE (username);


--
-- TOC entry 2653 (class 2606 OID 16491)
-- Name: campaign campaign_pkey; Type: CONSTRAINT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.campaign
    ADD CONSTRAINT campaign_pkey PRIMARY KEY (id);


--
-- TOC entry 2645 (class 2606 OID 16459)
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (company_id);


--
-- TOC entry 2643 (class 2606 OID 16451)
-- Name: news news_pkey; Type: CONSTRAINT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.news
    ADD CONSTRAINT news_pkey PRIMARY KEY (news_id);


--
-- TOC entry 2655 (class 2606 OID 16529)
-- Name: persons persons_pkey; Type: CONSTRAINT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (id);


--
-- TOC entry 2647 (class 2606 OID 16467)
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (tag_id);


--
-- TOC entry 2779 (class 0 OID 0)
-- Dependencies: 2778
-- Name: DATABASE newsml; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON DATABASE newsml TO newsml;


--
-- TOC entry 2781 (class 0 OID 0)
-- Dependencies: 3
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: newsml
--

REVOKE ALL ON SCHEMA public FROM cloudsqladmin;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;
GRANT ALL ON SCHEMA public TO newsml WITH GRANT OPTION;


--
-- TOC entry 2782 (class 0 OID 0)
-- Dependencies: 193
-- Name: TABLE api_users; Type: ACL; Schema: public; Owner: newsml
--

REVOKE ALL ON TABLE public.api_users FROM newsml;
GRANT ALL ON TABLE public.api_users TO newsml WITH GRANT OPTION;


--
-- TOC entry 2784 (class 0 OID 0)
-- Dependencies: 195
-- Name: TABLE campaign; Type: ACL; Schema: public; Owner: newsml
--

REVOKE ALL ON TABLE public.campaign FROM newsml;
GRANT ALL ON TABLE public.campaign TO newsml WITH GRANT OPTION;


--
-- TOC entry 2786 (class 0 OID 0)
-- Dependencies: 188
-- Name: TABLE companies; Type: ACL; Schema: public; Owner: newsml
--

REVOKE ALL ON TABLE public.companies FROM newsml;
GRANT ALL ON TABLE public.companies TO newsml WITH GRANT OPTION;


--
-- TOC entry 2788 (class 0 OID 0)
-- Dependencies: 186
-- Name: TABLE news; Type: ACL; Schema: public; Owner: newsml
--

REVOKE ALL ON TABLE public.news FROM newsml;
GRANT ALL ON TABLE public.news TO newsml WITH GRANT OPTION;


--
-- TOC entry 2790 (class 0 OID 0)
-- Dependencies: 197
-- Name: TABLE persons; Type: ACL; Schema: public; Owner: newsml
--

REVOKE ALL ON TABLE public.persons FROM newsml;
GRANT ALL ON TABLE public.persons TO newsml WITH GRANT OPTION;


--
-- TOC entry 2792 (class 0 OID 0)
-- Dependencies: 190
-- Name: TABLE tags; Type: ACL; Schema: public; Owner: newsml
--

REVOKE ALL ON TABLE public.tags FROM newsml;
GRANT ALL ON TABLE public.tags TO newsml WITH GRANT OPTION;


--
-- TOC entry 2793 (class 0 OID 0)
-- Dependencies: 191
-- Name: TABLE tags_news; Type: ACL; Schema: public; Owner: newsml
--

REVOKE ALL ON TABLE public.tags_news FROM newsml;
GRANT ALL ON TABLE public.tags_news TO newsml WITH GRANT OPTION;


-- Completed on 2019-10-31 00:21:40 PDT

--
-- PostgreSQL database dump complete
--

