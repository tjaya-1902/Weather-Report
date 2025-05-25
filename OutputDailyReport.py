from tabulate import tabulate
from yattag import Doc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from jinja2 import Template

def get_column_values(n, table):
    return [item[n] for item in table]

class ProcessedDailyReport:
    def __init__(self, city_name, data, col_names, selected_index):
        self.city_name = city_name
        self.data = data
        self.col_names = col_names
        self.selected_index = selected_index

    def output_daily_progression_to_console(self):
        days = min(3, len(self.data))
        for i in range(days):
            date = self.data[i][-1]
            print(f"Daily Weather Prediction in {self.city_name} on {date}")
            print(tabulate(self.data[i][:-1], headers=self.col_names, tablefmt="grid"))
            print("")

    def output_daily_progression_to_html(self,
                                         template_path="WeatherPredictionTemplate.html",
                                         output_path="WeatherPrediction.html"):
        doc, tag, text = Doc().tagtext()

        with tag('body'):
            with tag('h1', align="center"):
                text('Weather Prediction on Coming Days')

            days = min(3, len(self.data))
            for i in range(days):
                with tag('div', klass="grid-container"):
                    with tag('div'):
                        with tag('p', align="center"):
                            with tag('b'):
                                text(f'Date: {self.data[i][-1]}')

                        doc.asis(str(tabulate(self.data[i][:-1],
                                              headers=self.col_names,
                                              tablefmt="html",
                                              numalign="left",
                                              stralign="left")))

                    with tag('div'):
                        with tag('h1'):
                            text(f'{{{{ fig{i} }}}}')  # double braces for Jinja2 placeholder

                if i != days - 1:
                    with tag('div', style="break-after:page"):
                        text("")

        with open(template_path, "a", encoding="utf-8") as f:
            f.write(doc.getvalue())

        self.create_plot_daily_progression('Plotly', template_path, output_path)

    def create_plot_daily_progression(self, graph_format, template_path=None, output_path=None):
        plt.close('all')

        days = min(3, len(self.data))
        matplotlib_figs = []
        plotly_figs = []

        for i in range(days):

            day_data = self.data[i][:-1]  # all except last date entry

            hour_values = get_column_values(0, day_data)
            col_num = 1

            # Matplotlib setup
            if graph_format == "Matplotlib":
                fig, primary_ax = plt.subplots()
                secondary_ax = primary_ax.twinx()
                primary_lines = []
                secondary_lines = []

            # Plotly setup
            if graph_format == "Plotly":
                fig = make_subplots(specs=[[{"secondary_y": True}]])

            # Define plot items: (selected_index_pos, label, color, secondary_y)
            plot_defs = [
                (0, "Temperature", "blue", False),
                (1, "Wind Speed", "red", False),
                (2, "Humidity", "green", True)
            ]

            for idx, label, color, secondary_y in plot_defs:
                if idx >= len(self.selected_index) or self.selected_index[idx] != 1:
                    continue
                
                values = get_column_values(col_num, day_data)
                col_num += 1

                if graph_format == "Matplotlib":
                    ax = secondary_ax if secondary_y else primary_ax
                    line, = ax.plot(hour_values, values, color=color, label=label)
                    if secondary_y:
                        secondary_lines.append(line)
                    else:
                        primary_lines.append(line)

                elif graph_format == "Plotly":
                    fig.add_trace(go.Scatter(x=hour_values, y=values, mode='lines',
                                             name=label, line=dict(color=color)),
                                  secondary_y=secondary_y)

            title = f"Weather Prediction in {self.city_name} on {self.data[i][-1]}"
            x_label = "Time of Day"
            primary_y_label = " & ".join(lbl for sel, lbl, _, sec in plot_defs if self.selected_index[sel] == 1 and not sec)
            secondary_y_label = " & ".join(lbl for sel, lbl, _, sec in plot_defs if self.selected_index[sel] == 1 and sec)

            if graph_format == "Matplotlib":
                fig.suptitle(title, fontsize=8)
                box = primary_ax.get_position()
                primary_ax.set_position([box.x0, box.y0 + box.height * 0.15, box.width, box.height * 0.85])

                primary_ax.legend(primary_lines + secondary_lines,
                                  [l.get_label() for l in primary_lines + secondary_lines],
                                  loc='upper center', bbox_to_anchor=(0.5, -0.225),
                                  fancybox=True, shadow=True, ncol=5, prop={'size': 6})

                primary_ax.tick_params(axis='x', labelsize=6, labelrotation=45)
                primary_ax.tick_params(axis='y', labelsize=6)
                secondary_ax.tick_params(axis='y', labelsize=6)

                primary_ax.set_xlabel(x_label, fontsize=8)
                primary_ax.set_ylabel(primary_y_label, fontsize=8)
                secondary_ax.set_ylabel(secondary_y_label, fontsize=8)

                matplotlib_figs.append(fig)

            elif graph_format == "Plotly":
                fig.update_layout(title_text=title)
                fig.update_xaxes(title_text=x_label, tickangle=45)
                fig.update_yaxes(title_text=primary_y_label, secondary_y=False)
                fig.update_yaxes(title_text=secondary_y_label, secondary_y=True)
                plotly_figs.append(fig)

        if graph_format == "Matplotlib":
            return matplotlib_figs

        elif graph_format == "Plotly":
            if template_path is None or output_path is None:
                return plotly_figs

            # Read template, render with figures, write output HTML
            with open(template_path, encoding="utf-8") as template_file:
                template_content = template_file.read()

            context = {f"fig{i}": fig.to_html(full_html=False) for i, fig in enumerate(plotly_figs)}

            rendered_html = Template(template_content).render(context)

            with open(output_path, "a", encoding="utf-8") as output_file:
                output_file.write(rendered_html)

            return plotly_figs