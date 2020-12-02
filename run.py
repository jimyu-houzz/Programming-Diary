from blog import create_app

# using the function to create the application with multiple packages
# function already has the default class CONFIG, so no need to pass in arguments
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)