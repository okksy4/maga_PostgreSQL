/*
ФИО: Абрамова Оксана Васильевна
Вариант: 3
Задание:
Описание хранящихся на складе товаров. Включает в себя: описание помещений, описание стеллажей, 
описание клиентов, описание товаров, хранящихся на стеллажах. Описание помещения состоит из: 
названия, полезного объёма, температурных и влажностных условий. Описание стеллажа состоит из: 
номера, указания помещения, в котором стеллаж находится, количества мест для хранения в стеллаже, 
высоты, ширины и длины одного места, максимальной суммарной нагрузки. Описание клиента состоит из: 
названия юридического лица и банковских реквизитов в виде большого текста. Описание товара, 
хранящегося на стеллажах, состоит из: высоты, ширины, длины, веса, даты поступления, 
номера договора, указания, от какого клиента поступил, даты окончания договора, 
температурных и влажностных условий хранения, указания стеллажа, и позиции размещения на нём, 
представляемой в виде целого номера.
На одном стеллаже могут храниться товары только одного клиента.
*/

DROP TABLE IF EXISTS goods;
DROP TABLE IF EXISTS rack_lease;
DROP TABLE IF EXISTS rack;
DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS room;

CREATE TABLE room
(
    id serial,
    name character varying(100) NOT NULL,
    useful_volume numeric(10, 2) NOT NULL,
    min_temp numeric(5, 1) NOT NULL,
    max_temp numeric(5, 1) NOT NULL,
    min_humidity numeric(5, 1) NOT NULL,
    max_humidity numeric(5, 1) NOT NULL,
    CONSTRAINT room_pkey PRIMARY KEY (id),
    CONSTRAINT uq_room_name UNIQUE (name),
    CONSTRAINT ck_room_volume CHECK (useful_volume > 0),
    CONSTRAINT ck_room_temp CHECK (min_temp <= max_temp),
    CONSTRAINT ck_room_humidity_range CHECK (min_humidity >= 0 AND max_humidity <= 100),
    CONSTRAINT ck_room_humidity_order CHECK (min_humidity <= max_humidity)
);

CREATE TABLE client
(
    id serial,
    legal_name character varying(200) NOT NULL,
    bank_details text NOT NULL,
    CONSTRAINT client_pkey PRIMARY KEY (id),
    CONSTRAINT uq_client_legal_name UNIQUE (legal_name),
    CONSTRAINT ck_client_name CHECK (length(legal_name) > 0)
);

CREATE TABLE rack
(
    id serial,
    room_id integer NOT NULL,
    rack_number integer NOT NULL,
    places integer NOT NULL,
    place_height numeric(6, 2) NOT NULL,
    place_width numeric(6, 2) NOT NULL,
    place_length numeric(6, 2) NOT NULL,
    max_load numeric(10, 2) NOT NULL,
    CONSTRAINT rack_pkey PRIMARY KEY (id),
    CONSTRAINT uq_rack_number_in_room UNIQUE (room_id, rack_number),
    CONSTRAINT fk_rack_room FOREIGN KEY (room_id)
        REFERENCES room (id),
    CONSTRAINT ck_rack_number CHECK (rack_number > 0),
    CONSTRAINT ck_rack_places CHECK (places > 0),
    CONSTRAINT ck_rack_place_size CHECK (
        place_height > 0 AND place_width > 0 AND place_length > 0
    ),
    CONSTRAINT ck_rack_load CHECK (max_load > 0)
);

/* таблицу rack_lease создала для соблюдения условия в задании:
"На одном стеллаже могут храниться товары только одного клиента."
*/

CREATE TABLE rack_lease
(
    rack_id integer NOT NULL,
    client_id integer NOT NULL,
    CONSTRAINT pk_rack_lease PRIMARY KEY (rack_id),
    CONSTRAINT uq_lease_pair UNIQUE (rack_id, client_id),
    CONSTRAINT fk_lease_rack FOREIGN KEY (rack_id)
        REFERENCES rack (id),
    CONSTRAINT fk_lease_client FOREIGN KEY (client_id)
        REFERENCES client (id)
);

CREATE TABLE goods
(
    id serial,
    height numeric(6, 2) NOT NULL,
    width numeric(6, 2) NOT NULL,
    length numeric(6, 2) NOT NULL,
    weight numeric(10, 2) NOT NULL,
    receipt_date date NOT NULL DEFAULT CURRENT_DATE,
    contract_number character varying(50) NOT NULL,
    contract_end_date date NOT NULL,
    storage_min_temp numeric(5, 1) NOT NULL,
    storage_max_temp numeric(5, 1) NOT NULL,
    storage_min_humidity numeric(5, 1) NOT NULL,
    storage_max_humidity numeric(5, 1) NOT NULL,
    rack_id integer NOT NULL,
    client_id integer NOT NULL,
    place_number integer NOT NULL,
    CONSTRAINT goods_pkey PRIMARY KEY (id),
    CONSTRAINT uq_place_on_rack UNIQUE (rack_id, place_number),
    CONSTRAINT fk_goods_lease FOREIGN KEY (rack_id, client_id)
        REFERENCES rack_lease (rack_id, client_id),
    CONSTRAINT ck_goods_size CHECK (height > 0 AND width > 0 AND length > 0),
    CONSTRAINT ck_goods_weight CHECK (weight > 0),
    CONSTRAINT ck_goods_contract CHECK (contract_end_date >= receipt_date),
    CONSTRAINT ck_goods_temp CHECK (storage_min_temp <= storage_max_temp),
    CONSTRAINT ck_goods_humidity_range CHECK (
        storage_min_humidity >= 0 AND storage_max_humidity <= 100
    ),
    CONSTRAINT ck_goods_humidity_order CHECK (storage_min_humidity <= storage_max_humidity),
    CONSTRAINT ck_goods_place CHECK (place_number > 0)
);
