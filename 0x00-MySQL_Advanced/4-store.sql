-- Task: Create a trigger to decrease the quantity of an item

DELIMITER //

CREATE TRIGGER decrease_quantity_after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
   UPDATE items
   SET quantity = quantity - NEW.number
   WHERE item_id = NEW.item_id;
END;//

DELIMITER ;
