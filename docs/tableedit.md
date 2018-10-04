https://www.jqueryscript.net/tags.php?/editable%20table/
https://markcell.github.io/jquery-tabledit/#examples
https://datatables.net/
http://appendgrid.apphb.com/Download


          customGridButtons: {
            append: function (){
                var button = document.createElement('input');
                button.type = 'button'; button.value = '+'; return button;
            },
            removeLast: function (){
                var button = document.createElement('input');
                button.type = 'button'; button.value = '-'; return button;
            },
            insert: function (){
                var button = document.createElement('input');
                button.type = 'button'; button.value = '+'; return button;
            },
            remove: function (){
                var button = document.createElement('input');
                button.type = 'button'; button.value = '-'; return button;
            },
            moveUp: function (){
                var button = document.createElement('input');
                button.type = 'button'; button.value = '^'; return button;
            },
            moveDown: function (){
                var button = document.createElement('input');
                button.type = 'button'; button.value = '!'; return button;
            },
          },