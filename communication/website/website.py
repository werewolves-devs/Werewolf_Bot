from flask import Flask, render_template, redirect, url_for, request, jsonify
from communication import webhook
import management.items as items
import management.boxes as box
from communication.website.blueprints.api import bp as api_blueprint
import random
import config


app = Flask(__name__)

# This commands is for debugging only
@app.route('/create/<token>')
def create_lootbox(token):
    return render_template('notoken.html', reason='ERROR: This part of the API is only opened in testing stages.')
    if box.add_token(token,248158876799729664,random.randint(0,9999999)) == None:
        return 'ERROR: This token already existed!'
    return 'The token {} has successfully been created.'.format(token)

@app.route('/unbox/<token>/<int:choice>')
def choose_reward(token,choice):
    validity = box.token_status(token)
    if validity != 1:
        return redirect(url_for('open_lootbox', token=token))

    data = box.get_token_data(token)
    given_options = [int(data[3]),int(data[4]),int(data[5])]

    if choice not in given_options:
        return render_template('notoken.html', reason='ERROR: {} is not a valid option.'.format(choice))

    box.add_source2(token,request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    webhook.send_private_message(config.universal_prefix + "SUCCESS {} {}".format(token,choice))
    return render_template('finish.html')


@app.route('/unbox/<token>')
def open_lootbox(token):
    #validity = token
    validity = box.token_status(token)

    if validity == -1:
        # Invalid token
        return render_template('notoken.html', reason="You have filled in a non-existent token!")
    if validity == 2:
        # Token already used
        return render_template('notoken.html', reason="This lootbox has already been redeemed!")

    if validity == 0:
        # The user is prepared to open the lootbox.
        return render_template('open.html', token=token)

    if validity == 1:
        # The user can make a choice.
        data = box.get_token_data(token)
        choices = [int(data[3]),int(data[4]),int(data[5])]
        choices = [items.import_reward(option) for option in choices]

        return render_template('choice.html', choices=choices, token=token)

    return 'This is strange! How did you get here?\nPlease report this to the Game Masters!'

@app.route('/')
def main():
    return render_template('main-index.html')

app.register_blueprint(api_blueprint, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run(debug=True)
