from tabulate import tabulate
from yattag import Doc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from jinja2 import Template


def GetColumnValues(n, Table):
    """Get the nth column values from a 2D list (table)."""
    try:
        return [item[n] for item in Table]
    except IndexError:
        return []

class ProcessedBiweeklyReport:
    """Class to process and output biweekly weather reports in console, HTML, and plots."""

    def __init__(self, city_name, data, col_names, selected_index):
        self.city_name = city_name
        self.data = data
        self.col_names = col_names
        self.selected_index = selected_index

        # Define plot items with label, index in data, color, and whether to plot on secondary y-axis
        self.plot_items = [
            ("Max Temperature", 0, 'red', False),
            ("Min Temperature", 1, 'blue', False),
            ("Wind Speed", 2, 'green', False),
            ("Precip. Probability", 3, 'yellow', True),
            ("Humidity", 4, 'black', True),
        ]

    def output_biweekly_progression_to_console(self):
        """Print weather data table to console."""
        title = f"Weather Prediction in {self.city_name} between {self.data[0][0]} and {self.data[-1][0]}"
        print(title)
        print(tabulate(self.data, headers=self.col_names, tablefmt="grid"))
        print("")

    def output_biweekly_progression_to_html(self, html_template_path="WeatherPredictionTemplate.html", output_html_path="WeatherPrediction.html"):
        """Generate HTML weather report with a placeholder for interactive plot."""
        title = f"Weather Prediction in {self.city_name} between {self.data[0][0]} and {self.data[-1][0]}"
        doc, tag, text = Doc().tagtext()

        with tag('body'):
            with tag('h1', align="center"):
                text('Biweekly Weather Prediction')

        with tag('p', align="center"):
            with tag('b'):
                text(title)

        doc.asis(str(tabulate(self.data, headers=self.col_names, tablefmt="html", numalign="left", stralign="left")))

        with tag('div', style="break-after:page"):
            text("")

        # Placeholder for plotly figure insertion via Jinja2
        with tag('div'):
            text('{{ fig }}')

        # Write HTML template content
        with open(html_template_path, "a", encoding="utf-8") as f:
            f.write(doc.getvalue())

        # Create and embed the plotly figure into the HTML report
        self.create_plot_biweekly_progression(graph_format="Plotly", 
                                              input_template_path=html_template_path,
                                              output_html_path=output_html_path)

    def create_plot_biweekly_progression(self, graph_format="Plotly", input_template_path=None, output_html_path=None):
        """
        Create and return a plot (Matplotlib or Plotly) based on selected data.
        If Plotly and template/output paths are given, render HTML with embedded plot.
        """
        # Close any existing matplotlib figures
        plt.close('all')

        # Initialize Matplotlib figure and axes if needed
        if graph_format == "Matplotlib":
            fig, primary_ax = plt.subplots()
            secondary_ax = primary_ax.twinx()
            primary_graphs = []
            secondary_graphs = []

        # Initialize Plotly figure with secondary y-axis
        if graph_format == "Plotly":
            fig = make_subplots(specs=[[{"secondary_y": True}]])

        dates = GetColumnValues(0, self.data)
        col_num = 1

        for label, index, color, secondary_y in self.plot_items:
            if index >= len(self.selected_index) or self.selected_index[index] != 1:
                continue  # Skip if not selected

            values = GetColumnValues(col_num, self.data)
            col_num += 1

            if graph_format == "Matplotlib":
                ax = secondary_ax if secondary_y else primary_ax
                graph_line, = ax.plot(dates, values, color=color, label=label)
                if secondary_y:
                    secondary_graphs.append(graph_line)
                else:
                    primary_graphs.append(graph_line)

            elif graph_format == "Plotly":
                fig.add_trace(go.Scatter(x=dates, y=values, mode='lines', name=label, line=dict(color=color)), secondary_y=secondary_y)

        title = f"Weather Prediction in {self.city_name} between {dates[0]} and {dates[-1]}"
        x_label = "Date"
        primary_y_label_parts = []
        if self.selected_index[0] == 1 or self.selected_index[1] == 1:
            primary_y_label_parts.append("Temperature [°C]")
        if self.selected_index[2] == 1:
            primary_y_label_parts.append("Wind Speed [km/h]")
        primary_y_label = " & ".join(primary_y_label_parts)

        secondary_y_label_parts = []
        if self.selected_index[3] == 1:
            secondary_y_label_parts.append("Precip. Prob. [%]")
        if self.selected_index[4] == 1:
            secondary_y_label_parts.append("Humidity [%]")
        secondary_y_label = " & ".join(secondary_y_label_parts)

        if graph_format == "Matplotlib":
            # Format figure
            fig.suptitle(title, fontsize=10)

            box = primary_ax.get_position()
            primary_ax.set_position([box.x0, box.y0 + box.height * 0.15, box.width, box.height * 0.85])

            # Combine legends
            primary_lines, primary_labels = primary_ax.get_legend_handles_labels()
            secondary_lines, secondary_labels = secondary_ax.get_legend_handles_labels()
            primary_ax.legend(primary_lines + secondary_lines, primary_labels + secondary_labels,
                              loc='upper center', bbox_to_anchor=(0.5, -0.225),
                              fancybox=True, shadow=True, ncol=5, prop={'size': 8})

            primary_ax.tick_params(axis='x', labelrotation=45, labelsize=8)
            primary_ax.tick_params(axis='y', labelsize=8)
            secondary_ax.tick_params(axis='y', labelsize=8)

            primary_ax.set_xlabel(x_label, fontsize=9)
            primary_ax.set_ylabel(primary_y_label, fontsize=9)
            secondary_ax.set_ylabel(secondary_y_label, fontsize=9)

            return fig

        elif graph_format == "Plotly":
            fig.update_layout(title_text=title)
            fig.update_xaxes(title_text=x_label)
            fig.update_yaxes(title_text=primary_y_label, secondary_y=False)
            fig.update_yaxes(title_text=secondary_y_label, secondary_y=True)

            # Render plotly figure into HTML template using Jinja2
            if input_template_path and output_html_path:
                with open(input_template_path, encoding="utf-8") as template_file:
                    template_content = template_file.read()

                plotly_html = fig.to_html(full_html=False)
                rendered_html = Template(template_content).render(fig=plotly_html)

                with open(output_html_path, "w", encoding="utf-8") as output_file:
                    output_file.write(rendered_html)

            return fig