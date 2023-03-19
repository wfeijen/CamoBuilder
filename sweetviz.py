import sweetviz as sw
import pandas as pd

data = pd.read_csv('titanic.csv')

analyze_report = sw.analyze_report(data)
analyze_report.show_html('output.html', open_browser=True)