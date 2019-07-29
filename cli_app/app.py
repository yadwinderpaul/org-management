import click
import functools
from initialize import InitConfig, InitLogger, InitAdapter
from organizations import Organizations,\
    OrganizationsException,\
    InvalidInputException,\
    AbsentResourceException,\
    UnavailableException

app = {}

config = InitConfig(app)
config['LOG_LEVEL'] = 'ERROR'
app['config'] = config

logger = InitLogger(app)
app['logger'] = logger

adapter = InitAdapter(app)
app['organizations_adapter'] = adapter

organizations = Organizations(app)
app['organizations'] = organizations


def handle_organizations_exceptions(fun):
    @functools.wraps(fun)
    def func(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except InvalidInputException as ex:
            print(str(ex))
        except AbsentResourceException as ex:
            print(str(ex))
        except UnavailableException as ex:
            print(str(ex))
        except OrganizationsException as ex:
            print(str(ex))
    return func


@click.group()
def cli_app():
    pass


@click.command()
@click.option('--start',
              type=click.INT,
              default=0)
@handle_organizations_exceptions
def list_org(start):
    res = app['organizations'].list(start)
    print(res)


@click.command()
@click.argument('id', type=click.INT)
@handle_organizations_exceptions
def get(id):
    res = app['organizations'].get(id)
    print(res)


@click.command()
@click.option('--name', required=True, type=click.STRING)
@click.option('--url', required=True, type=click.STRING)
@click.option('--address', required=True, type=click.STRING)
@click.option('--lat', required=True, type=click.FLOAT)
@click.option('--lng', required=True, type=click.FLOAT)
@handle_organizations_exceptions
def create(name, url, address, lat, lng):
    details = {
        'name': name,
        'url': url,
        'address': address,
        'lat': lat,
        'lng': lng
    }
    res = app['organizations'].create(details)
    print(res)


@click.command()
@click.option('--id', required=True, type=click.STRING)
@click.option('--name', required=True, type=click.STRING)
@click.option('--url', type=click.STRING)
@click.option('--address', type=click.STRING)
@click.option('--lat', type=click.FLOAT)
@click.option('--lng', type=click.FLOAT)
@handle_organizations_exceptions
def update(id, name, url=None, address=None, lat=None, lng=None):
    details = {
        'name': name,
        'url': url,
        'address': address,
        'lat': lat,
        'lng': lng
    }
    res = app['organizations'].update(id, details)
    print(res)


@click.command()
@click.argument('id', type=click.INT)
@handle_organizations_exceptions
def delete(id):
    res = app['organizations'].delete(id)
    print(res)


@click.command()
@click.option('--query', type=click.STRING, required=True)
@click.option('--user_lat', type=click.FLOAT)
@click.option('--user_lng', type=click.FLOAT)
@click.option('--start',
              type=click.INT,
              default=0)
@handle_organizations_exceptions
def search(query, user_lat, user_lng, start):
    res = app['organizations'].search(query,
                                      user_lat=user_lat,
                                      user_lng=user_lng,
                                      start=start)
    print(res)


cli_app.add_command(list_org, name='list')
cli_app.add_command(get)
cli_app.add_command(create)
cli_app.add_command(update)
cli_app.add_command(delete)
cli_app.add_command(search)

cli_app()
