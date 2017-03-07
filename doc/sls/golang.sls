send_file:
  file.managed:
      - name: /tmp/go${version}.linux-amd64.tar.gz
      - source: salt://go${version}.linux-amd64.tar.gz
      - unless: test -f /tmp/go${version}.linux-amd64.tar.gz

extract_file:
  cmd.run:
      - name: tar -xvf ./go${version}.linux-amd64.tar.gz
      - cwd: /tmp
      - unless: test -d /tmp/go
      - require:
        - file: send_file

move_go:
  cmd.run:
      - name: mv /tmp/go /opt/
      - unless: test -d /opt/go/
      - require:
        - cmd: extract_file


make_gopath:
  cmd.run:
      - name: mkdir /opt/gopath
      - unless: test -d /opt/gopath/
      - require:
        - cmd: move_go

change_env:
  cmd.run:
      - name: echo 'GO_HOME=/opt/go \n PATH=$GO_HOME/bin:$PATH \n export GO_HOME \n GO_PATH=/opt/gopath \n export PATH' >> /etc/profile
      - user: root
      - unless: cat /etc/profile|grep GO_HOME
      - require:
        - cmd: make_gopath