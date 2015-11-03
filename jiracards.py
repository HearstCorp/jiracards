from flask import Flask, render_template, request
from flask.ext.basicauth import BasicAuth
from jira.client import GreenHopper
from jira.resources import Issue

app = Flask(__name__)
app.config.from_object('settings')
basic_auth = BasicAuth(app)

gh = GreenHopper(
    {'server': app.config.get('JIRA_HOST')},
    basic_auth=(app.config.get('JIRA_USERNAME'),
                app.config.get('JIRA_PASSWORD')))


@app.route('/', methods=['GET', 'POST'])
def index():
    board_id = sprint_id = None

    if request.method == 'POST':
        board_id = request.form.get('board_id', None)
        sprint_id = request.form.get('sprint_id', None)

        if board_id and sprint_id:
            print_issues = []

            # Get around python jira lib not getting incomplete issues properly at the moment
            # issues = gh.incompleted_issues(board_id, sprint_id)
            r_json = gh._get_json('rapid/charts/sprintreport?rapidViewId=%s&sprintId=%s' % (
                board_id, sprint_id), base=gh.AGILE_BASE_URL)
            issues = [
                Issue(gh._options, gh._session, raw_issues_json)
                for raw_issues_json in r_json['contents']['issuesNotCompletedInCurrentSprint']]

            for issue in issues:
                try:
                    epic_title = issue.epicField.text
                    epic_color_label = issue.epicField.epicColor
                except AttributeError:
                    epic_title = None
                    epic_color_label = 'default-label'

                i = gh.issue(issue.key)

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
    projects = gh.boards()
    sprints = gh.sprints(board_id) if board_id else None

    return render_template('select-sprint.html',
                           projects=projects,
                           sprints=sprints,
                           board_id=board_id,
                           sprint_id=sprint_id)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
