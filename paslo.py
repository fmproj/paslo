import click
import cli

@click.group()
def main():
    pass

main.add_command(cli.add)
main.add_command(cli.get)
main.add_command(cli.list)

if __name__ == "__main__":
    main()