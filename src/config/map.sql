

SELECT id FROM episodes WHERE id = %s;
SELECT id FROM characters WHERE id = %s;
SELECT id FROM locations WHERE id = %s;

INSERT INTO episodes(id, name, episode) VALUES (%s, %s, %s);
INSERT INTO characters(id, name, status, species, gender, origin, location, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
INSERT INTO locations(id, name, type, dimension) VALUES (%s, %s, %s ,%s);
