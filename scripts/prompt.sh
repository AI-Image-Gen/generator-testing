pip install -U pip
pip install -U g4f

mkdir -p ./tmp
if [ -n "$PROMPT" ]; then
    python prompt.py $CONFIGPATH "$PROMPT"
else 
    python prompt.py $CONFIGPATH
fi