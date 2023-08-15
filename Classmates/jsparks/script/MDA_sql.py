import datetime

import numpy as np
import psycopg2 as pg

# This file defines and invokes PostgreSQL functions
# Using the generated covar matrices, MDA is performed on a subset of a table
# For example, on the table natalityConf WHERE valid is TRUE

db_params = {
    'database': 'USA',
    'user': 'postgres',
    'password': 'password',
    'port': '5435'
}

table_name = '"natalityConf"'
conn = pg.connect(**db_params)
cur = conn.cursor()

cur.execute("SET search_path TO 'USA';")
conn.commit()

with open("fct_defs.sql", 'r') as file:
    sql_script = file.read()
cur.execute(sql_script)
conn.commit()


def prepare_queries():
    global declarations, get_avgs, get_covar, get_total_avg, drop_ave_tbl, pop_var_from_cols, REPL_TXT
    global query_template
    declarations, get_avgs, get_covar = "", "", []
    for i in range(1, len(conditions)+1):
        declarations += f"class{i}_condition text:='{conditions[i-1]}';\n"
        declarations += f"class{i}_covar_tbl_name text:='temp_class_{i}_covar';\n"
        get_avgs += f"perform get_avg_per_class(data_tbl_name,cols,avg_tbl_name,array[]::numeric[],class{i}_condition,pk_col);\n"
        get_covar.append(f"perform get_covar(data_tbl_name,cols,avg_tbl_name,class{i}_covar_tbl_name,class{i}_condition,'where cat={i}');")
    get_total_avg = f"perform get_avg_per_class(data_tbl_name,cols,'{total_avg_name}',array[]::numeric[],'{condit}','cat');"
    # get_all_var_covar = f"perform get_covar(data_tbl_name,cols,'{total_avg_name}',{all_var_covar_name},'{condit}','');"
    drop_ave_tbl = "EXECUTE format('DROP TABLE IF EXISTS %I', avg_tbl_name);"
    pop_var_from_cols = "cols := array_remove(cols, classification_var);"
    REPL_TXT = f"%%{np.random.randint(2147483647, size=(1)).item()}%%"
    query_template = f'''
    do $$ declare
        cols text[]:=array[{"'" + "','".join(cols) + "'"}];
        classification_var text:='{classification_var}';
    	data_tbl_name text:='{table_name}';
    	avg_tbl_name text:='{avg_tbl_name}';
    	pk_col text:='cat'; 
        {declarations}
    begin {REPL_TXT} end; $$
    '''

def run_query(query: str):
    cur.execute(query_template.replace(REPL_TXT, query))
    conn.commit()

def print_times():
    global last_time
    iter_time = str(datetime.datetime.now() - last_time).split(".")[0]
    last_time = datetime.datetime.now()
    total_time = str(datetime.datetime.now() - start_time).split(".")[0]
    print(f"Time elapsed: {iter_time}, total time: {total_time}")

def run_sql():
    global last_time
    global start_time
    start_time = datetime.datetime.now()
    last_time = start_time
    print("*"*55)
    print(f'Start time: {start_time.strftime("%b %d at %H:%M:%S")}')
    print("Computing means of all data")
    run_query(f"{pop_var_from_cols} {drop_ave_tbl} {get_total_avg}")
    print_times()
    print("Computing means of each category")
    run_query(f"{pop_var_from_cols} {get_avgs}")
    print_times()
    for i in range(1, len(conditions)+1):
        print(f"Computing covar matrix for category {i}")
        run_query(f"{pop_var_from_cols} {get_covar[i-1]}")
        print_times()


def drop_temp_tbls():
    tables = [total_avg_name, avg_tbl_name]
    for i in range(1, len(conditions) + 1):
        tables. append(f"temp_class_{i}_covar")
    query = ""
    for t in tables:
        query += f"drop table if exists {t};"
    cur.execute(query)
    conn.commit()

