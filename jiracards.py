from flask import Flask, render_template, request
from flask.ext.basicauth import BasicAuth
from jira.client import GreenHopper

app = Flask(__name__)
app.config.from_object('settings')
basic_auth = BasicAuth(app)

jira = GreenHopper(
    {'server': app.config.get('JIRA_HOST')},
    basic_auth=(app.config.get('JIRA_USERNAME'),
                app.config.get('JIRA_PASSWORD')))


@app.route('/', methods=['GET', 'POST'])
def index():
    project_id = sprint_id = None

    if request.method == 'POST':
        project_id = request.form.get('project_id', None)
        sprint_id = request.form.get('sprint_id', None)

        if project_id and sprint_id:
            print_issues = []
            issues = jira.incompleted_issues(project_id, sprint_id)

            for issue in issues:
                try:
                    epic_title = issue.epicField.text
                    epic_color_label = issue.epicField.epicColor
                except AttributeError:
                    epic_title = None
                    epic_color_label = 'default-label'

                i = jira.issue(issue.key)

                story_points = getattr(i.fields, 'customfield_10004', None)

                print_issues.append({
                    'id': i.key.split('-', 1)[-1],
                    'title': i.fields.summary,
                    'description': i.fields.description,
                    'reporter': i.fields.reporter.displayName,
                    'points': int(story_points) if story_points else None,
                    'epic_title': epic_title,
                    'epic_color_label': epic_color_label,
                })

            return render_template('jiracards.html', stories=print_issues)
    projects = jira.boards()
    sprints = jira.sprints(project_id) if project_id else None

    return render_template('select-sprint.html',
                           projects=projects,
                           sprints=sprints,
                           project_id=project_id,
                           sprint_id=sprint_id)


if __name__ == '__main__':
    app.run(port=5000, debug=True)

