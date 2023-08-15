drop function if exists get_avg_per_class;
CREATE OR REPLACE FUNCTION get_avg_per_class(
	data_tbl_name TEXT
,	cols VARCHAR[]
,	avg_tbl_name TEXT
,	avgs numeric[]
,	condit text
,	avg_tbl_pk text
)
RETURNS VOID AS $$
DECLARE
	col_names TEXT := array_to_string(cols, ', ');
	col_decls TEXT;
	col_avg_sel TEXT;
    col_selects TEXT;
	avgs_text TEXT;
    table_exists boolean;
BEGIN

	SELECT string_agg('avg(' || col::text || ')', ', ') INTO col_avg_sel
    FROM unnest(cols) AS col;

    IF avgs IS NULL OR array_length(avgs, 1) IS NULL THEN
        EXECUTE format('SELECT array[%s] FROM %I %s', col_avg_sel, data_tbl_name, condit) INTO avgs;
	END IF;
	SELECT string_agg(col::text || ' numeric', ', ') INTO col_decls FROM unnest(cols) AS col;
	EXECUTE format('SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %L)', avg_tbl_name)
    	INTO table_exists;
	if not table_exists then
		EXECUTE format('CREATE TABLE %I (%s)', avg_tbl_name, col_decls);
		EXECUTE format('ALTER TABLE %I ADD COLUMN %I serial PRIMARY KEY', avg_tbl_name, avg_tbl_pk);
	end if;

	SELECT string_agg('' || av::numeric, ', ') INTO avgs_text FROM unnest(avgs) AS av;

	col_selects := REPLACE(col_decls, ' numeric', '');
    EXECUTE format('INSERT INTO %I (%s) VALUES (%s)', avg_tbl_name, col_selects, avgs_text) USING avgs;
END;
$$ LANGUAGE plpgsql;

drop function if exists get_covar;
CREATE OR REPLACE FUNCTION get_covar(
	data_tbl_name TEXT
,	cols VARCHAR[]
,	avg_tbl_name TEXT
,	covar_tbl_name TEXT
,	data_condit TEXT
,	avg_condit TEXT
)
RETURNS VOID AS $$
DECLARE
	col_names TEXT := array_to_string(cols, ', ');
	col_decls TEXT;
	col_avg_sel TEXT;
    col_selects TEXT;
	avgs_text TEXT;
	dot_product numeric;
	a_mean numeric;
	b_mean numeric;
	pk_name TEXT := 'PK_COL';
BEGIN
	SELECT string_agg(col::text || ' numeric', ', ') INTO col_decls FROM unnest(cols) AS col;
    EXECUTE format('DROP TABLE IF EXISTS %I', covar_tbl_name);
	EXECUTE format('CREATE TABLE %I (%s)', covar_tbl_name, col_decls);
	EXECUTE format( -- 	Populate covar_tbl with a square of zeros
		'INSERT INTO %I (%s) SELECT %s FROM generate_series(1, %s) AS x',
		covar_tbl_name,
		array_to_string(cols, ', '),
		array_to_string(array_fill('0'::text, array[array_length(cols, 1)]), ', '),
		array_length(cols, 1)
	);
    EXECUTE format('ALTER TABLE %I ADD COLUMN %I serial PRIMARY KEY', covar_tbl_name, pk_name);

    FOR i IN 1..array_length(cols, 1) LOOP
		EXECUTE format('SELECT %I FROM %I %s LIMIT 1', cols[i], avg_tbl_name, avg_condit) INTO a_mean;
        FOR j IN i..array_length(cols, 1) LOOP
			EXECUTE format('SELECT %I FROM %I %s LIMIT 1', cols[j], avg_tbl_name, avg_condit) INTO b_mean;
			EXECUTE format('SELECT SUM((%I - $1) * (%I - $2)) FROM %I %s',
						   cols[i], cols[j], data_tbl_name, data_condit)
			INTO dot_product USING a_mean, b_mean;

			EXECUTE format('UPDATE %I SET %I = $1 WHERE %I = $2',
        		covar_tbl_name, cols[i], pk_name)
    			USING dot_product, j;
			if i <> j then
				EXECUTE format('UPDATE %I SET %I = $1 WHERE %I = $2',
							   covar_tbl_name, cols[j], pk_name) USING dot_product, i;
			end if;
        END LOOP;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
