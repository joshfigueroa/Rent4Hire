from website import create_app

# Runs __init__.py in debug mode, this is why when database is messed up, the error message comes up on the webpage.
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)#TAKE OUT DEBUG BEFORE PRODUCTION

# HAVING ISSUES STARTING WITH EXISTING DATABASE, IF ERROR IS TRACEDBACK TO user.lastName than delete database file and rerun
