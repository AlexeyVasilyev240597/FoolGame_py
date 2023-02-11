def display_field(stack, table, players):
    if players['actv'].is_user:
        rival_str =        '         ' + str(players['pssv'].show_set()) + '\n'
        user_str  = '\n' + '!        ' + str(players['actv'].show_set())
    else:
        rival_str =        '!        ' + str(players['actv'].show_set()) + '\n'
        user_str  = '\n' + '         ' + str(players['pssv'].show_set())
    
    table_str = ['', '']
    for c in table.show_set('up'):
        table_str[0] += str(c) + '    '
    for c in table.show_set('down'):
        table_str[1] += str(c) + '    '
    
    field = rival_str
    field = ' --- ' + '    '