def fetch_computations():
    global m, m_i, S_i
    cols_ = cols.copy()
    cols_.pop(cols_.index(classification_var))

    cur.execute(f"SELECT {','.join(cols_)} FROM {total_avg_name};")
    m = np.array(cur.fetchall(), dtype=np.float64)

    cur.execute(f"SELECT {','.join(cols_)} FROM {avg_tbl_name} order by cat;")
    m_i = np.array(cur.fetchall(), dtype=np.float64)
    S_i = []
    for i in range(1, len(conditions)+1):
        cur.execute(f"SELECT {','.join(cols_)} FROM temp_class_{i}_covar order by \"PK_COL\";")
        S_i.append(np.array(cur.fetchall(), dtype=np.float64))
        # print(f"S_{i} = {S_i[i-1]}")

def store_computations(prefix: str):
    np.save(f"{prefix}_m.npy",m)
    np.save(f"{prefix}_m_i.npy",m_i)
    np.save(f"{prefix}_S_i.npy",S_i)

def load_computations(prefix: str):
    global m, m_i, S_i
    m = np.load(f"{prefix}_m.npy")
    m_i = np.load(f"{prefix}_m_i.npy")
    S_i = np.load(f"{prefix}_S_i.npy")

def fetch_data(condition: str, max_rows: int, random: bool = True):
    cols_ = cols.copy()
    cols_.pop(cols_.index(classification_var))
    r = "order by random()" if random else ""
    cur.execute(f"SELECT {','.join(cols_)} FROM {table_name} {condition} {r} limit {max_rows};")
    return np.array(cur.fetchall(), dtype=np.float64)


# table_name = 'natal500k'
cols = ['in_resident', 'id_sex', 'id_f_race', 'id_m_race', 'am_m_age', 'am_tot_b_order', 'am_f_age', 'am_birthweight', 'am_gestation', 'id_m_edu', 'id_f_edu', 'am_prenatal', 'am_post_full_dob', 'am_lunar_month_dob', 'days_since_1969']
avg_tbl_name = 'temp_mld_avg_per_class'
total_avg_name = 'temp_total_data_avg'
# all_var_covar_name = 'temp_all_var_covar'
condit = 'where valid is true'

def run_and_store(prefix: str):
    prepare_queries()
    run_sql()
    fetch_computations()
    store_computations(prefix)
    drop_temp_tbls()

# Run 1

topic = '2_class_birthweight'
print(f"Computing for {topic}")
classification_var = 'am_birthweight'
class_1_condit = f'{condit} and {classification_var}<2500'
class_2_condit = f'{condit} and {classification_var}>=2500'
conditions = [class_1_condit, class_2_condit]
run_and_store(topic)

# Run 2

topic = '2_class_sex'
print(f"Computing for {topic}")
classification_var = 'id_sex'
class_1_condit = f'{condit} and {classification_var}=1'
class_2_condit = f'{condit} and {classification_var}=2'
conditions = [class_1_condit, class_2_condit]
run_and_store(topic)

# Run 3

topic = '7_class_birthweight'
print(f"Computing for {topic}")
classification_var = 'am_birthweight'
class_1_condit = f'{condit} and {classification_var} < 1250'
class_2_condit = f'{condit} and {classification_var} between 1250 and 2499'
class_3_condit = f'{condit} and {classification_var} between 2500 and 3749'
class_4_condit = f'{condit} and {classification_var} between 3750 and 4999'
class_5_condit = f'{condit} and {classification_var} between 5000 and 6249'
class_6_condit = f'{condit} and {classification_var} between 6250 and 7499'
class_7_condit = f'{condit} and {classification_var} > 7499'
conditions = [class_1_condit, class_2_condit, class_3_condit, class_4_condit,
              class_5_condit, class_6_condit, class_7_condit]
run_and_store(topic)




# Visualization


# print(fetch_data(conditions[0], 20, False))
# fetch_computations()
# store_computations('test')
load_computations('test')
print(m)
print(S_i)
print(m_i)

'''
{pop_var_from_cols}
{drop_ave_tbl}
{get_total_avg}
{get_avgs}
{get_covar}
'''

# run_sql()
# drop_temp_tbls()

# Retrieve data from SQL tables


# {pop_var_from_cols}
# {drop_ave_tbl}
# {get_total_avg}
# {get_avgs}
# {get_covar[0]}


# Store tables as Numpy objects, perform MDA

# drop_temp_tbls()

cur.close()
conn.close()
