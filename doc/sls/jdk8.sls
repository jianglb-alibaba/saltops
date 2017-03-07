send_file:
  file.managed:
      - name: /tmp/jdk-${version}-linux-x64.tar.gz
      - source: salt://files/jdk-${version}-linux-x64.tar.gz

extract_file:
  cmd.run:
      - name: tar -xvf ./jdk-${version}-linux-x64.tar.gz
      - cwd: /tmp
      - unless: test -d /tmp/${arg}
      - require:
        - file: send_file

make_java_dir:
  cmd.run:
      - name: mkdir -p /opt/jdk
      - unless: test -d /opt/jdk/
      - require:
        - cmd: extract_file

move_java:
  cmd.run:
      - name: mv /tmp/${arg} /opt/jdk
      - unless: test -d /opt/jdk/${arg}
      - require:
        - cmd: make_java_dir

change_env:
  cmd.run:
      - name: echo 'JAVA_HOME=/opt/jdk/${arg} \n PATH=$JAVA_HOME/bin:$PATH \n CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar \n export JAVA_HOME \n export PATH \n export CLASSPATH' >> /etc/profile
      - user: root
      - unless: cat /etc/profile|grep JAVA
      - require:
        - cmd: move_java