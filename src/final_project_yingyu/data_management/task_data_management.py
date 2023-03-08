"""Tasks for managing the data."""

import pandas as pd
import pytask

from final_project_yingyu.config import BLD, SRC
from final_project_yingyu.data_management import clean_data


@pytask.mark.depends_on(
    {
        "scripts": ["clean_data.py"],
        "bds": SRC / "data" / "bds_all.csv",
        "sic_naics": SRC / "data" / "sic-naics.csv",
        "data": SRC / "data" / "emp.csv",
        "io_naics": SRC / "data" / "io_naics_raw.csv",
        "io": SRC / "data" / "io.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "data" / "IO_naics_2_digit.csv")
def task_clean_IO_python(depends_on, produces):
    """Generate cleaned data.

    Args:
        depends_on (_type_): _description_
        produces (_type_): _description_
    """
    data = pd.read_csv(depends_on["data"])
    bds = pd.read_csv(depends_on["bds"])
    sic_naics = pd.read_excel(depends_on["sic_naics"])
    io_naics = pd.read_csv(depends_on["io_naics"])
    io = pd.read_csv(depends_on["io"])
    IO_naics_2_digit = clean_data(sic_naics, data, io_naics, bds, io )
    IO_naics_2_digit.to_csv(produces, index=False)



# @pytask.mark.depends_on(
#     {
#         "scripts": ["clean_data.py"],
#         "bds": SRC / "data" / "bds_all.csv",
#         "sic_naics": SRC / "data" / "sic-naics.csv",
#         "data": SRC / "data" / "emp.csv",
#         "io_naics": SRC / "data" / "io_naics_raw.csv",
#         "io": SRC / "data" / "io.csv",
#     },
# )
# @pytask.mark.produces(BLD / "python" / "data" / "IO_naics_2_digit.csv")
# def task_clean_IO_nacis_python(depends_on, produces):
#     """Generate cleaned data.

#     Args:
#         depends_on (_type_): _description_
#         produces (_type_): _description_
#     """
#     data = pd.read_csv(depends_on["data"])
#     bds = pd.read_csv(depends_on["bds"])
#     sic_naics = pd.read_csv(depends_on["sic_naics"])
#     io_naics = pd.read_csv(depends_on["io_naics"])
#     io = pd.read_csv(depends_on["io"])
#     IO_naics_2_digit = clean_data(sic_naics, data, io_naics, bds, io )    
#     IO_naics_2_digit.to_csv(produces, index=False)    


@pytask.mark.depends_on(
    {
        "scripts": ["clean_data.py"],
        "bds": SRC / "data" / "bds_all.csv",
        "sic_naics": SRC / "data" / "sic-naics.csv",
        "data": SRC / "data" / "emp.csv",
        "io_naics": SRC / "data" / "io_naics_raw.csv",
        "io": SRC / "data" / "io.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "data" / "weights.csv")
def task_weights_python(depends_on, produces):
    """Generate cleaned data.

    Args:
        depends_on (_type_): _description_
        produces (_type_): _description_
    """
    data = pd.read_csv(depends_on["data"])
    bds = pd.read_csv(depends_on["bds"])
    sic_naics = pd.read_csv(depends_on["sic_naics"])
    io_naics = pd.read_csv(depends_on["io_naics"])
    io = pd.read_csv(depends_on["io"])
    weights = clean_data(sic_naics, data, io_naics, bds, io )
    weights.to_csv(produces, index=False)