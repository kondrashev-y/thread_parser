import sqlalchemy as sa

metadata = sa.MetaData()
connection = {'user': '...', 'database': '...', 'host': '...', 'password': '..'}
dsn = 'postgresql://{user}:{password}@{host}/{database}'.format(**connection)


Page = sa.Table(
    'pars_page', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('url', sa.String),
    sa.Column('title', sa.String),
    sa.Column('h1', sa.String),
    sa.Column('description', sa.Text),
    sa.Column('page_size', sa.Integer),
    sa.Column('load_time', sa.Float)
)


if __name__ == '__main__':
    engine = sa.create_engine(dsn)
    # metadata.drop_all(engine)
    metadata.create_all(engine)
