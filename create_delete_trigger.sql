CREATE OR REPLACE FUNCTION public.delete_func() RETURNS TRIGGER AS $shadow_audit2$
    declare event_id int;

begin
    event_id := nextval('public.trigger_seq');
    
        --id
        if(OLD.id is not NULL) then 
            INSERT INTO public.sdl_audit SELECT event_id, 'public.test_delete', OLD.row_id, 'protocol_id', OLD.id, null, old.modified_by, now();
        end if;
        --id_2
        if(OLD.id_2 is not NULL) then 
            INSERT INTO public.sdl_audit SELECT event_id, 'public.test_delete', OLD.row_id, 'protocol_id', OLD.id_2, null, old.modified_by, now();
        end if;
        --id_3
        if(OLD.id_3 is not NULL) then 
            INSERT INTO public.sdl_audit SELECT event_id, 'public.test_delete', OLD.row_id, 'protocol_id', OLD.id_3, null, old.modified_by, now();
        end if;
        --id_4
        if(OLD.id_4 is not NULL) then 
            INSERT INTO public.sdl_audit SELECT event_id, 'public.test_delete', OLD.row_id, 'protocol_id', OLD.id_4, null, old.modified_by, now();
        end if;
        --id_5
        if(OLD.id_5 is not NULL) then 
            INSERT INTO public.sdl_audit SELECT event_id, 'public.test_delete', OLD.row_id, 'protocol_id', OLD.id_5, null, old.modified_by, now();
        end if;
        --id_6
        if(OLD.id_6 is not NULL) then 
            INSERT INTO public.sdl_audit SELECT event_id, 'public.test_delete', OLD.row_id, 'protocol_id', OLD.id_6, null, old.modified_by, now();
        end if;
        RETURN NULL;
    END;
$shadow_audit2$ LANGUAGE plpgsql;

---Delete trigger
CREATE TRIGGER public.delete_trigger
    after delete on public.test_delete
    FOR EACH ROW EXECUTE FUNCTION public.delete_func();
    
    