def import_story(folder,owner='UNDEFINED',player_list=[]):
    with open('story_time/' + folder,'r') as read_file:
        msg = ''
        for line in read_file:
            broken_input = line.split('[owner]')
            for i in range(len(broken_input)):
                if i > 0:
                    msg += owner
                msg += insert_user(broken_input[i],i,player_list)

        return msg

def insert_user(line,i,player_list):
    if len(player_list) <= i:
        return line

    user = player_list[i]
    broken_input = line.split('[{}]'.format(i))
    msg = ''
    for j in range(len(broken_input)):
        if j > 0:
            msg += user
        msg += insert_user(broken_input[j],i+1,player_list)
    
    return msg

def player_amount(folder,i=1):
    with open('story_time/' + folder,'r') as read_file:
        for line in read_file:
            if '[{}]'.format(i-1) in line:
                return player_amount(folder,i+1)
        return i-1