import matplotlib.pyplot as plt
import numpy as np

# Example data for demonstration
dates = ['2024-09-01', '2024-09-02', '2024-09-03', '2024-09-04']
completed_tasks = [10, 15, 12, 20]
total_tasks = [20, 25, 20, 30]

# 1. Task Completion Over Time - Line Chart
plt.figure(figsize=(10, 5))
plt.plot(dates, completed_tasks, marker='o', label='Completed Tasks', color='green')
plt.plot(dates, total_tasks, marker='o', label='Total Tasks', color='blue')
plt.title('Task Completion Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Tasks')
plt.legend()
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout
plt.savefig('static/images/task_completion_over_time.png')  # Save the figure
plt.close()

# 2. Task Distribution by Assigned User - Donut Chart
labels = ['User A', 'User B', 'User C', 'User D']
sizes = [25, 35, 20, 20]
colors = plt.cm.Paired.colors

plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
centre_circle = plt.Circle((0, 0), 0.70, fc='white')  # Create a donut chart
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.axis('equal')
plt.title('Task Distribution by Assigned User')
plt.tight_layout()  # Adjust layout
plt.savefig('static/images/task_distribution_donut_chart.png')  # Save the figure
plt.close()

# 3. Task Assignment Over Time - Bar Chart
assignees = ['User A', 'User B', 'User C', 'User D']
tasks_assigned = [5, 10, 8, 12]

plt.figure(figsize=(10, 5))
plt.bar(assignees, tasks_assigned, color='orange')
plt.title('Tasks Assigned to Users')
plt.xlabel('Users')
plt.ylabel('Number of Tasks')
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout
plt.savefig('static/images/tasks_assigned_bar_chart.png')  # Save the figure
plt.close()

# 4. Task Completion Rate - Horizontal Bar Chart
completion_rates = [50, 60, 70, 80]  # Percentages
plt.figure(figsize=(10, 5))
plt.barh(assignees, completion_rates, color='purple')
plt.title('Task Completion Rate by User')
plt.xlabel('Completion Rate (%)')
plt.xlim(0, 100)
plt.tight_layout()  # Adjust layout
plt.savefig('static/images/task_completion_rate_horizontal.png')  # Save the figure
plt.close()

# 5. Tasks Over Time - Area Chart
task_counts = [5, 15, 10, 20]  # Example task counts over days
plt.figure(figsize=(10, 5))
plt.fill_between(dates, task_counts, color="skyblue", alpha=0.4)
plt.plot(dates, task_counts, color="Slateblue", alpha=0.6)
plt.title('Tasks Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Tasks')
plt.xticks(rotation=45)
plt.tight_layout()  # Adjust layout
plt.savefig('static/images/tasks_over_time_area_chart.png')  # Save the figure
plt.close()

print("All graphs have been generated and saved successfully!")
