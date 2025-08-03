--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: advertisingstatus; Type: TYPE; Schema: public; Owner: soupuser
--

CREATE TYPE public.advertisingstatus AS ENUM (
    'ACTIVE',
    'PAUSED',
    'COMPLETED',
    'PENDING_REVIEW'
);


ALTER TYPE public.advertisingstatus OWNER TO soupuser;

--
-- Name: advertisingtype; Type: TYPE; Schema: public; Owner: soupuser
--

CREATE TYPE public.advertisingtype AS ENUM (
    'BANNER',
    'HIGHLIGHTED_LISTING',
    'SOCIAL_MEDIA_AD'
);


ALTER TYPE public.advertisingtype OWNER TO soupuser;

--
-- Name: businesstype; Type: TYPE; Schema: public; Owner: soupuser
--

CREATE TYPE public.businesstype AS ENUM (
    'PRODUCTOS',
    'SERVICIOS',
    'AMBOS',
    'productos',
    'servicios',
    'ambos'
);


ALTER TYPE public.businesstype OWNER TO soupuser;

--
-- Name: contacttype; Type: TYPE; Schema: public; Owner: soupuser
--

CREATE TYPE public.contacttype AS ENUM (
    'CLIENT',
    'SUPPLIER',
    'PARTNER',
    'OTHER'
);


ALTER TYPE public.contacttype OWNER TO soupuser;

--
-- Name: encargostate; Type: TYPE; Schema: public; Owner: soupuser
--

CREATE TYPE public.encargostate AS ENUM (
    'PENDIENTE_PAGO',
    'EN_PRODUCCION',
    'LISTO_PARA_ENVIO',
    'ENVIADO',
    'ENTREGADO',
    'CANCELADO',
    'COMPLETADO'
);


ALTER TYPE public.encargostate OWNER TO soupuser;

--
-- Name: messagechannel; Type: TYPE; Schema: public; Owner: soupuser
--

CREATE TYPE public.messagechannel AS ENUM (
    'WHATSAPP',
    'EMAIL',
    'PHONE_CALL',
    'IN_APP',
    'OTHER'
);


ALTER TYPE public.messagechannel OWNER TO soupuser;

--
-- Name: productcategory; Type: TYPE; Schema: public; Owner: soupuser
--

CREATE TYPE public.productcategory AS ENUM (
    'PAN',
    'PASTEL',
    'GALLETA',
    'BOLLO',
    'TARTA',
    'EMPANADA',
    'OTRO'
);


ALTER TYPE public.productcategory OWNER TO soupuser;

--
-- Name: producttype; Type: TYPE; Schema: public; Owner: soupuser
--

CREATE TYPE public.producttype AS ENUM (
    'PHYSICAL_GOOD',
    'SERVICE_BY_HOUR',
    'SERVICE_BY_PROJECT',
    'DIGITAL_GOOD'
);


ALTER TYPE public.producttype OWNER TO soupuser;

--
-- Name: publicidadtipo; Type: TYPE; Schema: public; Owner: soupuser
--

CREATE TYPE public.publicidadtipo AS ENUM (
    'BANNER',
    'LISTADO_DESTACADO',
    'ANUNCIO_RED_SOCIAL'
);


ALTER TYPE public.publicidadtipo OWNER TO soupuser;

--
-- Name: shipmentprogress; Type: TYPE; Schema: public; Owner: soupuser
--

CREATE TYPE public.shipmentprogress AS ENUM (
    'PENDIENTE',
    'EN_CAMINO',
    'EN_REPARTO',
    'ENTREGADO',
    'FALLIDO'
);


ALTER TYPE public.shipmentprogress OWNER TO soupuser;

--
-- Name: userrole; Type: TYPE; Schema: public; Owner: soupuser
--

CREATE TYPE public.userrole AS ENUM (
    'TRABAJADOR_ATENCION',
    'COCINERO',
    'MANAGER',
    'ADMIN'
);


ALTER TYPE public.userrole OWNER TO soupuser;

--
-- Name: usertier; Type: TYPE; Schema: public; Owner: soupuser
--

CREATE TYPE public.usertier AS ENUM (
    'CLIENT',
    'FREELANCER',
    'MICROEMPRENDIMIENTO',
    'PREMIUM'
);


ALTER TYPE public.usertier OWNER TO soupuser;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: carritos_compra; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.carritos_compra (
    id uuid NOT NULL,
    negocio_id uuid NOT NULL,
    cliente_id uuid,
    session_id character varying,
    fecha_creacion timestamp with time zone DEFAULT now() NOT NULL,
    fecha_actualizacion timestamp with time zone DEFAULT now() NOT NULL,
    activo boolean NOT NULL
);


ALTER TABLE public.carritos_compra OWNER TO soupuser;

--
-- Name: contactos; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.contactos (
    id uuid NOT NULL,
    nombre character varying(100) NOT NULL,
    tipo_contacto public.contacttype NOT NULL,
    info_contacto json NOT NULL,
    empresa character varying(100),
    notas text,
    usuario_id uuid NOT NULL,
    fecha_creacion timestamp with time zone DEFAULT now() NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL
);


ALTER TABLE public.contactos OWNER TO soupuser;

--
-- Name: detalles_venta; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.detalles_venta (
    id uuid NOT NULL,
    venta_id uuid NOT NULL,
    producto_id uuid NOT NULL,
    cantidad double precision NOT NULL,
    precio_unitario double precision NOT NULL,
    descuento_unitario double precision NOT NULL,
    subtotal double precision NOT NULL,
    costo_unitario double precision,
    margen_ganancia double precision,
    codigo_lote character varying
);


ALTER TABLE public.detalles_venta OWNER TO soupuser;

--
-- Name: encargos; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.encargos (
    id uuid NOT NULL,
    cliente_id uuid NOT NULL,
    producto_id uuid NOT NULL,
    cantidad double precision NOT NULL,
    precio_total double precision NOT NULL,
    fecha_encargo timestamp with time zone DEFAULT now() NOT NULL,
    fecha_entrega_estimada timestamp with time zone,
    estado public.encargostate NOT NULL,
    notas text,
    direccion_envio character varying(255),
    progreso_envio public.shipmentprogress,
    usuario_id uuid NOT NULL,
    fecha_creacion timestamp with time zone DEFAULT now() NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL
);


ALTER TABLE public.encargos OWNER TO soupuser;

