
/**
 * 
 * @returns
 */
function display_terminal_panel() {
    if (antaresTerminalLinks.terminal_call) {
        $('#antares_terminal')
            .terminal(
                function(command, term) {
                    $
                        .ajax({
                            'method': 'POST',
                            'dataType': 'json',
                            'url': antaresTerminalLinks.terminal_call,
                            'data': {
                                'csrfmiddlewaretoken': $.cookie('csrftoken'),
                                'action': [
                                    command,
                                ]
                            },
                            'success': function(response) {
                                term.echo(response.message, {
                                    'raw': true
                                });
                            }
                        });
                }, {
                    greetings: gettext('antares.apps.terminal.welcome'),
                    onBlur: function() {
                        // the height of the body is only 2 lines initialy
                        return false;
                    },
                    height: 400,
                    prompt: '> '
                });
    }
}