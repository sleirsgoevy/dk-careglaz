if [ "x$4" == x ]
then
    cat >&2 << EOF
Usage: install_vseros.sh <id> <name> <sortid> <archive_dir>
EOF
    exit 1
fi

mkdir data/tasksheets/$1
mkdir data/scoreboard/$1
echo "$2" > data/tasksheets/$1/name.txt
echo $3 > data/tasksheets/$1/sortid.txt
echo "import vseros
tasks = vseros.prepare_contest(\"$4\")" > data/tasksheets/$1/tester.py

