/*
ФИО: Абрамова Оксана Васильевна
Вариант: 3
Задание:
Выберите номера стеллажей, а также объём одного места 
и суммарный объём всех мест на каждом из них.
Выберите номера помещений и суммарный объём всех мест 
всех стеллажей в каждом из них, оставив только те помещения,
 суммарный объем всех стеллажей которых больше 50 м3.
*/
-- ==================структура БД=====================================================
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

-- ===============================данные в БД=================================================

INSERT INTO room (name, useful_volume, min_temp, max_temp, 
                  min_humidity, max_humidity) VALUES
('Склад1', 1000.00,   0.0,  30.0, 50.0, 75.0),
('Склад2',  500.00, -18.0,   5.0, 60.0, 95.0),
('Склад3', 1500.00,   2.0,   5.0, 60.0, 95.0),
('Склад4',  750.00, -10.0,  40.0, 50.0, 98.0),
('Склад5', 1500.00,  10.0,  30.0, 55.0, 70.0),
('Склад6', 1000.00, -18.0,   5.0, 50.0, 75.0),
('Склад7',  110.00, -30.0, -18.0, 75.0, 98.0);


INSERT INTO client (legal_name, bank_details) VALUES
('ООО «СеверСтройТорг»',
 'Р/с 40702810900010012345 в АО «Примсоцбанк», БИК 040410999, ИНН 2508123456, КПП 250801001'),
('ООО «Восток-Логистика»',
 'Р/с 40702810600020098765 в АО «Альфа-Банк», БИК 044525593, ИНН 7701234567, КПП 770101001'),
('ИП Кузнецова Марина Викторовна',
 'Р/с 40802810300030055443 в ПАО «Сбербанк», БИК 044525225, ИНН 771099876543'),
('ООО «Галерея бытовой техники»',
 'Р/с 40702810500040011223 в АО «Тинькофф Банк», БИК 044525974, ИНН 5004111223, КПП 500401001'),
('ООО «ВладТоргСервис»',
 'Р/с 40702810400050066778 в АО «Банк Приморье», БИК 040410000, ИНН 2539223344, КПП 253901001'),
('ООО «БумКанцелярия»',
 'Р/с 40702810200060033445 в АО «ВТБ», БИК 044525187, ИНН 7802555666, КПП 780201001'),
('ИП Смирнов Артём Олегович',
 'Р/с 40802810100070077665 в АО «Райффайзенбанк», БИК 044525700, ИНН 540133344455');


INSERT INTO rack (room_id, rack_number, places, place_height, 
                  place_width, place_length, max_load) VALUES
(1, 1, 20, 1.80, 1.00, 1.20, 350.00),
(1, 2, 20, 1.80, 1.00, 1.20, 350.00),
(2, 1, 45, 2.00, 0.80, 1.00, 200.00),
(3, 1, 12, 1.50, 1.20, 1.50, 500.00),
(4, 1, 24, 1.60, 0.90, 1.10, 300.00),
(5, 1, 18, 1.20, 0.60, 0.80, 150.00),
(6, 1, 40, 1.90, 0.70, 1.00, 250.00);


INSERT INTO rack_lease (rack_id, client_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7);

INSERT INTO goods (height, width, length, weight, receipt_date, 
                   contract_number, contract_end_date, storage_min_temp, 
                   storage_max_temp, storage_min_humidity, storage_max_humidity,
                   rack_id, client_id, place_number) VALUES
(1.20, 0.60, 0.80, 85.50, '2026-10-12', 'Д-2026-014', '2027-10-11', 10.0, 22.0, 35.0, 60.0, 1, 1, 1),
(0.80, 0.50, 0.60, 24.00, '2026-10-18', 'Д-2024-021', '2027-04-17',  9.0, 23.0, 40.0, 60.0, 2, 2, 3),
(1.00, 0.90, 1.10, 120.00,'2026-09-05', 'Д-2026-008', '2027-09-04', 16.0, 28.0, 42.0, 58.0, 3, 3, 1),
(0.45, 0.35, 0.55, 18.50, '2026-11-01', 'Д-2018-043', '2027-05-31', 16.0, 29.0, 40.0, 58.0, 4, 4, 2),
(0.30, 0.25, 0.40,  4.20, '2026-10-25', 'Д-2026-036', '2027-10-24', 15.0, 24.0, 30.0, 44.0, 5, 5, 1),
(0.15, 0.21, 0.30,  6.80, '2026-10-30', 'Д-2020-051', '2027-04-29', 12.0, 21.0, 38.0, 52.0, 6, 6, 5),
(0.60, 0.40, 0.50, 12.30, '2026-11-06', 'Д-2011-058', '2027-11-05', 11.0, 25.0, 35.0, 65.0, 7, 7, 4);

-- =====================================запросы======================================================

SELECT 
	rack_number,
	place_height * place_width * place_length AS volume_place,
	place_height * place_width * place_length * places AS volume_rack
	
FROM	
	rack
;


SELECT   
	room_id,
	SUM(place_height * place_width * place_length * places) AS total_volume_room
FROM	
	rack
GROUP BY
	room_id
HAVING  
	SUM(place_height * place_width * place_length * places) > 50
;