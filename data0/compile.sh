src="$1"
dst="$2"

if [ "$3" == cpp ]
then
    echo sandbox/run-sandbox "$dst"
    exec g++ --std=c++14 -x c++ "$src" -o "$dst" -static
fi

echo "Unknown extension: $3" >&2
exit 1
