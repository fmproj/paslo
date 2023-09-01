import click
import os
from db.database import add_passrec, get_passrec, list_passrecs

@click.command()
@click.argument("url")
@click.argument("username")
@click.argument("password")
@click.argument("notes")
def add(url, username, password, notes):
    add_passrec(url, username, password, notes)

@click.command()
@click.argument("url")
def get(url):
    click.echo(get_passrec(url))

@click.command()
def list():
    click.echo(list_passrecs())