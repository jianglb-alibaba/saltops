{% set es = "elasticsearch-${version}" %}
send_file:
  file.managed:
      - name: /tmp/{{es}}.tar.gz
      - user: kira
      - unless: test -f /tmp/{{es}}.tar.gz
      - source: salt://files/{{es}}.tar.gz

extract_file:
  cmd.run:
      - name: tar -xvf ./{{es}}.tar.gz
      - cwd: /tmp
      - user: kira
      - unless: test -d /tmp/{{es}}
      - require:
          - file: send_file

install_head:
  cmd.run:
      - name: ./bin/plugin install mobz/elasticsearch-head
      - cwd: /tmp/{{es}}
      - user: kira
      - unless: test -d ./plugins/head
      - require:
          - cmd: extract_file

run_es:
  cmd.run:
      - cwd: /tmp/{{es}}/bin
      - name: ./elasticsearch -d &
      - user: kira
      - unless: ps -ef|grep elasticsearch|grep -v grep
      - require:
          - cmd: install_head