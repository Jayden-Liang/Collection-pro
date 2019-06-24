import click
from sqlalchemy_utils import database_exists, create_database
from project.extensions import db
from project.blueprints.user.models import User, Role
from project.app import create_app

# Create an app context for the database connection.
app = create_app()
db.app = app


@click.group()
def cli():
    """ Run PostgreSQL related tasks. """
    pass


@click.command()
@click.option('--with-testdb/--no-with-testdb', default=False,
              help='Create a test db too?')
def init(with_testdb):
    """
    初始化，如果传入参数则创建测试数据库

    :param with_testdb: Create a test database
    :return: None
    """
    db.drop_all()
    db.create_all()

    if with_testdb:
        db_uri = '{0}_test'.format(app.config['SQLALCHEMY_DATABASE_URI'])
        if not database_exists(db_uri):
            create_database(db_uri)
            print('创建了测试数据库')

    return None

@click.command()
def firstuser():
    '''create the first user for test'''
    if User.find_by_identity(app.config['SEED_ADMIN_EMAIL']) is not None:
        print('already  exist initial user')
        return None

    params = {
        'email': app.config['SEED_ADMIN_EMAIL'],
        'password': User.encryptpassword(app.config['SEED_ADMIN_PASSWORD'])
    }
    u= User(**params)
    admin = Role(name= 'Admin')
    db.session.add(admin)
    db.session.add(u)
    admin.users.append(u)
    db.session.commit()

    return None


@click.command()
@click.option('--with-testdb/--no-with-testdb', default=False,
              help='Create a test db too?')
@click.pass_context
def reset(ctx, with_testdb):
    """
    Init and seed automatically.

    :param with_testdb: Create a test database
    :return: None
    """
    ctx.invoke(init, with_testdb=with_testdb)
    ctx.invoke(firstuser)

    return None

cli.add_command(init)
cli.add_command(firstuser)
cli.add_command(reset)
