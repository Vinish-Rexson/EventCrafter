import plotly.graph_objects as go

# Example data for demonstration
dates = ['2024-09-01', '2024-09-02', '2024-09-03', '2024-09-04']
completed_tasks = [10, 15, 12, 20]
total_tasks = [20, 25, 20, 30]

# 1. Task Completion Over Time - Line Chart
fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x=dates, y=completed_tasks, mode='lines+markers', name='Completed Tasks', line=dict(color='green')))
fig_line.add_trace(go.Scatter(x=dates, y=total_tasks, mode='lines+markers', name='Total Tasks', line=dict(color='blue')))
fig_line.update_layout(title='Task Completion Over Time',
                       xaxis_title='Date',
                       yaxis_title='Number of Tasks',
                       template='plotly_white')
fig_line.write_html('templates/task_completion_over_time.html')

# 2. Task Distribution by Assigned User - Pie Chart
labels = ['User A', 'User B', 'User C', 'User D']
sizes = [25, 35, 20, 20]

fig_pie = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=.3)])
fig_pie.update_layout(title='Task Distribution by Assigned User', template='plotly_white')
fig_pie.write_html('templates/task_distribution_by_user.html')

print("Interactive graphs have been generated and saved successfully!")
