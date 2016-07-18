create or replace function comments_update_counter() returns trigger as $$
  declare
    row_story_id integer;
  begin
    if (TG_OP = 'INSERT') then
      row_story_id := new.story_id;
    elsif (TG_OP = 'DELETE' or TG_OP = 'UPDATE') then
      row_story_id := old.story_id;
    end if;

    update stories set comments_count = (select count(*) from comments where story_id = stories.id) where id = row_story_id;
    return null;
  end;
$$ language plpgsql;

drop trigger if exists comments_update_counter_trigger on comments;

create trigger comments_update_counter_trigger
after insert or delete
on comments
for each row
execute procedure comments_update_counter();
