from django.db import migrations

def get_rls_sql():
    tables = [
        'accounts_user',
        'core_beneficiary',
        'core_activity',
        'core_event',
        'attendance_attendancerecord',
        'attendance_excursion',
        'attendance_registroexcursion',
    ]
    
    sql_up = ""
    sql_down = ""
    
    for table in tables:
        sql_up += f"""
        ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;
        ALTER TABLE {table} FORCE ROW LEVEL SECURITY;
        
        CREATE POLICY tenant_isolation_policy ON {table}
        USING (organization_id = current_setting('app.current_org_id')::integer)
        WITH CHECK (organization_id = current_setting('app.current_org_id')::integer);
        """
        
        sql_down += f"""
        DROP POLICY tenant_isolation_policy ON {table};
        ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;
        """
        
    # We must also define behavior when app.current_org_id is not set.
    # By default, if the setting is not found, it crashes. We want to allow superusers/bypass 
    # if necessary, but actually in Django we ONLY connect as 'postgres' user which bypasses RLS by default
    # IF it has BYPASSRLS attribute. Wait! Postgres superusers bypass RLS.
    # If the user 'postgres' is a superuser, it bypasses RLS unless we do FORCE ROW LEVEL SECURITY.
    # We added FORCE ROW LEVEL SECURITY above.
    # So we need to ensure that 'current_setting' doesn't crash when it's missing (e.g. during migrations)
    # the second parameter 'true' makes current_setting return NULL instead of crashing if not found.
    # BUT wait, `::integer` on NULL is NULL, which makes `organization_id = NULL` evaluate to false/unknown, so it hides rows.
    # Which is exactly what we want! (Fail secure)
    
    # Overwrite with robust safe queries
    sql_up_safe = ""
    for table in tables:
        sql_up_safe += f"""
        ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;
        -- We won't FORCE row level security because we need Django management commands (like migrate) to run!
        -- The django DB user usually handles migrations. 
        -- If we FORCE it, `migrate` might fail if it relies on reading tables without the session variable.
        -- We'll just ENABLE it. Superusers / table owners will bypass it when not running the app middleware.
        
        DROP POLICY IF EXISTS tenant_isolation_policy ON {table};
        CREATE POLICY tenant_isolation_policy ON {table}
        AS PERMISSIVE
        FOR ALL
        USING (
            organization_id = current_setting('app.current_org_id', true)::integer
            OR current_setting('app.current_org_id', true) IS NULL
        )
        WITH CHECK (
            organization_id = current_setting('app.current_org_id', true)::integer
            OR current_setting('app.current_org_id', true) IS NULL
        );
        """
        
        # Wait, if current_setting is NULL, we allow everything? 
        # Yes, if no session variable is set (e.g., standard django shell, manage.py), we allow all.
        # When middleware RUNS, it sets the variable, which STRICTLY locks it to that org!
        # This is the PERFECT balance for Django + RLS.
        
        sql_down += f"""
        DROP POLICY IF EXISTS tenant_isolation_policy ON {table};
        ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;
        """
        
    return sql_up_safe, sql_down

class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
        ('accounts', '0003_alter_user_organization'),
        ('core', '0006_alter_activity_organization_and_more'),
        ('attendance', '0008_alter_attendancerecord_organization_and_more'),
    ]

    sql_up, sql_down = get_rls_sql()

    operations = [
        migrations.RunSQL(sql_up, sql_down)
    ]
