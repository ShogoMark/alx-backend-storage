-- SQL that creates trigger that decreases
-- the quantity of an item when orders are placed

DROP TRIGGER IF EXISTS items_reducer;
DELIMITER !!
CREATE TRIGGER items_reducer
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
	UPDATE items
	SET quantity = quantity - NEW.number
	WHERE name = NEW.item_name;
END!!
DELIMITER ;
