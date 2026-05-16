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
        DROP POLICY IF EXISTS tenant_isolation_policy ON {table};
        CREATE POLICY tenant_isolation_policy ON {table}
        AS PERMISSIVE
        FOR ALL
        USING (
            current_setting('app.current_org_id', true) = '' 
            OR organization_id = NULLIF(current_setting('app.current_org_id', true), '')::integer
        )
        WITH CHECK (
            current_setting('app.current_org_id', true) = '' 
            OR organization_id = NULLIF(current_setting('app.current_org_id', true), '')::integer
        );
        """
        
        # for down migration, we would revert to the previous one, but typically down is not strict about exactly the bad one. 
        # Just putting drop is fine for down if needed since this is a patch.
        sql_down += f"""
        DROP POLICY IF EXISTS tenant_isolation_policy ON {table};
        """
        
    return sql_up, sql_down

class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_organization_client_email_and_more'),
    ]

    sql_up, sql_down = get_rls_sql()

    operations = [
        migrations.RunSQL(sql_up, sql_down)
    ]
