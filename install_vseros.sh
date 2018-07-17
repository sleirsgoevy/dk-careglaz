mkdir tasksheets/$1
mkdir scoreboard/$1
echo "$2" > tasksheets/$1/name.txt
echo $3 > tasksheets/$1/sortid.txt
echo "import vseros
tasks = vseros.prepare_contest(\"$4\")" > tasksheets/$1/tester.py

