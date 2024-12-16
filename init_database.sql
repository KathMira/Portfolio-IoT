create table if not exists Temperaturas(
id varchar (100) primary key,
room_id varchar (100) not null,
noted_date timestamp not null,
temperature int not null,
out_in char (3) not null
);

CREATE VIEW media_temperatura_salas_por_dia AS
SELECT room_id, AVG(temperature) as avg_temp, date(noted_date), out_in
FROM Temperaturas
GROUP BY room_id, date(noted_date), out_in
order by date(noted_date);

create VIEW media_temperatura_externa_no_dia_por_mes as
SELECT room_id, avg(temperature) as avg_temp, extract (hour from noted_date) as hour, to_char(noted_date, 'MM-YYYY') as month
FROM Temperaturas
where out_in = 'Out'
GROUP BY room_id, EXTRACT(hour from noted_date),to_char(noted_date, 'MM-YYYY')
order by to_char(noted_date, 'MM-YYYY'), extract (hour from noted_date);

create VIEW media_temperatura_interna_no_dia_por_mes as
SELECT room_id, avg(temperature) as avg_temp, extract (hour from noted_date) as hour, to_char(noted_date, 'MM-YYYY') as month
FROM Temperaturas
where out_in = 'In'
GROUP BY room_id, EXTRACT(hour from noted_date),to_char(noted_date, 'MM-YYYY')
order by to_char(noted_date, 'MM-YYYY'), extract (hour from noted_date);
