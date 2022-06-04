from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph


def main():
    # create the pydot graph object by autoloading all tables via a bound metadata object
    graph = create_schema_graph(
        metadata=MetaData("mysql+pymysql://apogee:foobar@localhost/apogee"),
        show_datatypes=False,  # The image would get too big if true
        show_indexes=False,  # ditto for indexes
        rankdir="LR",  # From left to right (instead of top to bottom)
        concentrate=False,  # Don't try to join the relation lines together
    )
    filename = "dbschema.png"
    graph.write_png(filename)  # write out the file
    print(f"Schema UML created: <{filename}>")


if __name__ == "__main__":
    main()
