# """Tasks running the results formatting (tables, figures)."""

# import pandas as pd
# import pytask

# from final_project_yingyu.config import BLD
# from final_project_yingyu.final import plot_weights

# kwargs={"produces":BLD/"python"/"figures"/"plot_weights.png"}

# @pytask.mark.depends_on(
#         {
#             "IO_naics_2_digit": BLD / "python" / "data" / "IO_naics_2_digit.csv",
#             "weights": BLD / "python" / "data" / "weights.csv",
#         },
#     )
# @pytask.mark.task(kwargs=kwargs)
# def task_plot_weights_python(depends_on, produces):
#     """plots."""
#     IO_naics_2_digit=pd.read_csv(depends_on["IO_naics_2_digit"])
#     weights=pd.read_csv(depends_on["weights"])
#     fig=plot_weights(IO_naics_2_digit,weights)
#     fig.write_image(produces)