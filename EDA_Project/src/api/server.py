from flask import Flask, request, render_template
import os
import sys
import json
import argparse

dir = os.path.dirname
path = dir(dir(dir(__file__)))
sys.path.append(path)

parser= argparse.ArgumentParser()
parser.add_argument('-x', '--x', type= int)
args = vars(parser.parse_args())

if args['x'] == 8642:

    from src.utils.apis_tb import read_json
    from src.utils.apis_tb import cvs_to_json
    # Mandatory
    app = Flask(__name__)  # __name__ --> __main__  

    # ---------- Flask functions ----------

    # localhost:6060/give_me_id?password=12345
    @app.route('/get_API', methods=['GET'])
    def give_id():
        x = request.args['Token_id']
        if x == "L16092222":
            new_path = path + os.sep + 'Data' + os.sep + 'Def_Data' + os.sep 
            return cvs_to_json(fullpath= new_path, extension='fleet_seatrade')
        else:
            return "No es la contraseña correcta"



    # ---------- Other functions ----------

    def main():
        print("---------STARTING PROCESS---------")
        print(__file__)
        
        # Get the settings fullpath
        # \\ --> WINDOWS
        # / --> UNIX
        # Para ambos: os.sep
        settings_file = os.path.dirname(__file__) + os.sep + "settings.json"
        print(settings_file)
        # Load json from file
        json_readed = read_json(fullpath=settings_file)
        
        # Load variables from jsons
        SERVER_RUNNING = json_readed["server_running"]
        print("SERVER_RUNNING", SERVER_RUNNING)
        if SERVER_RUNNING:
            DEBUG = json_readed["debug"]
            HOST = json_readed["host"]
            PORT_NUM = json_readed["port"]
            app.run(debug=DEBUG, host=HOST, port=PORT_NUM)
        else:
            print("Server settings.json doesn't allow to start server. " + 
                "Please, allow it to run it.")

    if __name__ == "__main__":
        main()

else:
    print('wrong password')