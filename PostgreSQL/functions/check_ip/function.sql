create or replace function public.check_ip()
returns void as $$
declare
client_ip text;
allowed_ips text[] := array['0.0.0.0', '8.8.8.8'];
begin
client_ip := current_setting('request.headers', true)::json->>'x-forwarded-for';

if client_ip is null or not (client_ip = any(allowed_ips)) then
    raise exception 'Unauthorized IP: %', client_ip
    using hint = 'Access denied';
end if;
end;
$$ language plpgsql;

-- Then run 2 commands:
-- alter role authenticator set pgrst.db_pre_request to 'public.check_ip';
-- notify pgrst, 'reload config';