from flask import Flask, render_template, redirect, url_for, request, jsonify
from communication import webhook
import management.items as items
import management.boxes as box
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

@app.route('/api/v1/<token>/rewards')
def get_rewards(token):
    validity = box.token_status(token)
    if validity != 0:
        return jsonify(option1={"code": -1, "description": "NOT FOUND", "name": "NOT FOUND"},
            option2={"code": -1, "description": "NOT FOUND", "name": "NOT FOUND"},
            option3={"code": -1, "description": "NOT FOUND", "name": "NOT FOUND"},)
    
    given_options = items.get_rewards()
    box.add_source1(token,request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    box.add_options(token,given_options[0]["code"],given_options[1]["code"],given_options[2]["code"])

    # Make an announcement if any legendaries found
    legendary_amount = 0
    for option in given_options:
        if option["code"] > 4000000-1:
            legendary_amount += 1
    if legendary_amount > 3:
        print("Invalid amount of legendaries found.")
    if legendary_amount == 3:
        webhook.send_public_message("**NO WAY!** <@{}> just found ***THREE LEGENDARIES*** in a lootbox!\nThat's a chance of 1 in 1 MILLION!".format(box.get_token_data(token)[1]))
    if legendary_amount == 2:
        webhook.send_public_message("<@{}> just opened a lootbox with two legendaries! Wow!".format(box.get_token_data(token)[1]))
    if legendary_amount == 1:
        webhook.send_public_message("<@{}> just found a legendary item in a lootbox!".format(box.get_token_data(token)[1]))

    return jsonify(option1=given_options[0],option2=given_options[1],option3=given_options[2])

if __name__ == '__main__':
    app.run(debug=True)
