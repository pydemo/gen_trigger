CREATE OR REPLACE FUNCTION {func_name}() RETURNS TRIGGER AS $shadow_audit2$
    declare event_id int;

begin
    event_id := nextval('{sequence_name}');
    {if_list}
        RETURN NULL;
    END;
$shadow_audit2$ LANGUAGE plpgsql;

---Delete trigger
CREATE TRIGGER {trigger_name}
    after delete on {table_name}
    FOR EACH ROW EXECUTE FUNCTION {func_name}();
    
    