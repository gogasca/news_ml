--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.15
-- Dumped by pg_dump version 12.0

-- Started on 2019-12-04 21:53:58 PST

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


ALTER SCHEMA public OWNER TO dev_news_ml;

--
-- TOC entry 2792 (class 0 OID 0)
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


ALTER TABLE public.api_users OWNER TO dev_news_ml;

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


ALTER TABLE public.api_users_id_seq OWNER TO dev_news_ml;

--
-- TOC entry 2795 (class 0 OID 0)
-- Dependencies: 192
-- Name: api_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: newsml
--


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


ALTER TABLE public.campaign OWNER TO dev_news_ml;

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


ALTER TABLE public.campaign_id_seq OWNER TO dev_news_ml;

--
-- TOC entry 2797 (class 0 OID 0)
-- Dependencies: 194
-- Name: campaign_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: newsml
--


--
-- TOC entry 188 (class 1259 OID 16454)
-- Name: companies; Type: TABLE; Schema: public; Owner: newsml
--

CREATE TABLE public.companies (
    company_id integer NOT NULL,
    name character varying(1024) NOT NULL,
    mention_date time(6) with time zone
);


ALTER TABLE public.companies OWNER TO dev_news_ml;

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


ALTER TABLE public.companies_company_id_seq OWNER TO dev_news_ml;

--
-- TOC entry 2799 (class 0 OID 0)
-- Dependencies: 187
-- Name: companies_company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: newsml
--


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
    content character varying(65536),
    campaign character varying(16),
    score double precision,
    magnitude double precision,
    sentiment character varying(16),
    rank_score double precision,
    rank_order integer,
    translated_content character varying(65536),
    detected_language character varying(128),
    published_at timestamp with time zone,
    inserted_at timestamp with time zone
);


ALTER TABLE public.news OWNER TO dev_news_ml;

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


ALTER TABLE public.news_news_id_seq OWNER TO dev_news_ml;

--
-- TOC entry 2801 (class 0 OID 0)
-- Dependencies: 185
-- Name: news_news_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: newsml
--


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


ALTER TABLE public.persons OWNER TO dev_news_ml;

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


ALTER TABLE public.persons_id_seq OWNER TO dev_news_ml;

--
-- TOC entry 2803 (class 0 OID 0)
-- Dependencies: 196
-- Name: persons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: newsml
--



--
-- TOC entry 190 (class 1259 OID 16462)
-- Name: tags; Type: TABLE; Schema: public; Owner: newsml
--

CREATE TABLE public.tags (
    tag_id integer NOT NULL,
    tag_name character varying(128) NOT NULL
);


ALTER TABLE public.tags OWNER TO dev_news_ml;

--
-- TOC entry 191 (class 1259 OID 16468)
-- Name: tags_news; Type: TABLE; Schema: public; Owner: newsml
--

CREATE TABLE public.tags_news (
    tag_id bigint,
    news_id bigint
);


ALTER TABLE public.tags_news OWNER TO dev_news_ml;

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


ALTER TABLE public.tags_tag_id_seq OWNER TO dev_news_ml;

--
-- TOC entry 2806 (class 0 OID 0)
-- Dependencies: 189
-- Name: tags_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: newsml
--



--
-- TOC entry 2635 (class 2604 OID 16476)
-- Name: api_users id; Type: DEFAULT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.api_users ALTER COLUMN id SET DEFAULT nextval('public.api_users_id_seq'::regclass);


--
-- TOC entry 2636 (class 2604 OID 16489)
-- Name: campaign id; Type: DEFAULT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.campaign ALTER COLUMN id SET DEFAULT nextval('public.campaign_id_seq'::regclass);


--
-- TOC entry 2633 (class 2604 OID 16457)
-- Name: companies company_id; Type: DEFAULT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.companies ALTER COLUMN company_id SET DEFAULT nextval('public.companies_company_id_seq'::regclass);


--
-- TOC entry 2632 (class 2604 OID 16446)
-- Name: news news_id; Type: DEFAULT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.news ALTER COLUMN news_id SET DEFAULT nextval('public.news_news_id_seq'::regclass);


--
-- TOC entry 2641 (class 2604 OID 16527)
-- Name: persons id; Type: DEFAULT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.persons ALTER COLUMN id SET DEFAULT nextval('public.persons_id_seq'::regclass);


--
-- TOC entry 2634 (class 2604 OID 16465)
-- Name: tags tag_id; Type: DEFAULT; Schema: public; Owner: newsml
--

ALTER TABLE ONLY public.tags ALTER COLUMN tag_id SET DEFAULT nextval('public.tags_tag_id_seq'::regclass);