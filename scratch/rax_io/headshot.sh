#!/bin/bash


cat << "EOF"
  +-'~`---------------------------------/\--
 ||"""""""""""""""""""""""""""""""" \\\\\\  \/~)
 || *BOOM* HEADSHOT                  \\\\\\  \/_
  |~~~~~~~~-________________-_________________\ ~--_
  !---------|_________       ------~~~~~(--   )--~~
                      \ /~~~~\~~\   )--- \_ /(
                       ||     |  | \   ()   \\
                       \\____/_ / ()\        \\
                        `~~~~~~~~~-. \        \\
                                    \ \  <($)> \\
                                     \ \        \\
                                      \ \        \\
                                       \ \        \\
                                        \ \  ()    \|
                                        _\_\__====~~~
EOF


ansible-playbook -f 8 -i/tmp/inventory headshot.pb