--
-- Name: horarios_pico; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.horarios_pico (
    id uuid NOT NULL,
    negocio_id uuid NOT NULL,
    dia_semana integer NOT NULL,
    hora_inicio character varying NOT NULL,
    hora_fin character varying NOT NULL,
    ventas_promedio double precision,
    productos_vendidos_promedio integer,
    clientes_promedio integer,
    activo boolean NOT NULL,
    prioridad integer,
    fecha_creacion timestamp with time zone DEFAULT now() NOT NULL,
    fecha_actualizacion timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.horarios_pico OWNER TO soupuser;

--
-- Name: ingredientes_receta; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.ingredientes_receta (
    id uuid NOT NULL,
    receta_id uuid NOT NULL,
    insumo_id uuid NOT NULL,
    cantidad_necesaria double precision NOT NULL,
    unidad_medida character varying NOT NULL,
    orden integer,
    notas text
);


ALTER TABLE public.ingredientes_receta OWNER TO soupuser;

--
-- Name: insumos; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.insumos (
    id uuid NOT NULL,
    nombre character varying(100) NOT NULL,
    cantidad_disponible double precision NOT NULL,
    unidad_medida_compra character varying(50) NOT NULL,
    costo_unitario_compra double precision NOT NULL,
    usuario_id uuid NOT NULL,
    fecha_creacion timestamp with time zone DEFAULT now() NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL
);


ALTER TABLE public.insumos OWNER TO soupuser;

--
-- Name: items_carrito; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.items_carrito (
    id uuid NOT NULL,
    carrito_id uuid NOT NULL,
    producto_id uuid NOT NULL,
    cantidad double precision NOT NULL,
    precio_unitario double precision NOT NULL,
    fecha_agregado timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.items_carrito OWNER TO soupuser;

--
-- Name: mensajes_registro; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.mensajes_registro (
    id uuid NOT NULL,
    contacto_id uuid NOT NULL,
    canal public.messagechannel NOT NULL,
    contenido text NOT NULL,
    fecha_envio timestamp with time zone NOT NULL,
    usuario_id uuid NOT NULL,
    fecha_creacion timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.mensajes_registro OWNER TO soupuser;

--
-- Name: negocios; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.negocios (
    id uuid NOT NULL,
    nombre character varying(100) NOT NULL,
    rubro character varying(100),
    descripcion text,
    localizacion_geografica character varying(255),
    fotos_urls json,
    fecha_creacion timestamp with time zone DEFAULT now() NOT NULL,
    fecha_actualizacion timestamp with time zone DEFAULT now(),
    propietario_id uuid NOT NULL,
    tipo_negocio public.businesstype DEFAULT 'productos'::public.businesstype NOT NULL,
    calificacion_promedio double precision,
    total_calificaciones integer,
    ventas_completadas integer
);


ALTER TABLE public.negocios OWNER TO soupuser;

--
-- Name: producciones; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.producciones (
    id uuid NOT NULL,
    receta_id uuid NOT NULL,
    negocio_id uuid NOT NULL,
    productor_id uuid NOT NULL,
    fecha_produccion date NOT NULL,
    hora_inicio timestamp with time zone,
    hora_fin timestamp with time zone,
    cantidad_producida double precision NOT NULL,
    cantidad_esperada double precision NOT NULL,
    rendimiento_real double precision,
    calidad character varying,
    observaciones text,
    problemas text,
    costo_total double precision,
    costo_unitario double precision,
    estado character varying NOT NULL,
    fecha_creacion timestamp with time zone DEFAULT now() NOT NULL,
    fecha_actualizacion timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.producciones OWNER TO soupuser;

--
-- Name: producto_insumo; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.producto_insumo (
    id uuid NOT NULL,
    producto_id uuid NOT NULL,
    insumo_id uuid NOT NULL,
    cantidad_necesaria double precision NOT NULL,
    fecha_creacion timestamp with time zone DEFAULT now() NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    fecha_asociacion timestamp with time zone DEFAULT now()
);


ALTER TABLE public.producto_insumo OWNER TO soupuser;

--
-- Name: producto_insumos; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.producto_insumos (
    id uuid NOT NULL,
    producto_id uuid NOT NULL,
    insumo_id uuid NOT NULL,
    cantidad_necesaria double precision NOT NULL,
    fecha_asociacion timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.producto_insumos OWNER TO soupuser;

--
-- Name: productos; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.productos (
    id uuid NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    tipo_producto public.producttype NOT NULL,
    fotos_urls json,
    stock integer,
    unidad_medida character varying(50),
    atributos_especificos json,
    negocio_id uuid,
    precio_sugerido double precision,
    cogs double precision,
    margen_ganancia_porcentaje double precision,
    rating_promedio double precision DEFAULT 0.0 NOT NULL,
    reviews_count integer DEFAULT 0 NOT NULL,
    fecha_creacion timestamp with time zone DEFAULT now() NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    precio_venta double precision,
    margen_ganancia_sugerido double precision,
    precio double precision DEFAULT 0.0 NOT NULL,
    propietario_id uuid NOT NULL,
    calificacion_promedio double precision,
    total_calificaciones integer,
    ventas_completadas integer,
    stock_terminado double precision DEFAULT 0.0,
    margen_ganancia_real double precision,
    categoria character varying(50),
    codigo_lote character varying(100),
    fecha_vencimiento date,
    fecha_produccion date,
    stock_minimo double precision DEFAULT 0.0,
    stock_maximo double precision,
    unidad_venta character varying(50) DEFAULT 'unidad'::character varying,
    es_perecedero boolean DEFAULT true,
    tiempo_vida_util integer,
    requiere_refrigeracion boolean DEFAULT false,
    ingredientes text[],
    alergenos text[],
    calorias_por_porcion double precision,
    peso_porcion double precision,
    unidad_peso character varying(10) DEFAULT 'g'::character varying
);


ALTER TABLE public.productos OWNER TO soupuser;

--
-- Name: COLUMN productos.stock_terminado; Type: COMMENT; Schema: public; Owner: soupuser
--

COMMENT ON COLUMN public.productos.stock_terminado IS 'Cantidad de productos terminados disponibles para venta';


--
-- Name: publicidades; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.publicidades (
    id uuid NOT NULL,
    item_publicitado_id uuid NOT NULL,
    tipo_publicidad public.advertisingtype NOT NULL,
    fecha_inicio timestamp with time zone NOT NULL,
    fecha_fin timestamp with time zone NOT NULL,
    costo double precision NOT NULL,
    usuario_id uuid NOT NULL,
    estado public.advertisingstatus NOT NULL,
    visualizaciones integer NOT NULL,
    clics integer NOT NULL,
    conversiones integer NOT NULL,
    fecha_creacion timestamp with time zone DEFAULT now() NOT NULL,
    fecha_actualizacion timestamp with time zone NOT NULL,
    nombre character varying DEFAULT 'Publicidad'::character varying NOT NULL,
    item_publicitado_tipo character varying DEFAULT 'producto'::character varying NOT NULL
);


ALTER TABLE public.publicidades OWNER TO soupuser;

--
-- Name: recetas; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.recetas (
    id uuid NOT NULL,
    nombre character varying NOT NULL,
    descripcion text,
    producto_id uuid NOT NULL,
    negocio_id uuid NOT NULL,
    creador_id uuid NOT NULL,
    tiempo_preparacion integer,
    tiempo_coccion integer,
    temperatura_horno double precision,
    rendimiento double precision,
    unidad_rendimiento character varying,
    dificultad character varying,
    instrucciones text,
    fecha_creacion timestamp with time zone DEFAULT now() NOT NULL,
    fecha_actualizacion timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.recetas OWNER TO soupuser;

--
-- Name: reviews; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.reviews (
    id uuid NOT NULL,
    encargo_id uuid NOT NULL,
    rating integer NOT NULL,
    comentario text,
    fecha_review timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.reviews OWNER TO soupuser;

--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.usuarios (
    id uuid NOT NULL,
    nombre character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    localizacion character varying(255),
    info_contacto json,
    tipo_tier public.usertier NOT NULL,
    fecha_creacion timestamp with time zone DEFAULT now() NOT NULL,
    fecha_actualizacion timestamp with time zone DEFAULT now() NOT NULL,
    curriculum_vitae character varying,
    hashed_password character varying,
    is_active boolean DEFAULT true,
    plugins_activos text[] DEFAULT '{}'::text[],
    rol character varying(50),
    negocio_asignado_id uuid,
    fecha_contratacion date,
    salario numeric(10,2),
    horario_trabajo character varying(100),
    permisos_especiales text[] DEFAULT '{}'::text[]
);


ALTER TABLE public.usuarios OWNER TO soupuser;

--
-- Name: ventas; Type: TABLE; Schema: public; Owner: soupuser
--

CREATE TABLE public.ventas (
    id uuid NOT NULL,
    negocio_id uuid NOT NULL,
    cliente_id uuid,
    numero_venta character varying NOT NULL,
    fecha_venta timestamp with time zone DEFAULT now() NOT NULL,
    subtotal double precision NOT NULL,
    descuento double precision NOT NULL,
    impuestos double precision NOT NULL,
    total double precision NOT NULL,
    metodo_pago character varying,
    estado character varying NOT NULL,
    notas text,
    margen_ganancia_total double precision,
    costo_total double precision
);


ALTER TABLE public.ventas OWNER TO soupuser;

--
-- Data for Name: carritos_compra; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.carritos_compra (id, negocio_id, cliente_id, session_id, fecha_creacion, fecha_actualizacion, activo) FROM stdin;
\.


--
-- Data for Name: contactos; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.contactos (id, nombre, tipo_contacto, info_contacto, empresa, notas, usuario_id, fecha_creacion, fecha_actualizacion) FROM stdin;
\.


--
-- Data for Name: detalles_venta; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.detalles_venta (id, venta_id, producto_id, cantidad, precio_unitario, descuento_unitario, subtotal, costo_unitario, margen_ganancia, codigo_lote) FROM stdin;
\.


--
-- Data for Name: encargos; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.encargos (id, cliente_id, producto_id, cantidad, precio_total, fecha_encargo, fecha_entrega_estimada, estado, notas, direccion_envio, progreso_envio, usuario_id, fecha_creacion, fecha_actualizacion) FROM stdin;
\.


--
-- Data for Name: horarios_pico; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.horarios_pico (id, negocio_id, dia_semana, hora_inicio, hora_fin, ventas_promedio, productos_vendidos_promedio, clientes_promedio, activo, prioridad, fecha_creacion, fecha_actualizacion) FROM stdin;
\.


--
-- Data for Name: ingredientes_receta; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.ingredientes_receta (id, receta_id, insumo_id, cantidad_necesaria, unidad_medida, orden, notas) FROM stdin;
\.


--
-- Data for Name: insumos; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.insumos (id, nombre, cantidad_disponible, unidad_medida_compra, costo_unitario_compra, usuario_id, fecha_creacion, fecha_actualizacion) FROM stdin;
6bd2c6ce-2255-4539-a8f7-b16bf3b9d53f	Harina	10	kg	2.5	39937ac4-5b47-4a5f-87fb-3fa0adcd2f5f	2025-07-07 20:03:24.115235-03	2025-07-07 20:03:24.115235-03
daf112a6-867e-4f03-9bc5-f462b7c4ffd7	Azúcar	5	kg	3	39937ac4-5b47-4a5f-87fb-3fa0adcd2f5f	2025-07-07 20:03:24.115235-03	2025-07-07 20:03:24.115235-03
f2ad0d3e-3917-42bc-b05a-fccbd43f3c35	Harina de Trigo 000	50	kg	0.8	d3c0a59c-26e2-4f01-a222-c2e2452f4d02	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
87c1f77e-edc7-43fa-a44a-f43c020fa712	Harina Integral	30	kg	1.2	d3c0a59c-26e2-4f01-a222-c2e2452f4d02	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
47ad4343-b2b3-4976-bfe8-924d6415fdfa	Levadura Fresca	2	kg	2.5	d3c0a59c-26e2-4f01-a222-c2e2452f4d02	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
3cd45677-d8c9-45c4-918f-46c67bb1d4c4	Azúcar Blanca	25	kg	1.2	d3c0a59c-26e2-4f01-a222-c2e2452f4d02	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
b237707a-c9d0-4e10-8878-582e4c0a38f7	Manteca	15	kg	3.5	d3c0a59c-26e2-4f01-a222-c2e2452f4d02	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
1fe5aee9-4aa9-4311-9afd-7a34e403b3d7	Huevos	200	unidad	0.15	d3c0a59c-26e2-4f01-a222-c2e2452f4d02	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
ffdf60f5-251b-4de4-8f64-1ac270ed38f0	Leche	40	litro	0.8	d3c0a59c-26e2-4f01-a222-c2e2452f4d02	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
639cb394-3deb-4fa8-8c2d-1ff82abb3c72	Sal Fina	5	kg	0.5	d3c0a59c-26e2-4f01-a222-c2e2452f4d02	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
a4768395-f71b-4e4f-93a4-2ce7762935a8	Aceite de Oliva	10	litro	2.8	d3c0a59c-26e2-4f01-a222-c2e2452f4d02	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
14de9876-5e75-4246-80d0-1b55d6b1b8a3	Dulce de Leche	8	kg	4	d3c0a59c-26e2-4f01-a222-c2e2452f4d02	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
56a574ac-ec7c-4233-a8b2-3be4a637e40d	Licencia Adobe Creative Suite	1	licencia	50	4106dbf0-69be-43a8-9f28-17e0dfcb31c3	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
81e874dd-9db7-4d28-8d02-40daded3119b	Licencia Figma Pro	1	licencia	15	4106dbf0-69be-43a8-9f28-17e0dfcb31c3	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
b51f1d27-9919-41b1-bdd4-a044bc4538b6	Hosting Web	12	mes	8	4106dbf0-69be-43a8-9f28-17e0dfcb31c3	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
a5e2e55f-da57-443a-b4ae-e63d54a502d8	Dominio Web	1	año	12	4106dbf0-69be-43a8-9f28-17e0dfcb31c3	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
d871a13a-b225-4fef-b37d-d431db7150dd	Stock de Imágenes	100	imagen	0.5	4106dbf0-69be-43a8-9f28-17e0dfcb31c3	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
d4713100-21ce-4884-ba4c-5b6e07d25ac2	Fuentes Premium	50	fuente	2	4106dbf0-69be-43a8-9f28-17e0dfcb31c3	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
8bea07c0-9f4b-4538-94e9-cecf5fee0129	Energía Eléctrica	160	hora	0.1	4106dbf0-69be-43a8-9f28-17e0dfcb31c3	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
030eb5e1-9e41-441a-abbd-c3198e8b2f05	Internet	160	hora	0.05	4106dbf0-69be-43a8-9f28-17e0dfcb31c3	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
666dfafd-449e-4586-8b15-485e30226cb6	Café	160	taza	0.3	4106dbf0-69be-43a8-9f28-17e0dfcb31c3	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
2fab530b-2bb6-4471-b228-c995ba1b3a44	Sal	2	kg	200	aee8ca47-d7e1-4729-b1e5-9fa23a28eedb	2025-07-07 19:29:35.266734-03	2025-07-09 17:50:01.191312-03
4261ac77-9bcb-4d65-a0df-0cba8d76d5d1	Harina	5	kg	2000	aee8ca47-d7e1-4729-b1e5-9fa23a28eedb	2025-07-07 19:20:14.068372-03	2025-07-09 17:50:16.777933-03
\.


--
-- Data for Name: items_carrito; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.items_carrito (id, carrito_id, producto_id, cantidad, precio_unitario, fecha_agregado) FROM stdin;
\.


--
-- Data for Name: mensajes_registro; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.mensajes_registro (id, contacto_id, canal, contenido, fecha_envio, usuario_id, fecha_creacion) FROM stdin;
\.


--
-- Data for Name: negocios; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.negocios (id, nombre, rubro, descripcion, localizacion_geografica, fotos_urls, fecha_creacion, fecha_actualizacion, propietario_id, tipo_negocio, calificacion_promedio, total_calificaciones, ventas_completadas) FROM stdin;
349f1893-9c0d-473b-bc37-fdde20f31ca6	SOUP Software Studio	Desarrollo de Software	Sistema Operativo Universal Personal\nEcosistema de servicios web\nArquitectura de Software	Paraná	["https://thehappypear.ie/wp-content/uploads/2024/10/Roasted-Tomato-and-Pumpkin-Traybake-Soup-500x500.jpg"]	2025-07-07 18:42:27.446585-03	2025-07-08 15:06:37.578146-03	aee8ca47-d7e1-4729-b1e5-9fa23a28eedb	PRODUCTOS	\N	\N	\N
4061845b-a8bc-429d-8363-636c24eb6c01	IDZ Estudio de Arquitectura	Arquitectura	Anteproyectos y Presupuestos de Obras de Construcción	Paraná	["https://www.uhipocrates.edu.mx/wp-content/uploads/2022/07/carrera-de-arquitectura-y-urbanismo.jpg"]	2025-07-08 15:47:49.053093-03	2025-07-08 15:48:22.216095-03	aee8ca47-d7e1-4729-b1e5-9fa23a28eedb	SERVICIOS	\N	\N	\N
36ceeaea-e97d-417c-8366-0f4a3946f708	Panadería Artesanal Ñiam	Panadería	Panadería Artesanal	Paraná	["https://scontent.fros8-1.fna.fbcdn.net/v/t39.30808-6/494206219_1252182360248587_5569894707026610990_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=127cfc&_nc_eui2=AeGXd2804B3Go5GEOY4MVVTOmuCeZQkIkUaa4J5lCQiRRjEaYZh_Z1Mm9UMjq3fyXhQ&_nc_ohc=8cmR50KxefUQ7kNvwH6ubhb&_nc_oc=Adm1ji9WMdHH5bTedUvkYqLKKFP15-83G8n7o8ar667k3I5cCLvqmUz_OFMLFsESJVI&_nc_zt=23&_nc_ht=scontent.fros8-1.fna&_nc_gid=m931vFFYPO1DUKDO2-B4vw&oh=00_AfSftzuQVN5MOUK0R8iVQqmoVgG_qeiQ-SAAWzYujpmqDQ&oe=68731370"]	2025-07-07 18:42:36.381512-03	2025-07-08 17:18:29.735446-03	aee8ca47-d7e1-4729-b1e5-9fa23a28eedb	PRODUCTOS	\N	\N	\N
cf95f34c-584a-4f4a-a1df-0a6b1bb37abf	Panadería Test POS	\N	Panadería para testing del sistema POS	\N	\N	2025-07-09 00:04:30.945067-03	2025-07-09 00:04:30.945067-03	cf64095a-1646-4ffe-85f7-d1e35a79a43a	PRODUCTOS	\N	\N	\N
91704c9d-9f36-4939-aa19-1b323e5ea853	Panadería Artesanal 'El Horno Mágico'	Alimentos y Bebidas	Panes de masa madre, facturas y pastelería fina elaborados con técnicas tradicionales.	CABA, Argentina	["https://lechecontuna.com/wp-content/uploads/2022/02/Panaderia-La-Roca-5.jpg"]	2025-07-08 01:46:46.688179-03	2025-07-08 12:49:26.505062-03	d3c0a59c-26e2-4f01-a222-c2e2452f4d02	PRODUCTOS	\N	\N	\N
b74ce22f-0941-4be8-849a-ed52d573cb31	Estudio de Diseño 'Pixel Perfect'	Diseño y Tecnología	Estudio creativo especializado en diseño gráfico, branding corporativo, diseño web y UX/UI.	Córdoba, Argentina	["https://media.istockphoto.com/id/641193684/es/foto/duro-d%C3%ADa-de-trabajo.jpg?s=612x612&w=0&k=20&c=V3jmvh03frtBLxivnLe40nV32xb_oOeKuU6DfKZkII0="]	2025-07-08 01:46:46.688179-03	2025-07-08 12:55:48.455766-03	4106dbf0-69be-43a8-9f28-17e0dfcb31c3	SERVICIOS	\N	\N	\N
ef83023c-6c4e-4f9f-9714-a0e386c0b2fa	Panadería Test POS	\N	Panadería para testing del sistema POS	\N	\N	2025-07-09 00:07:52.101951-03	2025-07-09 00:07:52.101951-03	cf64095a-1646-4ffe-85f7-d1e35a79a43a	PRODUCTOS	\N	\N	\N
0cc806ed-7556-4ccd-a812-7efd52523ecc	Test Business	\N	Business for testing	\N	\N	2025-07-09 00:09:52.611837-03	2025-07-09 00:09:52.611837-03	cd8d8f1d-089e-4231-9fe2-f4ac70fca878	PRODUCTOS	\N	\N	\N
15144d71-502c-422c-99f5-afe94e28101f	Test Business	\N	Business for testing	\N	\N	2025-07-09 00:16:05.558922-03	2025-07-09 00:16:05.558922-03	cd8d8f1d-089e-4231-9fe2-f4ac70fca878	PRODUCTOS	\N	\N	\N
68abfe64-7052-47aa-ba28-5bcb25fe411f	Test Business	\N	Business for testing	\N	\N	2025-07-09 00:24:29.707668-03	2025-07-09 00:24:29.707668-03	cd8d8f1d-089e-4231-9fe2-f4ac70fca878	PRODUCTOS	\N	\N	\N
d24a178f-abf9-40c8-a597-6ad1a524c1c2	Test Business	\N	Business for testing	\N	\N	2025-07-09 00:26:46.836297-03	2025-07-09 00:26:46.836297-03	cd8d8f1d-089e-4231-9fe2-f4ac70fca878	PRODUCTOS	\N	\N	\N
48af3c45-0363-416a-9278-31ebd84b3a90	Test Business	\N	Business for testing	\N	\N	2025-07-09 00:28:02.403011-03	2025-07-09 00:28:02.403011-03	cd8d8f1d-089e-4231-9fe2-f4ac70fca878	PRODUCTOS	\N	\N	\N
23cfe571-5fdb-48a1-ba8d-9e78620b8346	Test Business	\N	Business for testing	\N	\N	2025-07-09 00:33:00.874337-03	2025-07-09 00:33:00.874337-03	cd8d8f1d-089e-4231-9fe2-f4ac70fca878	PRODUCTOS	\N	\N	\N
409a8d61-2e8c-4dc9-9df5-c692cdb8e77e	Test Business	\N	Business for testing	\N	\N	2025-07-09 00:35:09.962845-03	2025-07-09 00:35:09.962845-03	cd8d8f1d-089e-4231-9fe2-f4ac70fca878	PRODUCTOS	\N	\N	\N
65619ed3-a1b1-4c35-8a0d-1c5687986d89	Test Business	\N	Business for testing	\N	\N	2025-07-09 00:39:41.814523-03	2025-07-09 00:39:41.814523-03	cd8d8f1d-089e-4231-9fe2-f4ac70fca878	PRODUCTOS	\N	\N	\N
00937602-e50f-4fb5-a498-f70bfae7f6b0	Test Business	\N	Business for testing	\N	\N	2025-07-09 00:40:34.137034-03	2025-07-09 00:40:34.137034-03	cd8d8f1d-089e-4231-9fe2-f4ac70fca878	PRODUCTOS	\N	\N	\N
478faf6e-efb1-4d2c-bea3-650caea71062	Test Business	\N	Business for testing	\N	\N	2025-07-09 00:54:46.658179-03	2025-07-09 00:54:46.658179-03	cd8d8f1d-089e-4231-9fe2-f4ac70fca878	PRODUCTOS	\N	\N	\N
9c6863e6-2cda-48b6-9dbe-9e12e3385dea	Panadería Test POS	\N	Panadería para testing del sistema POS	\N	\N	2025-07-09 00:55:27.879038-03	2025-07-09 00:55:27.879038-03	cf64095a-1646-4ffe-85f7-d1e35a79a43a	PRODUCTOS	\N	\N	\N
\.


--
-- Data for Name: producciones; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.producciones (id, receta_id, negocio_id, productor_id, fecha_produccion, hora_inicio, hora_fin, cantidad_producida, cantidad_esperada, rendimiento_real, calidad, observaciones, problemas, costo_total, costo_unitario, estado, fecha_creacion, fecha_actualizacion) FROM stdin;
\.


--
-- Data for Name: producto_insumo; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.producto_insumo (id, producto_id, insumo_id, cantidad_necesaria, fecha_creacion, fecha_actualizacion, fecha_asociacion) FROM stdin;
15c0da85-8a37-4866-8c4e-bdd2830a6915	e2e13234-8f2f-40a6-8f66-c8948c536217	4261ac77-9bcb-4d65-a0df-0cba8d76d5d1	1	2025-07-07 19:44:18.987048-03	2025-07-07 19:44:18.987048-03	2025-07-07 20:15:27.365249-03
c1e6ddb9-ab04-4025-8855-f0756fa32d87	fbaf398e-72c4-48b8-b24b-41bb30efa564	4261ac77-9bcb-4d65-a0df-0cba8d76d5d1	0.3	2025-07-07 19:43:50.277767-03	2025-07-07 19:51:55.477282-03	2025-07-07 20:15:27.365249-03
9c074cbb-3b8a-401c-ad85-0f093a7bafc5	e2e13234-8f2f-40a6-8f66-c8948c536217	2fab530b-2bb6-4471-b228-c995ba1b3a44	0.05	2025-07-07 19:44:18.987048-03	2025-07-07 19:52:14.658464-03	2025-07-07 20:15:27.365249-03
828643b5-fbd2-451c-8e0a-aa841d92cc59	fbaf398e-72c4-48b8-b24b-41bb30efa564	2fab530b-2bb6-4471-b228-c995ba1b3a44	0.01	2025-07-07 19:51:55.477282-03	2025-07-07 19:52:24.584017-03	2025-07-07 20:15:27.365249-03
7852fe81-f965-497c-9722-b872d47e3501	f5ad58ef-b4f8-4020-bf68-e6df4beb6604	6bd2c6ce-2255-4539-a8f7-b16bf3b9d53f	0.5	2025-07-07 20:03:24.115235-03	2025-07-07 20:03:24.115235-03	2025-07-07 20:15:27.365249-03
faa7243e-a2d6-405a-9921-83a185b29fc0	f5ad58ef-b4f8-4020-bf68-e6df4beb6604	daf112a6-867e-4f03-9bc5-f462b7c4ffd7	0.1	2025-07-07 20:03:24.115235-03	2025-07-07 20:03:24.115235-03	2025-07-07 20:15:27.365249-03
8013de18-0f56-4494-9209-86017702da2d	11d835b0-b753-41f1-a52a-c89aa74337fe	87c1f77e-edc7-43fa-a44a-f43c020fa712	0.5	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
637dd474-5f37-4109-babc-5707d9d9b897	11d835b0-b753-41f1-a52a-c89aa74337fe	47ad4343-b2b3-4976-bfe8-924d6415fdfa	0.01	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
c265bda5-ea0b-407a-94bf-03bf19a6f28b	11d835b0-b753-41f1-a52a-c89aa74337fe	639cb394-3deb-4fa8-8c2d-1ff82abb3c72	0.01	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
3c67c6b6-a10d-4da8-856a-111a8fd536db	11d835b0-b753-41f1-a52a-c89aa74337fe	a4768395-f71b-4e4f-93a4-2ce7762935a8	0.02	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
fee68ea6-b4d4-4c12-991e-329cd3783d6e	5626787a-24e6-46b6-806e-17147354e72b	f2ad0d3e-3917-42bc-b05a-fccbd43f3c35	0.8	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
8bbf1bca-1af2-4597-929e-4b7a91b5d61b	5626787a-24e6-46b6-806e-17147354e72b	3cd45677-d8c9-45c4-918f-46c67bb1d4c4	0.1	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
30e26009-3685-4161-954e-74bb630cafdf	5626787a-24e6-46b6-806e-17147354e72b	b237707a-c9d0-4e10-8878-582e4c0a38f7	0.3	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
ea7feae5-9a39-4451-a403-a4bd9f747d3f	5626787a-24e6-46b6-806e-17147354e72b	1fe5aee9-4aa9-4311-9afd-7a34e403b3d7	2	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
7e89f058-33be-4c1c-b8e5-3ae7a166cc1d	5626787a-24e6-46b6-806e-17147354e72b	ffdf60f5-251b-4de4-8f64-1ac270ed38f0	0.2	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
9ff0ba70-5d59-4a94-8b67-d4378353ff9c	5626787a-24e6-46b6-806e-17147354e72b	14de9876-5e75-4246-80d0-1b55d6b1b8a3	0.2	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
e1fc6b21-a1e1-46da-a78f-a3f104902510	312834f7-3cde-47dc-af15-066c9a5656f6	56a574ac-ec7c-4233-a8b2-3be4a637e40d	0.1	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
9cb419ca-fb59-4f6f-8d11-9aafca0e7a85	312834f7-3cde-47dc-af15-066c9a5656f6	8bea07c0-9f4b-4538-94e9-cecf5fee0129	8	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
68ce9828-8f96-4a0c-9c7b-1b3b7d19d55c	312834f7-3cde-47dc-af15-066c9a5656f6	030eb5e1-9e41-441a-abbd-c3198e8b2f05	8	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
130de509-1184-4476-870b-a3e524e6a04c	312834f7-3cde-47dc-af15-066c9a5656f6	666dfafd-449e-4586-8b15-485e30226cb6	4	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
e078b6f0-3a64-4654-b81e-a3bfb0d4cb52	1860e753-801d-4aac-96b9-c9fb0c3c51d3	56a574ac-ec7c-4233-a8b2-3be4a637e40d	0.2	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
f47381e3-04e5-48b8-854a-3d7295f91d07	1860e753-801d-4aac-96b9-c9fb0c3c51d3	d4713100-21ce-4884-ba4c-5b6e07d25ac2	2	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
c486a38e-cbb0-4be6-8c50-0218388be59c	1860e753-801d-4aac-96b9-c9fb0c3c51d3	8bea07c0-9f4b-4538-94e9-cecf5fee0129	20	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
e3ae2514-fd00-44d5-9de9-7c8e91a8f4a6	1860e753-801d-4aac-96b9-c9fb0c3c51d3	030eb5e1-9e41-441a-abbd-c3198e8b2f05	20	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
cb40b68a-50df-473f-9125-570c0f365691	1860e753-801d-4aac-96b9-c9fb0c3c51d3	666dfafd-449e-4586-8b15-485e30226cb6	10	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03
\.


--
-- Data for Name: producto_insumos; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.producto_insumos (id, producto_id, insumo_id, cantidad_necesaria, fecha_asociacion) FROM stdin;
b56c8b3c-af74-43ec-86ef-d515d03a508d	fbaf398e-72c4-48b8-b24b-41bb30efa564	4261ac77-9bcb-4d65-a0df-0cba8d76d5d1	1	2025-07-10 10:24:10.665137-03
81fb1a93-3e57-42e0-8e1b-e07e4b67e34c	fbaf398e-72c4-48b8-b24b-41bb30efa564	2fab530b-2bb6-4471-b228-c995ba1b3a44	0.05	2025-07-10 10:24:10.665137-03
\.


--
-- Data for Name: productos; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.productos (id, nombre, descripcion, tipo_producto, fotos_urls, stock, unidad_medida, atributos_especificos, negocio_id, precio_sugerido, cogs, margen_ganancia_porcentaje, rating_promedio, reviews_count, fecha_creacion, fecha_actualizacion, precio_venta, margen_ganancia_sugerido, precio, propietario_id, calificacion_promedio, total_calificaciones, ventas_completadas, stock_terminado, margen_ganancia_real, categoria, codigo_lote, fecha_vencimiento, fecha_produccion, stock_minimo, stock_maximo, unidad_venta, es_perecedero, tiempo_vida_util, requiere_refrigeracion, ingredientes, alergenos, calorias_por_porcion, peso_porcion, unidad_peso) FROM stdin;
2e98d8b4-9509-4b85-ae65-51a7cfcaa093	Test Product	Product for testing	PHYSICAL_GOOD	\N	\N	\N	\N	00937602-e50f-4fb5-a498-f70bfae7f6b0	0	0	\N	0	0	2025-07-09 00:40:36.221138-03	2025-07-09 00:40:36.221138-03	15	50	10	cd8d8f1d-089e-4231-9fe2-f4ac70fca878	\N	\N	\N	100	\N	\N	\N	\N	\N	0	\N	unidad	t	\N	f	\N	\N	\N	\N	g
9bf75d31-5519-43ca-8c8c-3b0c711e1a40	Test Product	Product for testing	PHYSICAL_GOOD	\N	\N	\N	\N	478faf6e-efb1-4d2c-bea3-650caea71062	0	0	\N	0	0	2025-07-09 00:54:48.743605-03	2025-07-09 00:54:48.743605-03	15	50	10	cd8d8f1d-089e-4231-9fe2-f4ac70fca878	\N	\N	\N	100	\N	\N	\N	\N	\N	0	\N	unidad	t	\N	f	\N	\N	\N	\N	g
b215807a-f41d-4268-9be8-a2dee5817a6f	Pan de Molde	Pan de molde fresco	PHYSICAL_GOOD	\N	\N	\N	\N	9c6863e6-2cda-48b6-9dbe-9e12e3385dea	\N	0	\N	0	0	2025-07-09 00:55:29.948179-03	2025-07-09 00:55:48.78247-03	\N	\N	2.5	cf64095a-1646-4ffe-85f7-d1e35a79a43a	\N	\N	\N	25	\N	\N	\N	\N	\N	0	\N	unidad	t	\N	f	\N	\N	\N	\N	g
f5ad58ef-b4f8-4020-bf68-e6df4beb6604	Pan Casero	Pan artesanal hecho en casa	PHYSICAL_GOOD	\N	20	unidad	\N	349f1893-9c0d-473b-bc37-fdde20f31ca6	\N	0	\N	0	0	2025-07-07 20:03:24.115235-03	2025-07-07 20:03:24.115235-03	15	30	10	39937ac4-5b47-4a5f-87fb-3fa0adcd2f5f	\N	\N	\N	50	\N	\N	\N	\N	\N	0	\N	unidad	t	\N	f	\N	\N	\N	\N	g
11d835b0-b753-41f1-a52a-c89aa74337fe	Pan de Masa Madre Integral	Pan artesanal de masa madre con harina integral.	PHYSICAL_GOOD	\N	\N	\N	\N	91704c9d-9f36-4939-aa19-1b323e5ea853	\N	\N	\N	0	0	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	6.5	100	3	d3c0a59c-26e2-4f01-a222-c2e2452f4d02	\N	\N	\N	50	\N	\N	\N	\N	\N	0	\N	unidad	t	\N	f	\N	\N	\N	\N	g
5626787a-24e6-46b6-806e-17147354e72b	Facturas Mixtas x Docena	Surtido de facturas frescas, ideales para el desayuno.	PHYSICAL_GOOD	\N	\N	\N	\N	91704c9d-9f36-4939-aa19-1b323e5ea853	\N	\N	\N	0	0	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	12	120	5	d3c0a59c-26e2-4f01-a222-c2e2452f4d02	\N	\N	\N	50	\N	\N	\N	\N	\N	0	\N	unidad	t	\N	f	\N	\N	\N	\N	g
312834f7-3cde-47dc-af15-066c9a5656f6	Logo Corporativo	Diseño de logo profesional con 3 propuestas iniciales, 2 revisiones incluidas.	SERVICE_BY_PROJECT	\N	\N	\N	\N	b74ce22f-0941-4be8-849a-ed52d573cb31	\N	\N	\N	0	0	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	300	1900	15	4106dbf0-69be-43a8-9f28-17e0dfcb31c3	\N	\N	\N	50	\N	\N	\N	\N	\N	0	\N	unidad	t	\N	f	\N	\N	\N	\N	g
1860e753-801d-4aac-96b9-c9fb0c3c51d3	Identidad Visual Completa	Branding completo incluyendo logo, paleta de colores, tipografías.	SERVICE_BY_PROJECT	\N	\N	\N	\N	b74ce22f-0941-4be8-849a-ed52d573cb31	\N	\N	\N	0	0	2025-07-08 01:59:42.250191-03	2025-07-08 01:59:42.250191-03	800	3100	25	4106dbf0-69be-43a8-9f28-17e0dfcb31c3	\N	\N	\N	50	\N	\N	\N	\N	\N	0	\N	unidad	t	\N	f	\N	\N	\N	\N	g
e2e13234-8f2f-40a6-8f66-c8948c536217	Pan Frances	1 kg de pan frances	PHYSICAL_GOOD	[]	10	kg	null	36ceeaea-e97d-417c-8366-0f4a3946f708	\N	0	\N	0	0	2025-07-07 19:26:02.25075-03	2025-07-10 01:44:25.658883-03	\N	\N	10	aee8ca47-d7e1-4729-b1e5-9fa23a28eedb	\N	\N	\N	33	\N	\N	\N	\N	\N	0	\N	unidad	t	\N	f	\N	\N	\N	\N	g
fbaf398e-72c4-48b8-b24b-41bb30efa564	Chipá	Una unidad de chipá recien salido del horno	PHYSICAL_GOOD	[]	20	unidad	null	36ceeaea-e97d-417c-8366-0f4a3946f708	\N	2010	\N	0	0	2025-07-07 18:46:19.087091-03	2025-07-10 10:24:10.665137-03	\N	\N	10	aee8ca47-d7e1-4729-b1e5-9fa23a28eedb	\N	\N	\N	19	\N	\N	\N	\N	\N	0	\N	unidad	t	\N	f	\N	\N	\N	\N	g
\.


--
-- Data for Name: publicidades; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.publicidades (id, item_publicitado_id, tipo_publicidad, fecha_inicio, fecha_fin, costo, usuario_id, estado, visualizaciones, clics, conversiones, fecha_creacion, fecha_actualizacion, nombre, item_publicitado_tipo) FROM stdin;
\.


--
-- Data for Name: recetas; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.recetas (id, nombre, descripcion, producto_id, negocio_id, creador_id, tiempo_preparacion, tiempo_coccion, temperatura_horno, rendimiento, unidad_rendimiento, dificultad, instrucciones, fecha_creacion, fecha_actualizacion) FROM stdin;
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.reviews (id, encargo_id, rating, comentario, fecha_review) FROM stdin;
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.usuarios (id, nombre, email, localizacion, info_contacto, tipo_tier, fecha_creacion, fecha_actualizacion, curriculum_vitae, hashed_password, is_active, plugins_activos, rol, negocio_asignado_id, fecha_contratacion, salario, horario_trabajo, permisos_especiales) FROM stdin;
aee8ca47-d7e1-4729-b1e5-9fa23a28eedb	Ismael	ismaeldimenza@hotmail.com	\N	null	MICROEMPRENDIMIENTO	2025-07-07 18:41:05.780587-03	2025-07-07 18:41:05.780587-03	\N	$2b$12$sKm4CeSROpr0bcrFcllOe.VjQOLDA3TVhFoj6hlXdcBVI6/s6WQEu	t	{}	\N	\N	\N	\N	\N	{}
39937ac4-5b47-4a5f-87fb-3fa0adcd2f5f	Usuario Test	test@example.com	\N	\N	MICROEMPRENDIMIENTO	2025-07-07 20:03:24.115235-03	2025-07-07 20:03:24.115235-03	\N	test_hash	t	{}	\N	\N	\N	\N	\N	{}
4106dbf0-69be-43a8-9f28-17e0dfcb31c3	Diseñador Creativo	disenador@ejemplo.com	Córdoba, Argentina	\N	FREELANCER	2025-07-08 01:29:04.103096-03	2025-07-08 01:29:04.103096-03	Diseñador gráfico y UX/UI con 8 años de experiencia. Especializado en branding, diseño web y aplicaciones móviles. Trabajo con startups y empresas establecidas.	$2b$12$v86S/dMZMrIXqQbwJjXjN.lsUtpCflsLjBEAXn18PBxPhEw2PlulO	t	{}	\N	\N	\N	\N	\N	{}
d3c0a59c-26e2-4f01-a222-c2e2452f4d02	Panadero Creativo	panadero@ejemplo.com	Buenos Aires, Argentina	\N	MICROEMPRENDIMIENTO	2025-07-08 01:29:05.196994-03	2025-07-08 01:29:05.196994-03	Panadero artesanal con 10 años de experiencia en panadería tradicional y moderna. Especializado en masas madre y pastelería fina.	$2b$12$8a/4.wheU90hLC/0LF2SkuQNNwx78JtyEpPm0zmz5ZJuxHTM6uAkW	t	{}	\N	\N	\N	\N	\N	{}
cd8d8f1d-089e-4231-9fe2-f4ac70fca878	Usuario Test Auth	test_auth@example.com	\N	\N	MICROEMPRENDIMIENTO	2025-07-08 23:52:26.677837-03	2025-07-08 23:52:26.677837-03	\N	$2b$12$Ksal.O3bXdn4fNwV.If5cOrBBsE4gHlRhZgeM2Gfv3.NhcgtZyOqq	t	{}	\N	\N	\N	\N	\N	{}
cf64095a-1646-4ffe-85f7-d1e35a79a43a	Usuario Test POS	test_pos@example.com	\N	\N	MICROEMPRENDIMIENTO	2025-07-08 23:53:18.138268-03	2025-07-08 23:53:18.138268-03	\N	$2b$12$ADAjdxqfCOQmnQWFjhEl5u19yDnZ31U.RMBHoM2dDT3XzerwV7bri	t	{}	\N	\N	\N	\N	\N	{}
\.


--
-- Data for Name: ventas; Type: TABLE DATA; Schema: public; Owner: soupuser
--

COPY public.ventas (id, negocio_id, cliente_id, numero_venta, fecha_venta, subtotal, descuento, impuestos, total, metodo_pago, estado, notas, margen_ganancia_total, costo_total) FROM stdin;
\.


--
-- Name: carritos_compra carritos_compra_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.carritos_compra
    ADD CONSTRAINT carritos_compra_pkey PRIMARY KEY (id);


--
-- Name: contactos contactos_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.contactos
    ADD CONSTRAINT contactos_pkey PRIMARY KEY (id);


--
-- Name: detalles_venta detalles_venta_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.detalles_venta
    ADD CONSTRAINT detalles_venta_pkey PRIMARY KEY (id);


--
-- Name: encargos encargos_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.encargos
    ADD CONSTRAINT encargos_pkey PRIMARY KEY (id);


--
-- Name: horarios_pico horarios_pico_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.horarios_pico
    ADD CONSTRAINT horarios_pico_pkey PRIMARY KEY (id);


--
-- Name: ingredientes_receta ingredientes_receta_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.ingredientes_receta
    ADD CONSTRAINT ingredientes_receta_pkey PRIMARY KEY (id);


--
-- Name: insumos insumos_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.insumos
    ADD CONSTRAINT insumos_pkey PRIMARY KEY (id);


--
-- Name: items_carrito items_carrito_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.items_carrito
    ADD CONSTRAINT items_carrito_pkey PRIMARY KEY (id);


--
-- Name: mensajes_registro mensajes_registro_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.mensajes_registro
    ADD CONSTRAINT mensajes_registro_pkey PRIMARY KEY (id);


--
-- Name: negocios negocios_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.negocios
    ADD CONSTRAINT negocios_pkey PRIMARY KEY (id);


--
-- Name: producciones producciones_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.producciones
    ADD CONSTRAINT producciones_pkey PRIMARY KEY (id);


--
-- Name: producto_insumo producto_insumo_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.producto_insumo
    ADD CONSTRAINT producto_insumo_pkey PRIMARY KEY (id);


--
-- Name: producto_insumos producto_insumos_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.producto_insumos
    ADD CONSTRAINT producto_insumos_pkey PRIMARY KEY (id);


--
-- Name: productos productos_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_pkey PRIMARY KEY (id);


--
-- Name: publicidades publicidades_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.publicidades
    ADD CONSTRAINT publicidades_pkey PRIMARY KEY (id);


--
-- Name: recetas recetas_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.recetas
    ADD CONSTRAINT recetas_pkey PRIMARY KEY (id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (id);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: ventas ventas_numero_venta_key; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT ventas_numero_venta_key UNIQUE (numero_venta);


--
-- Name: ventas ventas_pkey; Type: CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT ventas_pkey PRIMARY KEY (id);


--
-- Name: idx_carritos_negocio_id; Type: INDEX; Schema: public; Owner: soupuser
--

CREATE INDEX idx_carritos_negocio_id ON public.carritos_compra USING btree (negocio_id);


--
-- Name: idx_detalles_venta_id; Type: INDEX; Schema: public; Owner: soupuser
--

CREATE INDEX idx_detalles_venta_id ON public.detalles_venta USING btree (venta_id);


--
-- Name: idx_productos_categoria; Type: INDEX; Schema: public; Owner: soupuser
--

CREATE INDEX idx_productos_categoria ON public.productos USING btree (categoria);


--
-- Name: idx_productos_fecha_vencimiento; Type: INDEX; Schema: public; Owner: soupuser
--

CREATE INDEX idx_productos_fecha_vencimiento ON public.productos USING btree (fecha_vencimiento);


--
-- Name: idx_ventas_fecha; Type: INDEX; Schema: public; Owner: soupuser
--

CREATE INDEX idx_ventas_fecha ON public.ventas USING btree (fecha_venta);


--
-- Name: idx_ventas_negocio_id; Type: INDEX; Schema: public; Owner: soupuser
--

CREATE INDEX idx_ventas_negocio_id ON public.ventas USING btree (negocio_id);


--
-- Name: ix_usuarios_email; Type: INDEX; Schema: public; Owner: soupuser
--

CREATE UNIQUE INDEX ix_usuarios_email ON public.usuarios USING btree (email);


--
-- Name: carritos_compra carritos_compra_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.carritos_compra
    ADD CONSTRAINT carritos_compra_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.usuarios(id);


--
-- Name: carritos_compra carritos_compra_negocio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.carritos_compra
    ADD CONSTRAINT carritos_compra_negocio_id_fkey FOREIGN KEY (negocio_id) REFERENCES public.negocios(id);


--
-- Name: contactos contactos_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.contactos
    ADD CONSTRAINT contactos_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);


--
-- Name: detalles_venta detalles_venta_producto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.detalles_venta
    ADD CONSTRAINT detalles_venta_producto_id_fkey FOREIGN KEY (producto_id) REFERENCES public.productos(id);


--
-- Name: detalles_venta detalles_venta_venta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.detalles_venta
    ADD CONSTRAINT detalles_venta_venta_id_fkey FOREIGN KEY (venta_id) REFERENCES public.ventas(id);


--
-- Name: encargos encargos_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.encargos
    ADD CONSTRAINT encargos_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.contactos(id);


--
-- Name: encargos encargos_producto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.encargos
    ADD CONSTRAINT encargos_producto_id_fkey FOREIGN KEY (producto_id) REFERENCES public.productos(id);


--
-- Name: encargos encargos_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.encargos
    ADD CONSTRAINT encargos_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);


--
-- Name: horarios_pico horarios_pico_negocio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.horarios_pico
    ADD CONSTRAINT horarios_pico_negocio_id_fkey FOREIGN KEY (negocio_id) REFERENCES public.negocios(id);


--
-- Name: ingredientes_receta ingredientes_receta_insumo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.ingredientes_receta
    ADD CONSTRAINT ingredientes_receta_insumo_id_fkey FOREIGN KEY (insumo_id) REFERENCES public.insumos(id);


--
-- Name: ingredientes_receta ingredientes_receta_receta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.ingredientes_receta
    ADD CONSTRAINT ingredientes_receta_receta_id_fkey FOREIGN KEY (receta_id) REFERENCES public.recetas(id);


--
-- Name: insumos insumos_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.insumos
    ADD CONSTRAINT insumos_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);


--
-- Name: items_carrito items_carrito_carrito_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.items_carrito
    ADD CONSTRAINT items_carrito_carrito_id_fkey FOREIGN KEY (carrito_id) REFERENCES public.carritos_compra(id);


--
-- Name: items_carrito items_carrito_producto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.items_carrito
    ADD CONSTRAINT items_carrito_producto_id_fkey FOREIGN KEY (producto_id) REFERENCES public.productos(id);


--
-- Name: mensajes_registro mensajes_registro_contacto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.mensajes_registro
    ADD CONSTRAINT mensajes_registro_contacto_id_fkey FOREIGN KEY (contacto_id) REFERENCES public.contactos(id);


--
-- Name: mensajes_registro mensajes_registro_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.mensajes_registro
    ADD CONSTRAINT mensajes_registro_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);


--
-- Name: producciones producciones_negocio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.producciones
    ADD CONSTRAINT producciones_negocio_id_fkey FOREIGN KEY (negocio_id) REFERENCES public.negocios(id);


--
-- Name: producciones producciones_productor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.producciones
    ADD CONSTRAINT producciones_productor_id_fkey FOREIGN KEY (productor_id) REFERENCES public.usuarios(id);


--
-- Name: producciones producciones_receta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.producciones
    ADD CONSTRAINT producciones_receta_id_fkey FOREIGN KEY (receta_id) REFERENCES public.recetas(id);


--
-- Name: producto_insumo producto_insumo_insumo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.producto_insumo
    ADD CONSTRAINT producto_insumo_insumo_id_fkey FOREIGN KEY (insumo_id) REFERENCES public.insumos(id);


--
-- Name: producto_insumo producto_insumo_producto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.producto_insumo
    ADD CONSTRAINT producto_insumo_producto_id_fkey FOREIGN KEY (producto_id) REFERENCES public.productos(id);


--
-- Name: producto_insumos producto_insumos_insumo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.producto_insumos
    ADD CONSTRAINT producto_insumos_insumo_id_fkey FOREIGN KEY (insumo_id) REFERENCES public.insumos(id);


--
-- Name: producto_insumos producto_insumos_producto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.producto_insumos
    ADD CONSTRAINT producto_insumos_producto_id_fkey FOREIGN KEY (producto_id) REFERENCES public.productos(id);


--
-- Name: productos productos_negocio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_negocio_id_fkey FOREIGN KEY (negocio_id) REFERENCES public.negocios(id);


--
-- Name: productos productos_propietario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_propietario_id_fkey FOREIGN KEY (propietario_id) REFERENCES public.usuarios(id);


--
-- Name: publicidades publicidades_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.publicidades
    ADD CONSTRAINT publicidades_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);


--
-- Name: recetas recetas_creador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.recetas
    ADD CONSTRAINT recetas_creador_id_fkey FOREIGN KEY (creador_id) REFERENCES public.usuarios(id);


--
-- Name: recetas recetas_negocio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.recetas
    ADD CONSTRAINT recetas_negocio_id_fkey FOREIGN KEY (negocio_id) REFERENCES public.negocios(id);


--
-- Name: recetas recetas_producto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.recetas
    ADD CONSTRAINT recetas_producto_id_fkey FOREIGN KEY (producto_id) REFERENCES public.productos(id);


--
-- Name: reviews reviews_encargo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_encargo_id_fkey FOREIGN KEY (encargo_id) REFERENCES public.encargos(id);


--
-- Name: usuarios usuarios_negocio_asignado_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_negocio_asignado_id_fkey FOREIGN KEY (negocio_asignado_id) REFERENCES public.negocios(id);


--
-- Name: ventas ventas_cliente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT ventas_cliente_id_fkey FOREIGN KEY (cliente_id) REFERENCES public.usuarios(id);


--
-- Name: ventas ventas_negocio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: soupuser
--

ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT ventas_negocio_id_fkey FOREIGN KEY (negocio_id) REFERENCES public.negocios(id);


--
-- PostgreSQL database dump complete
--

