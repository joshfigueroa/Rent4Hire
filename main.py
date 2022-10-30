from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)#TAKE OUT DEBUG BEFORE PRODUCTION

# HAVING ISSUES STARTING WITH EXISTING DATABASE