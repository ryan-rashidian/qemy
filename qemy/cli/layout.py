""""""

from rich.layout import Layout
from rich.table import Table
from rich.text import Text

layout = Layout()


def concept_layout(
    company: Text,
    data: Table,
    label: Text,
    description: Text
) -> Layout:
    layout.split_column(
        Layout(company, name='Company'),
        Layout(name='Filing')
    )
    layout['Filing'].split_row(
        Layout(data, name='Data'),
        Layout(name='Info')
    )
    layout['Filing']['Info'].split_column(
        Layout(label, name='Description'),
        Layout(description, name='Info')
    )
    return layout

