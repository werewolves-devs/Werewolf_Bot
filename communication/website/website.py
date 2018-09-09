from flask import Flask, render_template, redirect, url_for, request, jsonify
import management.items as items
import management.boxes as box
import random


app = Flask(__name__)

# This commands is for debugging only
@app.route('/create/<token>')
def create_lootbox(token):
    #return 'Nice try, bud. Ya can\'t create your own lootboxes this way. ;)'
    if box.add_token(token,12345) == None:
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
        return 'I am sorry! {} is not a valid option.'.format(choice)
    
    box.add_source2(token,request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    box.add_choice(token,choice)
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
    
    return 'This is strange! How did you get here?'


@app.route('/open/<token>')
def open(token):
    validity = box.token_status(token)
    if validity != 0:
        return redirect(url_for('open_lootbox',token=token))
    
    # Add random rewards to lootbox: TODO
    prizes = random.sample(range(100,200),3)
    box.add_options(token,prizes[0],prizes[1],prizes[2])
    box.add_source1(token,request.environ.get('HTTP_X_REAL_IP', request.remote_addr))

    return render_template('unpack.html', token=token)

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

    return jsonify(option1=given_options[0],option2=given_options[1],option3=given_options[2])

if __name__ == '__main__':
    app.run(debug=True)